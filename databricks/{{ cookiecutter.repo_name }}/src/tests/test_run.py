"""
This module contains an example test.

Tests should be placed in ``src/tests``, in modules that mirror your
project's structure, and in files named test_*.py. They are simply functions
named ``test_*`` which test a unit of logic.

To run the tests, run ``kedro test`` from the project root directory.
"""

from pathlib import Path

import pytest
from kedro.config import ConfigLoader
from kedro.framework.context import KedroContext
from kedro.framework.hooks import _create_hook_manager
from kedro.framework.project import settings


@pytest.fixture
def config_loader():
    """_summary_

    Returns:
        _type_: _description_
    """
    return ConfigLoader(conf_source=str(Path.cwd() / settings.CONF_SOURCE))


@pytest.fixture
def project_context(cfg_loader=config_loader):
    """_summary_

    Args:
        config_loader (_type_): _description_

    Returns:
        _type_: _description_
    """
    return KedroContext(
        package_name="{{ cookiecutter.python_package }}",
        project_path=Path.cwd(),
        config_loader=cfg_loader,
        hook_manager=_create_hook_manager(),
    )
