from kedro.pipeline import Pipeline, node
from kedro.pipeline.modular_pipeline import pipeline

from .nodes import deploy_models


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=deploy_models,
                inputs=["dr_models", "parameters"],
                outputs="dr_deployments",
                name="deploy_models",
            ),
        ],
    )
