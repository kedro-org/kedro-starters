"""
This is a boilerplate pipeline
generated using Kedro {{ cookiecutter.kedro_version }}
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import evaluate_model, split_data, train_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=split_data,
                inputs=["example_iris_data", "params:model_options"],
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="split",
            ),
            node(
                func=train_model,
                inputs=["X_train", "X_test", "y_train"],
                outputs="y_pred",
                name="train",
            ),
            node(
                func=evaluate_model,
                inputs=["y_pred", "y_test"],
                outputs=None,
                name="evaluate_model_node",
            ),
        ]
    )
