from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from .nodes import segment_data, split_data, extract_data


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=extract_data,
                inputs=["web_data_request"],
                outputs="traffic_volume_data",
                name="extract_data",
            ),
            node(
                func=segment_data,
                inputs=["traffic_volume_data", "parameters"],
                outputs="segmented_data",
                name="segment_data",
            ),
            node(
                func=split_data,
                inputs=["segmented_data", "parameters"],
                outputs=["training_data", "testing_data"],
                name="split_data",
            ),
        ],
        namespace="data_processing",
        inputs={"web_data_request"},
        outputs={"training_data", "testing_data", "traffic_volume_data"},
    )
