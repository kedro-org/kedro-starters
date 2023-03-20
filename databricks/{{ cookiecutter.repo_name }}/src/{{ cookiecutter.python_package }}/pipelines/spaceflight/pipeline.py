"""
This is a boilerplate pipeline 'spaceflight'
generated using Kedro 0.18.4
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import generate_features, generate_predictions


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(lambda x: x, "iris_csv", "iris_bronze", name="raw_to_bronze"),
            node(generate_features, "iris_bronze", "iris_features", name="features"),
            node(generate_predictions, "iris_features", "iris_predictions"),
        ]
    )
