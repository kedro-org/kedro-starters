from kedro.pipeline import llm_context_node, node, pipeline, Pipeline, tool

from .nodes import (
    generate_response,
    log_response_and_end_session,
)
from .tools import build_create_claim, build_get_user_claims, build_lookup_docs


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            llm_context_node(
                name="response_agent_context_node",
                outputs="response_generation_context",
                llm="llm",
                prompts=["tool_prompt", "response_prompt"],
                tools=[
                    tool(build_get_user_claims, "db_engine"),
                    tool(build_lookup_docs, "docs", "params:docs_matches"),
                    tool(build_create_claim, "db_engine"),
                ],
            ),
            node(
                func=generate_response,
                inputs=[
                    "response_generation_context",
                    "intent_detection_result",
                    "user_context",
                    "session_config",
                ],
                outputs="final_response",
                name="generate_response_node",
            ),
            node(
                func=log_response_and_end_session,
                inputs=["db_engine", "session_id", "final_response"],
                outputs=None,
                name="end_session_node",
            ),
        ]
    )
