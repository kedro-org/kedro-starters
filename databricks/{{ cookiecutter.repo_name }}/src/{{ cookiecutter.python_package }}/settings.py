"""Project settings. There is no need to edit this file unless you want to change values
from the Kedro defaults. For further information, including these default values, see
https://kedro.readthedocs.io/en/stable/kedro_project_setup/settings.html."""
import logging
from pathlib import Path

from kedro.config import TemplatedConfigLoader

logger = logging.getLogger(__name__)

CONF_SOURCE = Path(__file__).parent / "conf"


# Class that enables a dynamic catalog based on runtime parameters
class EnvConfigLoader(TemplatedConfigLoader):
    """_summary_

    Args:
        TemplatedConfigLoader (_type_): _description_
    """

    def __init__(self, *args, **kwargs):
        run_params = kwargs.get("runtime_params", {})
        if run_params:
            env = run_params.get("env", "dev")
        else:
            env = "dev"
        globals_dict = {"env": env}

        logger.info("Global Dict: %s", globals_dict)
        if env == "dev":
            globals_dict.update({"catalog_suffix": "_dev"})
        elif env == "qa":
            globals_dict.update({"catalog_suffix": "_qa"})
        elif env == "prod":
            globals_dict.update({"catalog_suffix": ""})
        else:
            raise RuntimeError("Env must be dev/qa/prod")

        super().__init__(*args, **kwargs, globals_dict=globals_dict)


CONFIG_LOADER_CLASS = EnvConfigLoader  # pylint: disable=invalid-name
CONFIG_LOADER_ARGS = {
    "globals_pattern": "*globals.yml",
}

# Instantiated managed table hooks.
# from {{ cookiecutter.python_package }}.hooks import ManagedTableHooks
# HOOKS = (ManagedTableHooks(),)

# Installed plugins for which to disable hook auto-registration.
# DISABLE_HOOKS_FOR_PLUGINS = ("kedro-viz",)

# Class that manages storing KedroSession data.
# from kedro.framework.session.shelvestore import ShelveStore
# SESSION_STORE_CLASS = ShelveStore
# Keyword arguments to pass to the `SESSION_STORE_CLASS` constructor.
# SESSION_STORE_ARGS = {
#     "path": "./sessions"
# }

# Class that manages Kedro's library components.
# from kedro.framework.context import KedroContext
# CONTEXT_CLASS = KedroContext

# Directory that holds configuration.
# CONF_SOURCE = "conf"
# Class that manages how configuration is loaded.
# CONFIG_LOADER_CLASS = ConfigLoader

# Keyword arguments to pass to the `CONFIG_LOADER_CLASS` constructor.
# CONFIG_LOADER_ARGS = {
#       "config_patterns": {
#           "spark" : ["spark*/"],
#           "parameters": ["parameters*", "parameters*/**", "**/parameters*"],
#       }
# }

# Class that manages the Data Catalog.
# from kedro.io import DataCatalog
# DATA_CATALOG_CLASS = DataCatalog
