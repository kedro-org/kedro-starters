# implement hook to provdie datarobot token and client
from kedro.framework.hooks import hook_impl
from kedro.config import OmegaConfigLoader

# pyright: reportPrivateImportUsage=false
import datarobot as dr
from kedro.framework.context import KedroContext
from kedro.framework.project import settings
import logging
import urllib3.exceptions

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class DataRobotHook:
    def __init__(self):
        pass

    @hook_impl
    def after_context_created(self, context: KedroContext):
        """
        Hook implementation to set up DataRobot client before the node is run.
        """
        conf_path = str(context.project_path / settings.CONF_SOURCE)
        conf_loader = OmegaConfigLoader(conf_source=conf_path, env="local")
        self.credentials = conf_loader["credentials"]["datarobot"]

        logging.info(
            f"Initializing DataRobot client on endpoint {self.credentials['endpoint']}"
        )
        _ = dr.Client(
            token=self.credentials["token"],
            endpoint=self.credentials["endpoint"],
            ssl_verify=False,
        )
