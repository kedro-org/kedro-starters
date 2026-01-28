"""
Intent-classification agent built with LangGraph, routing between detection,
clarification, and context-update steps. Extend this module when adding new
intents or changing how user queries are resolved.
"""

from functools import partial
from typing import Any, TypedDict, Literal

from kedro.pipeline import LLMContext
from langchain_core.messages import AnyMessage, AIMessage
from langchain_core.runnables import Runnable
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph
from pydantic import BaseModel

from ...utils import KedroAgent


class IntentOutput(BaseModel):
    """
    Schema for intent classification results.

    Attributes:
        intent: Predicted intent label.
        reason: Explanation for why this intent was chosen.
    """

    intent: Literal[
        "general_question",
        "claim_new",
        "existing_claim_question",
        "clarification_needed",
    ]
    reason: str


class AgentState(TypedDict):
    """
    Shared state passed across nodes in the intent detection graph.

    Keys:
        messages: Conversation history so far.
        intent: Current intent classification.
        reason: Explanation for the intent classification.
        user_context: User-specific context (profile, claims, etc.).
    """

    messages: list[AnyMessage]
    intent: str
    reason: str
    user_context: dict


class IntentDetectionAgent(KedroAgent):
    """
    Agent that classifies user queries into intents.

    Flow:
        1. detect_intent → classify the user query.
        2. clarify_intent → ask for clarification if ambiguous.
        3. update_context → append classification result to messages.

    Uses LangGraph with memory checkpointing.
    """

    def __init__(self, context: LLMContext):
        super().__init__(context)
        self.compiled_graph: CompiledStateGraph | None = None
        self.memory: MemorySaver | None = None

        # LLM bound to structured intent output
        structured_llm = self.context.llm.with_structured_output(IntentOutput)
        self.intent_chain = (
            self.context.prompts["intent_prompt_langfuse"]
            | structured_llm
        )

    @staticmethod
    def _build_graph(
        *,
        detect_intent_node,
        clarify_intent_node,
        update_context_node,
        routing_fn,
    ) -> StateGraph:
        """
        Construct the intent-detection state graph with injected node behavior.

        This method defines the static topology of the agent graph:
        - node names
        - execution order
        - conditional routing

        Node behavior is injected, allowing reuse for:
          - runtime execution
          - static preview / visualization
        """
        builder = StateGraph(AgentState)

        builder.add_node("detect_intent", detect_intent_node)
        builder.add_node("clarify_intent", clarify_intent_node)
        builder.add_node("update_context", update_context_node)

        builder.add_edge(START, "detect_intent")

        builder.add_conditional_edges(
            "detect_intent",
            routing_fn,
            {
                "clarify_intent": "clarify_intent",
                "update_context": "update_context",
            },
        )

        builder.add_edge("clarify_intent", "update_context")
        builder.add_edge("update_context", END)

        return builder

    @staticmethod
    def graph() -> StateGraph:
        """
        Create a static, non-executable version of the intent-detection graph.

        Intended for:
          - Mermaid diagram rendering
          - Documentation
          - Architecture inspection
        """
        return IntentDetectionAgent._build_graph(
            detect_intent_node=lambda x: x,
            clarify_intent_node=lambda x: x,
            update_context_node=lambda x: x,
            routing_fn=lambda _: "update_context",
        )

    def compile(self) -> None:
        """
        Compile the executable intent-detection graph with runtime dependencies.
        """
        self.memory = MemorySaver()

        builder = self._build_graph(
            detect_intent_node=partial(
                detect_intent,
                llm=self.intent_chain,
            ),
            clarify_intent_node=clarify_intent,
            update_context_node=update_context,
            routing_fn=self._route_by_intent,
        )

        self.compiled_graph = builder.compile(
            checkpointer=self.memory
        )

    @staticmethod
    def _route_by_intent(state: AgentState) -> str:
        return (
            "clarify_intent"
            if state.get("intent") == "clarification_needed"
            else "update_context"
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


def detect_intent(state: AgentState, llm: Runnable) -> dict:
    """Classify the latest user message into an intent."""
    query = state["messages"][-1].content
    result: IntentOutput = llm.invoke(query)

    return {
        "intent": result.intent,
        "reason": result.reason,
        "messages": state["messages"],
    }


def update_context(state: AgentState) -> dict:
    """Append intent classification result to the conversation messages."""
    return {
        "messages": state["messages"]
        + [
            AIMessage(
                content=f"Intent classified: {state['intent']}\nReason: {state['reason']}"
            )
        ]
    }


def clarify_intent(state: AgentState) -> dict:
    """Ask the user for clarification if the intent is ambiguous."""
    return {
        "messages": state["messages"]
        + [
            AIMessage(
                content="Could you clarify if this is a new claim, an existing "
                "claim, or a general question?"
            )
        ]
    }
