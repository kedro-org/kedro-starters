"""
This is a boilerplate pipeline
generated using Kedro {{ cookiecutter.kedro_version }}
"""

from kedro.pipeline import Node, Pipeline

from .nodes import make_predictions, report_accuracy, split_data


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            Node(
                func=split_data,
                inputs=["example_iris_data", "parameters"],
                outputs=[
                    "X_train@pyspark",
                    "X_test@pyspark",
                    "y_train@pyspark",
                    "y_test@pyspark",
                ],
                name="split",
            ),
            Node(
                func=make_predictions,
                inputs=["X_train@pandas", "X_test@pandas", "y_train@pandas"],
                outputs="y_pred",
                name="make_predictions",
            ),
            Node(
                func=report_accuracy,
                inputs=["y_pred", "y_test@pandas"],
                outputs=None,
                name="report_accuracy",
            ),
        ]
    )
