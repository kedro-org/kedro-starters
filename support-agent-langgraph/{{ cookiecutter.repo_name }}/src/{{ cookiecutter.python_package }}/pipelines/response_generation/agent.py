"""
Response-generation agent powered by LangGraph, selecting tools when needed
and producing a structured final answer. Extend this module to add new nodes,
tool-routes, or modify how the agent composes responses.
"""

from functools import partial
from typing import TypedDict, Any

from kedro.pipeline import LLMContext
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.runnables import Runnable
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from pydantic import BaseModel, Field

from ...utils import KedroAgent


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

    def __init__(self, context: LLMContext):
        super().__init__(context)
        self.compiled_graph: CompiledStateGraph | None = None
        self.memory: MemorySaver | None = None

        # Available tools
        self.tools = list(self.context.tools.values())

        # LLM that decides tool usage
        llm_with_tools = self.context.llm.bind_tools(self.tools)
        self.llm_with_tools = self.context.prompts["tool_prompt"] | llm_with_tools

        # LLM that generates structured final response
        structured_llm = self.context.llm.with_structured_output(ResponseOutput)
        self.response_chain = self.context.prompts["response_prompt"] | structured_llm

    @staticmethod
    def _build_graph(
        *,
        tool_calling_node,
        tools_node,
        generate_response_node,
        tools_condition_fn,
    ) -> StateGraph:
        """
        Construct the response-generation state graph with injected node behavior.

        This method defines the *static topology* of the agent's LangGraph:
        - node names
        - execution order
        - conditional routing logic

        The concrete behavior of each node (LLMs, tools, no-op placeholders)
        is injected via callables, allowing the same graph structure to be
        reused for:
          - runtime execution (real LLMs, tools, memory)
          - static preview / visualization (no-op nodes)

        This method should be the single source of truth for the graph structure.
        Any change to node wiring or control flow must happen here.

        Args:
            tool_calling_node:
                Callable implementing the tool-decision step.
                At runtime, this invokes an LLM; for previews, this is a no-op.
            tools_node:
                Callable or ToolNode responsible for executing selected tools.
            generate_response_node:
                Callable that generates the final structured response.
            tools_condition_fn:
                Function that inspects state and decides whether tool execution
                is required ("tools") or can be skipped ("none").

        Returns:
            A StateGraph defining the response-generation workflow,
            ready to be compiled.
        """
        builder = StateGraph(AgentState)

        builder.add_node("tool_calling_llm", tool_calling_node)
        builder.add_node("tools", tools_node)
        builder.add_node("generate_response", generate_response_node)

        builder.add_edge(START, "tool_calling_llm")
        builder.add_conditional_edges(
            "tool_calling_llm",
            tools_condition_fn,
            {"tools": "tools", "none": "generate_response"},
        )
        builder.add_edge("tools", "generate_response")
        builder.add_edge("generate_response", END)

        return builder

    @staticmethod
    def graph() -> StateGraph:
        """
        Create a static, non-executable version of the agent graph for previewing.

        This method returns the same graph structure used at runtime, but with
        placeholder (no-op) nodes and a fixed routing condition. It is intended
        exclusively for:
          - Mermaid diagram rendering
          - Documentation
          - Architecture inspection

        The returned graph is *not* suitable for execution, but guarantees that
        any structural change to the runtime graph is immediately reflected
        in previews and diagrams.

        Returns:
            A StateGraph with no-op node implementations, suitable for compilation
            and visualization.
        """
        return ResponseGenerationAgent._build_graph(
            tool_calling_node=lambda x: x,
            tools_node=lambda x: x,
            generate_response_node=lambda x: x,
            tools_condition_fn=lambda _: "none",
        )

    def compile(self):
        """
        Compile the executable response-generation graph with runtime dependencies.

        This method binds concrete implementations to the static graph structure:
          - LLM-powered tool decision logic
          - Tool execution via ToolNode
          - Final response generation chain
          - Persistent memory / checkpointing

        It reuses the same graph topology defined in `_build_graph`, ensuring that
        the executable agent and its visualized architecture are always in sync.

        After calling this method, the agent is ready to be invoked.

        Raises:
            RuntimeError:
                If required runtime dependencies (LLM, tools, prompts) are missing.
        """
        self.memory = MemorySaver()

        builder = self._build_graph(
            tool_calling_node=partial(
                tool_calling_llm,
                llm_with_tools=self.llm_with_tools,
            ),
            tools_node=ToolNode(self.tools),
            generate_response_node=partial(
                generate_response,
                response_chain=self.response_chain,
            ),
            tools_condition_fn=tools_condition,
        )

        self.compiled_graph = builder.compile(
            checkpointer=self.memory
        )

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
