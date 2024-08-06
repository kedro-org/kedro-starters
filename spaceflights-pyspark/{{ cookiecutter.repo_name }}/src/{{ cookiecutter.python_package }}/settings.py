"""Project settings. There is no need to edit this file unless you want to change values
from the Kedro defaults. For further information, including these default values, see
https://docs.kedro.org/en/stable/kedro_project_setup/settings.html."""

# Instantiated project hooks.
from {{cookiecutter.python_package}}.hooks import SparkHooks  # noqa: E402

# Hooks are executed in a Last-In-First-Out (LIFO) order.
HOOKS = (SparkHooks(),)

# Installed plugins for which to disable hook auto-registration.
# DISABLE_HOOKS_FOR_PLUGINS = ("kedro-viz",)

# Class that manages storing KedroSession data.
# from kedro.framework.session.store import BaseSessionStore
# SESSION_STORE_CLASS = BaseSessionStore

# Setup for Experiment Tracking
# The SQLite DB required for experiment tracking is stored by default
# (supported from python >= 3.9 and Kedro-Viz 9.2.0) in the .viz folder
# of your project. To store it in another directory, provide the
# keyword argument `SESSION_STORE_ARGS`.
# SESSION_STORE_ARGS = {"path": str(Path(__file__).parents[2] / ".viz")}

# Directory that holds configuration.
# CONF_SOURCE = "conf"

# Class that manages how configuration is loaded.
from kedro.config import OmegaConfigLoader  # noqa: E402

CONFIG_LOADER_CLASS = OmegaConfigLoader
# Keyword arguments to pass to the `CONFIG_LOADER_CLASS` constructor.
CONFIG_LOADER_ARGS = {
    "base_env": "base",
    "default_run_env": "local",
    "config_patterns": {
        "spark": ["spark*", "spark*/**"],
    }
}

# Class that manages Kedro's library components.
# from kedro.framework.context import KedroContext
# CONTEXT_CLASS = KedroContext

# Class that manages the Data Catalog.
# from kedro.io import DataCatalog
# DATA_CATALOG_CLASS = DataCatalog
