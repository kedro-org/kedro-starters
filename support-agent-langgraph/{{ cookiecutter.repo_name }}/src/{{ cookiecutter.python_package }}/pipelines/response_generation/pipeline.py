from kedro.pipeline import Pipeline, node, pipeline, llm_context_node, tool

from .nodes import (
    generate_mermaid_preview,
    generate_response,
    log_response_and_end_session,
)
from .tools import build_lookup_docs, build_get_user_claims, build_create_claim
from ...utils import make_code_preview_fn


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
                preview_fn=make_code_preview_fn(build_get_user_claims, build_lookup_docs, build_create_claim)
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
                preview_fn=generate_mermaid_preview
            ),
            node(
                func=log_response_and_end_session,
                inputs=["db_engine", "session_id", "final_response"],
                outputs=None,
                name="end_session_node",
            ),
        ]
    )
