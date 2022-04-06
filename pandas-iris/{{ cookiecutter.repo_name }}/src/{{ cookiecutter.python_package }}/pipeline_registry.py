"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline, pipeline

from {{ cookiecutter.python_package }}.pipelines import data_science as ds

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """

    data_science_pipeline = ds.create_pipeline()

    return {
        "ds": data_science_pipeline,
        "__default__": data_science_pipeline,
    }
