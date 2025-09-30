from datetime import datetime
import logging
from typing import Callable

import pandas as pd
from langchain_core.messages import AIMessage
from sqlalchemy import text, Engine

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .agent import ResponseGenerationAgent
from .tools import build_lookup_docs, build_get_user_claims, build_create_claim
from ...utils import log_message, AgentContext

logger = logging.getLogger(__name__)


def init_tools(
    db_engine: Engine, docs: pd.DataFrame, docs_matches: int
) -> dict[str, Callable]:
    """Assemble all tools used by the response generation agent."""
    return {
        "lookup_docs": build_lookup_docs(docs, docs_matches),
        "get_user_claims": build_get_user_claims(db_engine),
        "create_claim": build_create_claim(db_engine),
    }


def init_response_generation_context(
    llm: ChatOpenAI,
    tool_prompt_txt: str,
    response_system_prompt_txt: str,
    response_user_prompt_txt: str,
    tools: dict[str, Callable],
) -> AgentContext:
    """
    Initialize the AgentContext for response generation.
    - Binds LLM and tools.
    - Attaches tool prompt and response prompt.
    """
    ctx = AgentContext(agent_id="response_generation_agent")
    ctx.llm = llm

    for name, fn in tools.items():
        ctx.add_tool(name, fn)

    tool_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", tool_prompt_txt),
        ]
    )
    response_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", response_system_prompt_txt),
            ("human", response_user_prompt_txt),
        ]
    )

    ctx.add_prompt("tool_prompt", tool_prompt)
    ctx.add_prompt("response_prompt", response_prompt)
    return ctx


def generate_response(
    response_generation_context: AgentContext,
    intent_detection_result: dict,
    user_context: dict,
    session_config: dict,
) -> dict:
    """
    Run the ResponseGenerationAgent to produce a final answer.
    Accepts intent detection result + user context and session config.
    """
    if intent_detection_result["intent"] == "clarification_needed":
        message = "Failed to recognize intent. Please try to describe your problem briefly."
        logger.warning(message)

        result = {
            "messages": [AIMessage(content=message)]
        }

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
            pass

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
