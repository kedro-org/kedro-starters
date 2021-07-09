"""
{{ cookiecutter.repo_name }}

Listing python packages from pypi, and finding available single word packages.


## Run the Pipeline at the command line

``` bash
# Run with existing package data
python {{ cookiecutter.repo_name }}.py

# Full run
python {{ cookiecutter.repo_name }}.py --full
```

## Run the Pipeline with a python repl

``` python
from {{ cookiecutter.python_package }} import run_project

run_project()  # run local datasets only
run_project(full=True)  # run full pipeline including network requests
```

"""
import logging
from typing import List, Optional

from kedro.extras.datasets.pickle.pickle_dataset import PickleDataSet
from kedro.io import DataCatalog
from kedro.pipeline import Pipeline, node
from kedro.runner.sequential_runner import SequentialRunner

logger = logging.getLogger(__name__)

__version__ = "0.1.0"

pipeline = Pipeline(
    nodes=[
        # your nodes go here
        node(lambda range: range(10), None, 'range')
   ]
)

default_entries = {
    name: PickleDataSet(filepath=f"data/{name}.pkl") for name in pipeline.all_outputs()
}

catalog = DataCatalog(
    {
        **default_entries,
        # override default entries here
    }
)

runner = SequentialRunner()


def run_project(full: Optional[bool] = None):
    """
    Run the project.

    Parameters
    --------
    full : bool
        runs the full pipeline if True
        skips network calls if False
        checks sys.arv for --full if None

    Returns
    --------
    None

    Examples
    --------
    >>> from {{ cookiecutter.python_package }} import run_project
    >>> run_project() # run local datasets only
    >>> run_project(full=True) # run full pipeline including network requests

    """
    import sys

    if "--full" in sys.argv and full is None:
        full = True

    if full:
        runner.run(pipeline, catalog)

    else:
        runner.run(
            Pipeline([node for node in pipeline.nodes if "raw" not in node.name]),
            catalog,
        )


if __name__ == "__main__":
    run_project()
