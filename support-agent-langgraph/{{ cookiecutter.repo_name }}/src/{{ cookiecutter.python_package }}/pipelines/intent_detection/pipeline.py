from kedro.pipeline import Pipeline, node, pipeline, llm_context_node

from .nodes import (
    create_session,
    detect_intent,
    generate_mermaid_preview,
    get_session_id,
    load_context,
    log_intent_detection,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=create_session,
                inputs="params:user_id",
                outputs="session_table",
                name="create_session_node",
            ),
            node(
                func=get_session_id,
                inputs="session_table",
                outputs="session_id",
                name="get_session_id_node",
            ),
            node(
                func=load_context,
                inputs=[
                    "params:user_id",
                    "user_data",
                    "session_id",
                    "intent_tracer_langfuse",
                ],
                outputs=["user_context", "session_config"],
                name="load_context_node",
            ),
            llm_context_node(
                name="intent_agent_context_node",
                outputs="intent_detection_context",
                llm="llm",
                prompts=[
                    "intent_prompt_langfuse",
                ],
            ),
            node(
                func=detect_intent,
                inputs=["intent_detection_context", "user_context", "session_config"],
                outputs="intent_detection_result",
                name="detect_intent_node",
                preview_fn=generate_mermaid_preview,
            ),
            node(
                func=log_intent_detection,
                inputs=["db_engine", "session_id", "intent_detection_result"],
                outputs=None,
                name="intent_detection_result_node",
            ),
        ]
    )
