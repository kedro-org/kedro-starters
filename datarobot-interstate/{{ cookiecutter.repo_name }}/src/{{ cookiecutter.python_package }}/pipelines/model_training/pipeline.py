from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from .nodes import train_models

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=train_models,
                inputs=["training_data", "parameters"],
                outputs="dr_projects",
                name="train_models",
            ),
        ],
    )
