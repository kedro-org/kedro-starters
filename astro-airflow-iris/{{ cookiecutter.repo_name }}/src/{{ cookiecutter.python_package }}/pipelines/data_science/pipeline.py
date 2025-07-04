"""Example code for the nodes in the example pipeline. This code is meant
just for illustrating basic Kedro features.

Delete this when you start working on your own Kedro project.
"""

from kedro.pipeline import Node, Pipeline

from .nodes import predict, report_accuracy, train_model


def create_pipeline(**kwargs):
    return Pipeline(
        [
            Node(
                train_model,
                ["example_train_x", "example_train_y", "parameters"],
                "example_model",
                name="train",
            ),
            Node(
                predict,
                dict(model="example_model", test_x="example_test_x"),
                "example_predictions",
                name="predict",
            ),
            Node(
                report_accuracy,
                ["example_predictions", "example_test_y"],
                None,
                name="report",
            ),
        ]
    )
