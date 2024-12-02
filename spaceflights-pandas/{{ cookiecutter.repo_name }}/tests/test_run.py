"""
This module contains an example test.

Tests should be placed in ``src/tests``, in modules that mirror your
project's structure, and in files named test_*.py. They are simply functions
named ``test_*`` which test a unit of logic.
"""
from pathlib import Path

import pytest
from kedro.config import OmegaConfigLoader
from kedro.framework.context import KedroContext
from kedro.framework.hooks import _create_hook_manager
from kedro.io import DataCatalog


@pytest.fixture
def config_loader():
    return OmegaConfigLoader(
        conf_source=str(Path.cwd() / "conf"),
        base_env="base",
        default_run_env="local"
    )


@pytest.fixture
def hook_manager():
    return _create_hook_manager()


@pytest.fixture
def kedro_context(config_loader, hook_manager):
    return KedroContext(
        package_name="{{ cookiecutter.python_package }}",
        project_path=Path.cwd(),
        env="local",
        config_loader=config_loader,
        hook_manager=hook_manager,
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


class TestKedroContext:
    def test_data_catalog(self, kedro_context):
        # Test if the data catalog is properly loaded within the KedroContext
        catalog = kedro_context.catalog
        assert isinstance(catalog, DataCatalog)

        # Parameters should be loaded into the catalog
        parameters = catalog.load("parameters")
        assert isinstance(parameters, dict)

    def test_project_path(self, kedro_context):
        # Test if the correct project path is set in the KedroContext
        assert kedro_context.project_path == Path.cwd()
