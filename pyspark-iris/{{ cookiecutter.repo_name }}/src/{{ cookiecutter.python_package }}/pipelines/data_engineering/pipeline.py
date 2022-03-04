"""Example data engineering pipeline with PySpark.
"""

from kedro.pipeline import node, pipeline

from .nodes import split_data, transform_features


def create_pipeline(**kwargs):
    return pipeline(
        [
            node(
                transform_features,
                inputs="example_iris_data",
                outputs="transformed_data",
            ),
            node(
                split_data,
                inputs=["transformed_data", "params:example_test_data_ratio"],
                outputs=["training_data", "testing_data"],
            ),
        ]
    )
