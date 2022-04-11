"""
This is a boilerplate pipeline
generated using Kedro {{ cookiecutter.kedro_version }}
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import make_predictions, report_accuracy, split_data


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=split_data,
                inputs=["example_iris_data", "parameters"],
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="split",
            ),
            node(
                func=make_predictions,
                inputs=["X_train", "X_test", "y_train"],
                outputs="y_pred",
                name="make_predictions",
            ),
            node(
                func=report_accuracy,
                inputs=["y_pred", "y_test"],
                outputs=None,
                name="report_accuracy",
            ),
        ]
    )
