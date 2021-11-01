

"""Example data science pipeline using PySpark.
"""

from kedro.pipeline import Pipeline, node

from .nodes import predict, report_accuracy, train_model


def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                train_model,
                inputs=["training_data", "parameters"],
                outputs="example_classifier",
            ),
            node(
                predict,
                inputs=dict(model="example_classifier", testing_data="testing_data"),
                outputs="example_predictions",
            ),
            node(report_accuracy, ["example_predictions"], None),
        ]
    )
