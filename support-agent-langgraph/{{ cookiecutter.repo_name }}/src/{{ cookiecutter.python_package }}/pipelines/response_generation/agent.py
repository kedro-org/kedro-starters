from functools import partial
from typing import TypedDict, Any

from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.runnables import Runnable
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from pydantic import BaseModel, Field

from ...utils import KedroAgent, AgentContext


class AgentState(TypedDict):
    """Shared state across nodes in the response generation flow."""

    messages: list[BaseMessage]
    intent: str
    intent_generator_summary: str
    user_context: dict


class ResponseOutput(BaseModel):
    """Structured schema for the final response."""

    message: str = Field(..., description="Final message for the user")
    claim_created: bool = Field(
        default=False, description="Whether a claim was created"
    )
    escalation: bool = Field(default=False, description="Whether escalation is needed")


class ResponseGenerationAgent(KedroAgent):
    """
    Agent responsible for generating final user-facing responses.

    - Decides whether tools should be invoked (via tool_calling_llm).
    - Executes tools if needed.
    - Generates structured final responses using context + tool outputs.
    """

    def __init__(self, context: AgentContext):
        super().__init__(context)
        self.compiled_graph: CompiledStateGraph | None = None
        self.memory: MemorySaver | None = None

        # Available tools
        self.tools = list(self.context.tools.values())

        # LLM that decides tool usage
        llm_with_tools = self.context.llm.bind_tools(self.tools)
        self.llm_with_tools = self.context.get_prompt("tool_prompt") | llm_with_tools

        # LLM that generates structured final response
        structured_llm = self.context.llm.with_structured_output(ResponseOutput)
        self.response_chain = (
            self.context.get_prompt("response_prompt") | structured_llm
        )

    def compile(self):
        """Compile the state graph for response generation."""
        builder = StateGraph(AgentState)

        builder.add_node(
            "tool_calling_llm",
            partial(tool_calling_llm, llm_with_tools=self.llm_with_tools),
        )
        builder.add_node("tools", ToolNode(self.tools))
        builder.add_node(
            "generate_response",
            partial(generate_response, response_chain=self.response_chain),
        )

        builder.add_edge(START, "tool_calling_llm")
        builder.add_conditional_edges(
            "tool_calling_llm",
            tools_condition,
            {"tools": "tools", "none": "generate_response"},
        )
        builder.add_edge("tools", "generate_response")
        builder.add_edge("generate_response", END)

        # Compile with memory persistence
        self.memory = MemorySaver()
        self.compiled_graph = builder.compile(checkpointer=self.memory)

    def invoke(self, context: dict, config: dict | None = None) -> Any:
        """
        Run the compiled intent detection graph.

        Args:
            context: State dictionary passed into the agent graph.
            config: Optional runtime configuration for execution.

        Returns:
            The graph output after execution.

        Raises:
            ValueError: If the graph has not been compiled via `compile()`.
        """
        if self.compiled_graph:
            return self.compiled_graph.invoke(context, config)
        raise ValueError(
            f"{self.__class__.__name__} must be compiled before invoking. Call .compile() first."
        )


def tool_calling_llm(state: AgentState, llm_with_tools: Runnable):
    """
    Use LLM to decide whether to call tools.

    Args:
        state: Current agent state.
        llm_with_tools: Runnable LLM bound with tool capabilities.

    Returns:
        Updated state with tool call decision message.
    """
    query = {
        "intent": state["intent"],
        "intent_generator_summary": state.get("intent_generator_summary", ""),
        "user_id": state.get("user_context", {})
        .get("profile", {})
        .get("user_id", "unknown"),
    }
    result = {"messages": [llm_with_tools.invoke(query)]}

    for m in result["messages"]:
        m.pretty_print()

    return result


def generate_response(state: AgentState, response_chain: Runnable):
    """
    Generate final structured response using tool outputs + context.

    Args:
        state: Current agent state with messages, intent, and context.
        response_chain: Runnable LLM chain for structured response generation.

    Returns:
        Updated state with final AI response and metadata flags.
    """
    created_claim = [
        m for m in state["messages"] if getattr(m, "name", "") == "create_claim"
    ]
    doc_results = [
        m for m in state["messages"] if getattr(m, "name", "") == "lookup_docs"
    ]
    user_claims = [
        m for m in state["messages"] if getattr(m, "name", "") == "get_user_claims"
    ]

    created_claim_str = "\n".join([str(r.content) for r in created_claim])
    doc_results_str = "\n".join([str(r.content) for r in doc_results])
    user_claims_str = "\n".join([str(r.content) for r in user_claims])

    result: ResponseOutput = response_chain.invoke(
        {
            "intent": state["intent"],
            "intent_generator_summary": state["intent_generator_summary"],
            "user_context": state["user_context"],
            "created_claim": created_claim_str,
            "docs_lookup": doc_results_str,
            "user_claims": user_claims_str,
        }
    )

    return {
        "messages": state["messages"] + [AIMessage(content=result.message)],
        "claim_created": result.claim_created,
        "escalated": result.escalation,
    }
