from abc import ABC, abstractmethod
import json
import inspect
import textwrap
from typing import Any, Callable

from kedro.pipeline import LLMContext
from kedro.pipeline.preview_contract import TextPreview
from langchain_core.messages import ToolMessage, BaseMessage
from langchain.schema import HumanMessage, AIMessage
from sqlalchemy import Engine, text


class KedroAgent(ABC):
    """
    Abstract Kedro agent built on top of LangGraph or similar frameworks.

    Agents encapsulate a flow that:
    - Compiles to a runnable graph
    - Can be invoked with context and configuration
    """

    def __init__(self, context: LLMContext):
        self.context = context

    @abstractmethod
    def compile(self) -> None:
        """Build and compile the agent’s flow into a runnable graph."""

    @abstractmethod
    def invoke(self, context: dict, config: dict | None = None) -> Any:
        """Run the compiled graph with given state and config."""


def log_message(
    db_engine: Engine, session_id: int, message: BaseMessage | dict
) -> None:
    """
    Persist an agent message into the `message` table.

    Args:
        db_engine: SQLAlchemy engine
        session_id: Active session ID
        message:
            - LangChain message object (HumanMessage, AIMessage, ToolMessage)
            - or dict with {"sender", "content", ...}
    """
    if isinstance(message, dict):
        sender = message.get("sender", "assistant")
        content = message
    else:
        if isinstance(message, HumanMessage):
            sender = "user"
        elif isinstance(message, AIMessage):
            sender = "assistant"
        elif isinstance(message, ToolMessage):
            sender = "tool"
        else:
            sender = "assistant"  # fallback

        # Store the full message payload (tool calls, metadata, etc.)
        content = message.model_dump()

    query = text("""
        INSERT INTO message (session_id, sender, content)
        VALUES (:session_id, :sender, :content)
    """)

    with db_engine.begin() as conn:
        conn.execute(
            query,
            {
                "session_id": session_id,
                "sender": sender,
                "content": json.dumps(content, default=str),  # ensure JSON serializable
            },
        )


def make_code_preview_fn(*funcs: Callable):
    """Create a preview function with captured callable context."""
    def preview_fn() -> TextPreview:
        sources: list[str] = []

        for func in funcs:
            try:
                source = inspect.getsource(func)
                source = textwrap.dedent(source)
            except (OSError, TypeError):
                name = getattr(func, "__qualname__", repr(func))
                source = f"# Source unavailable for {name}"

            sources.append(source)

        return TextPreview(
            content="\n\n".join(sources),
            meta={"language": "python"},
        )

    return preview_fn
