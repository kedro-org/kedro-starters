from typing import Dict
from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline


def register_pipelines() -> Dict[str, Pipeline]:
    pipelines = find_pipelines()

    return {
        "__default__": sum(pipelines.values()),
        "data_processing": pipelines["data_processing"],
        "model_training": pipelines["model_training"],
        "model_selection": pipelines["model_selection"],
        "model_deployment": pipelines["model_deployment"],
        "model_prediction": pipelines["model_prediction"],
    }
