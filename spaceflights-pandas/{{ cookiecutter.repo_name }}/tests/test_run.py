"""
This module contains example tests for a Kedro project.
Tests should be placed in ``src/tests``, in modules that mirror your
project's structure, and in files named test_*.py.
"""
from pathlib import Path

from kedro.framework.session import KedroSession
from kedro.framework.startup import bootstrap_project
from kedro.io import DataCatalog

# The tests below are here for the demonstration purpose
# and should be replaced with the ones testing the project
# functionality

class TestKedroSession:
    def test_config_loader(self):
        bootstrap_project(Path.cwd())

        with KedroSession.create(project_path=Path.cwd()) as session:
            # Test creating a Kedro session and verifying the config loader
            context = session.load_context()
            config_loader = context.config_loader
            assert str(config_loader.conf_source) == str(Path.cwd() / "conf")

            base_params = config_loader.get("parameters", "base")
            assert base_params == {}

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
