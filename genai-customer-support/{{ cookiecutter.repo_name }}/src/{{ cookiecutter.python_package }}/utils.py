from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import json
from typing import Any, TypeVar

from sqlalchemy import Engine, text
from langchain_core.messages import ToolMessage, BaseMessage
from langchain.schema import HumanMessage, AIMessage


@dataclass
class AgentContext:
    """
    Container for all agent runtime dependencies.

    Stores:
    - llm: Language model instance (e.g., ChatOpenAI)
    - tools: Dictionary of callable tools available to the agent
    - prompts: Named prompt templates
    - metadata: Extra runtime metadata for tracing, configs, etc.
    """

    agent_id: str
    llm: Any = None
    tools: dict[str, Any] = field(default_factory=dict)
    prompts: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def add_tool(self, name: str, tool: Any) -> None:
        """Register a tool under the given name."""
        self.tools[name] = tool

    def get_tool(self, name: str) -> Any:
        """Retrieve a tool by name."""
        return self.tools.get(name)

    def add_prompt(self, name: str, prompt: Any) -> None:
        """Register a prompt template under the given name."""
        self.prompts[name] = prompt

    def get_prompt(self, name: str) -> Any:
        """Retrieve a prompt template by name."""
        return self.prompts.get(name)


class KedroAgent(ABC):
    """
    Abstract Kedro agent built on top of LangGraph or similar frameworks.

    Agents encapsulate a flow that:
    - Compiles to a runnable graph
    - Can be invoked with context and configuration
    """

    def __init__(self, context: AgentContext):
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
