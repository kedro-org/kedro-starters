from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    generate_response,
    init_tools,
    init_response_generation_context,
    log_response_and_end_session,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=init_tools,
                inputs=["db_engine", "docs", "params:docs_matches"],
                outputs="tools",
                name="init_tools_node",
            ),
            node(
                func=init_response_generation_context,
                inputs=[
                    "llm",
                    "tool_prompt",
                    "response_prompt",
                    "tools",
                ],
                outputs="response_generation_context",
                name="init_response_generation_context_node",
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
