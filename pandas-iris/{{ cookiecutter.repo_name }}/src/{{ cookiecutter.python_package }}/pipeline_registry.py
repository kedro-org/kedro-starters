"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline

from {{ cookiecutter.python_package }} import pipeline as mp


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """

    my_pipeline = mp.create_pipeline()

    return {
        "ds": my_pipeline,
        "__default__": my_pipeline,
    }
