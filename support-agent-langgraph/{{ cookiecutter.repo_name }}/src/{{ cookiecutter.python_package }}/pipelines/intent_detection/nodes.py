import logging
from typing import Any

from kedro.pipeline import LLMContext
from kedro.pipeline.preview_contract import MermaidPreview
from langfuse.langchain import CallbackHandler
from langchain_core.messages import HumanMessage, AIMessage
import pandas as pd
import questionary
from sqlalchemy import Engine

from .agent import IntentDetectionAgent
from ...utils import log_message

logger = logging.getLogger(__name__)


def generate_mermaid_preview() -> MermaidPreview:
    """
    Generate a styled Mermaid diagram preview of the response-generation graph.

    This function compiles the agent’s static, non-executable graph definition
    and renders it as a Mermaid diagram for visualization purposes only.

    The preview is guaranteed to reflect the same graph structure used at
    runtime, while avoiding any dependency on LLMs, tools, or memory.

    Returns:
        MermaidPreview containing the rendered diagram and Mermaid theme
        configuration metadata.
    """
    compiled = IntentDetectionAgent.graph().compile()
    mermaid = compiled.get_graph().draw_mermaid()
    mermaid = mermaid.replace(
        "classDef first fill-opacity:0",
        "classDef first fill:#50C878,color:#000000",
    )
    config = {
        "themeVariables": {
            "lineColor": "#F5A623",
            "nodeTextColor": "#000000",
        },
    }
    return MermaidPreview(content=mermaid, meta=config)


def create_session(user_id: int) -> pd.DataFrame:
    """
    Create a new user session entry.

    Args:
        user_id: ID of the active user.

    Returns:
        DataFrame containing the new session entry.
    """
    return pd.DataFrame({"user_id": [user_id]})


def get_session_id(session_table: pd.DataFrame) -> int:
    """
    Extract the latest session ID from the session table.

    Args:
        session_table: DataFrame of sessions.

    Returns:
        Latest session ID.
    """
    session_id = int(session_table.iloc[-1]["id"])
    started_at = pd.to_datetime(session_table.iloc[-1]["started_at"])
    logger.info(
        "Session session_id %s created at started_at %s", session_id, started_at
    )
    return session_id


def load_context(
    user_id: int,
    user_data: pd.DataFrame,
    session_id: int,
    intent_tracer_langfuse: CallbackHandler,
):
    """
    Build user context and tracing configuration for LangChain.

    Args:
        user_id: Active user ID.
        user_data: DataFrame containing user profile info.
        session_id: Current session ID.
        intent_tracer_langfuse: Langfuse tracer dataset for callback handling.

    Returns:
        Tuple of (user_context, session_config).
    """
    user_context = {"profile": {"user_id": user_id, "name": user_data.at[0, "name"]}}
    session_config = {
        "configurable": {"thread_id": str(session_id)},
        "callbacks": [intent_tracer_langfuse],
    }

    # Example alternative using Opik
    # session_config = {
    #     "configurable": {"thread_id": str(session_id)},
    #     "callbacks": [intent_tracer_opik]
    # }

    return user_context, session_config


def detect_intent(
    intent_detection_context: LLMContext,
    user_context: dict,
    session_config: dict,
    clarification_attempts: int = 2,
) -> dict[str, Any]:
    """
    Run interactive intent detection with clarification fallback.

    Args:
        intent_detection_context: Configured AgentContext for detection.
        user_context: Dictionary of user profile/context data.
        session_config: LLM session configuration (thread + callbacks).
        clarification_attempts: Number of clarification retries allowed.

    Returns:
        Intent detection result dictionary.
    """
    agent = IntentDetectionAgent(context=intent_detection_context)
    agent.compile()

    # Initial greeting
    greeting_message = (
        f"Hi {user_context['profile']['name']}! 👋 How can I help you today?\n"
        f"You can ask me a question, open a new claim, or follow up on the existing one."
    )
    human_input = questionary.text(greeting_message).ask()

    context = {
        "messages": [
            AIMessage(content=greeting_message),
            HumanMessage(content=human_input),
        ],
        "user_context": user_context,
    }
    result = agent.invoke(context, session_config)

    # Retry clarification loop
    while result["intent"] == "clarification_needed":
        if not clarification_attempts:
            break

        human_clarification = questionary.text(result["messages"][-2].content).ask()
        context = {
            "messages": result["messages"]
            + [HumanMessage(content=human_clarification)],
            "user_context": user_context,
        }
        result = agent.invoke(context, session_config)
        clarification_attempts -= 1

    # Print conversation
    for m in result["messages"]:
        m.pretty_print()

    return result


def log_intent_detection(
    db_engine: Engine, session_id: int, intent_detection_result: dict
):
    """
    Persist intent detection conversation messages to the database.

    Args:
        db_engine: Active SQLAlchemy engine.
        session_id: Current session ID.
        intent_detection_result: Result dict from intent detection agent.
    """
    for m in intent_detection_result["messages"]:
        log_message(db_engine, session_id, m)
