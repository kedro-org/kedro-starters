from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from .nodes import predict


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=predict,
                inputs=["training_data", "dr_deployments"],
                outputs="predictions",
                name="predict",
            ),
            node(
                func=predict,
                inputs=["testing_data", "dr_deployments"],
                outputs="predictions_out_of_sample",
                name="predict_out_of_sample",
            ),
        ],
    )
