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
                inputs=["example_iris_data", "params:model_options"],
                outputs=["X_train@pyspark", "X_test@pyspark", "y_train@pyspark", "y_test@pyspark"],
                name="split",
            ),
            node(
                func=make_predictions,
                inputs=["X_train@pandas", "X_test@pandas", "y_train@pandas"],
                outputs="y_pred",
                name="make_predictions",
            ),
            node(
                func=report_accuracy,
                inputs=["y_pred", "y_test@pandas"],
                outputs=None,
                name="report_accuracy",
            ),
        ]
    )
