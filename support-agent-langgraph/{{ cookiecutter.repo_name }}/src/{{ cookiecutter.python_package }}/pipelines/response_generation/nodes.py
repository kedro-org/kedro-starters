from datetime import datetime
import logging

from kedro.pipeline import LLMContext
from kedro.pipeline.preview_contract import MermaidPreview

from langchain_core.messages import AIMessage
from sqlalchemy import text, Engine

from .agent import ResponseGenerationAgent
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
    compiled = ResponseGenerationAgent.graph().compile()
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



def generate_response(
    response_generation_context: LLMContext,
    intent_detection_result: dict,
    user_context: dict,
    session_config: dict,
) -> dict:
    """
    Run the ResponseGenerationAgent to produce a final answer.
    Accepts intent detection result + user context and session config.
    """
    if intent_detection_result["intent"] == "clarification_needed":
        message = (
            "Failed to recognize intent. Please try to describe your problem briefly."
        )
        logger.warning(message)

        result = {"messages": [AIMessage(content=message)]}

    else:
        agent = ResponseGenerationAgent(context=response_generation_context)
        agent.compile()

        context = {
            "messages": [],
            "intent": intent_detection_result["intent"],
            "intent_generator_summary": intent_detection_result["reason"],
            "user_context": user_context,
        }

        result = agent.invoke(context, session_config)

    for m in result["messages"]:
        try:
            m.pretty_print()
        except Exception:
            logger.warning("Failed to pretty_print message %r", m)

    return result


def log_response_and_end_session(
    db_engine: Engine, session_id: int, final_response: dict
):
    """Log all messages and mark the session as ended."""
    for m in final_response["messages"]:
        log_message(db_engine, session_id, m)

    ended_at = datetime.utcnow()
    query = text("""
        UPDATE session
        SET ended_at = :ended_at
        WHERE id = :session_id
    """)
    with db_engine.begin() as conn:
        conn.execute(query, {"ended_at": ended_at, "session_id": session_id})

    logger.info("Session session_id %s ended at ended_at %s", session_id, ended_at)
