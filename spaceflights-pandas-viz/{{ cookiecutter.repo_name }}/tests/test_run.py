"""
This module contains example tests for a Kedro project.
Tests should be placed in ``src/tests``, in modules that mirror your
project's structure, and in files named test_*.py.
"""
from pathlib import Path

import pytest
from kedro.config import OmegaConfigLoader
from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
from kedro.io import DataCatalog


@pytest.fixture
def config_loader():
    return OmegaConfigLoader(
        conf_source=str(Path.cwd() / "conf"),
        base_env="base",
        default_run_env="local"
    )


# The tests below are here for the demonstration purpose
# and should be replaced with the ones testing the project
# functionality

class TestConfigLoader:
    def test_config_loader(self, config_loader):
        # Test if the config loader is correctly utilizing the files in the conf directory
        assert str(config_loader.conf_source) == str(Path.cwd() / "conf")
        assert config_loader.base_env == "base"
        assert config_loader.default_run_env == "local"

    def test_load_base_parameters(self, config_loader):
        # Test if parameters.yml is being loaded, file is expected to be empty
        base_params = config_loader.get("parameters", "base")
        assert base_params == {}


class TestKedroSession:
    def test_session_data_catalog(self):
        bootstrap_project(Path.cwd())

        # Test creating a Kedro session and verifying its data catalog
        with KedroSession.create(project_path=Path.cwd()) as session:
            context = session.load_context()
            catalog = context.catalog
            assert isinstance(catalog, DataCatalog)

            # Test if parameters can be loaded
            parameters = catalog.load("parameters")
            assert isinstance(parameters, dict)

    def test_project_path(self):
        bootstrap_project(Path.cwd())
        with KedroSession.create(project_path=Path.cwd()) as session:
            assert session._project_path == Path.cwd()
