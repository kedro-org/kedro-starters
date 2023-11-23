from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from .nodes import select_models


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=select_models,
                inputs="dr_projects",
                outputs="dr_models",
                name="select_models",
            ),
        ],
        tags=["datarobot"],
    )
