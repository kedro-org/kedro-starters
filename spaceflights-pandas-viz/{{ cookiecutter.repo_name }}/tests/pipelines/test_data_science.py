import pandas as pd
import pytest
from kedro.io import DataCatalog, MemoryDataset
from kedro.runner import SequentialRunner
from {{ cookiecutter.python_package }}.pipelines.data_science import create_pipeline
from {{ cookiecutter.python_package }}.pipelines.data_science.nodes import split_data


@pytest.fixture
def dummy_data():
    return pd.DataFrame(
        {"engines": [1, 2, 3],
         "crew": [4, 5, 6],
         "passenger_capacity": [5, 6, 7],
         "price": [120, 290, 30]})

@pytest.fixture
def dummy_parameters():
    parameters = {"model_options":
                     {"test_size": 0.2,
                      "random_state": 3,
                      "features": ["engines", "passenger_capacity", "crew"]}
                 }
    return parameters

class TestDataScienceNodes:
    def test_split_data(self, dummy_data, dummy_parameters):
        X_train, X_test, y_train, y_test = split_data(dummy_data, dummy_parameters["model_options"])
        assert len(X_train) == 2  # noqa: PLR2004
        assert len(y_train) == 2  # noqa: PLR2004
        assert len(X_test) == 1
        assert len(y_test) == 1

class TestDataSciencePipeline:
    def test_data_science_pipeline(self, dummy_data, dummy_parameters):
        pipeline = create_pipeline().from_nodes("split_data_node").to_nodes("evaluate_model_node")
        catalog = DataCatalog()
        catalog.add("model_input_table", MemoryDataset(dummy_data))
        catalog.add_feed_dict({"params:model_options" : dummy_parameters["model_options"]})

        output = SequentialRunner().run(pipeline, catalog)
        assert len(output) == 0
