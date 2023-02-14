# {{ cookiecutter.python_package }}

## Overview

This is a sample Kedro project, which was generated using `Kedro 0.18.4`.

Take a look at the [Kedro documentation](https://kedro.readthedocs.io) for more info on Kedro.

## Rules and guidelines

In order to get the best out of the template:

* Always use virtualenv and poetry to manage your environment and dependencies
* Install the pre-commit hooks to ensure code is linted/tested before committing
* Don't remove any lines from the `.gitignore` file we provide
* Make sure your results can be reproduced by following a [data engineering convention](https://kedro.readthedocs.io/en/stable/faq/faq.html#what-is-data-engineering-convention)
* Don't commit data to your repository
* Don't commit any credentials or your local configuration to your repository. Keep all your credentials and local configuration in `src/<PACKAGE>/conf/local/`

## Managing your local development environment

The local development environment will be managed with `virtualenv` and `poetry`. Make sure to add the following section to your `.gitignore`: 
```
# ignore all local configuration
src/<PACKAGE>/conf/local/**
!src/<PACKAGE>/conf/local/.gitkeep
```

Where `<PACKAGE>` is the name of your package.

### Pre-requisites

Install the version of python you would like to use. Follow the instructions [here](https://www.python.org/downloads/) for your system. Make sure the `python` and `pip` commands are using the right version of python you need for your project. If you would like to have multiple versions of python installed, make sure to use the correct version for your virtual environment.

### Creating the virtualenv

Start by installing virtualenv using `pip install virtualenv`. Once installed create a new virtual environment inside the root folder of your repo: `virtualenv .venv`. This will create a virtualenv with the default version of python you installed virtualenv with.

If you would like to create a virtualenv with a different python version, simply append the path of the python executable you would like to use to the `-p` argument: `virtualenv .venv -p /usr/local/bin/python3.9` for example. Here `/usr/local/bin/python3.9` is the path to python 3.9 on a MacOS machine, but it can be a Windows path for Windows setups as well.

### Activating the virtual environment

Install poetry: `pip install poetry`. To activate the virtual environment run `poetry shell`. Depending on your IDE, you can add the poetry environment or it will be picked up automatically.

### Adding Dependencies

Poetry allows you to add dependencies in groups, keeping development dependencies outside package dependencies. To add a package dependency: `poetry add <package>`. Any dependency added to the base will be included in the package, all others will be optional.

To add a dependency to a specific group, say `dev`, run: `poetry add <package> --group dev`.

You can also modify the `pyproject.toml` file directly but always be sure to run a `poetry lock` right after to ensure the `poetry.lock` file is up to date.

## How to run your Kedro pipeline

You can run your Kedro project with:

```
kedro run
```

## How to test your Kedro project

Have a look at the file `src/tests/test_run.py` for instructions on how to write your tests. You can run your tests as follows:

```
poetry run pytest
```

## How to work with Kedro and notebooks

> Note: Using `kedro jupyter` or `kedro ipython` to run your notebook provides these variables in scope: `context`, `catalog`, and `startup_error`.
>
> Jupyter, JupyterLab, and IPython are already included in the project requirements by default, so once you have run `poetry install` you will not need to take any extra steps before you use them.

### Jupyter
To use Jupyter notebooks in your Kedro project, you need to install Jupyter (included in the pyproject.toml).

After installing Jupyter, you can start a local notebook server:

```
kedro jupyter notebook
```

### JupyterLab
To use JupyterLab, you need to install it (included in the pyproject.toml).

You can also start JupyterLab:

```
kedro jupyter lab
```

### IPython
And if you want to run an IPython session:

```
kedro ipython
```

### How to convert notebook cells to nodes in a Kedro project
You can move notebook code over into a Kedro project structure using a mixture of [cell tagging](https://jupyter-notebook.readthedocs.io/en/stable/changelog.html#release-5-0-0) and Kedro CLI commands.

By adding the `node` tag to a cell and running the command below, the cell's source code will be copied over to a Python file within `src/<package_name>/nodes/`:

```
kedro jupyter convert <filepath_to_my_notebook>
```
> *Note:* The name of the Python file matches the name of the original notebook.

Alternatively, you may want to transform all your notebooks in one go. Run the following command to convert all notebook files found in the project root directory and under any of its sub-folders:

```
kedro jupyter convert --all
```

### How to ignore notebook output cells in `git`
To automatically strip out all output cell contents before committing to `git`, you can run `kedro activate-nbstripout`. This will add a hook in `.git/config` which will run `nbstripout` before anything is committed to `git`.

> *Note:* Your output cells will be retained locally.

## Package your Kedro project

To package your project into a wheel file, run `poetry build` from the root directory of the folder. Notice how the `conf` is stored inside the package itself. This is different from the default kedro configuration and requires the following changes.

### Modify settings.py

Add the following to `settings.py`

``` python
from pathlib import Path
CONF_SOURCE = Path(__file__).parent / "conf"
```

### Modify pyproject.toml

Make sure the following lines are accurate in `pyproject.toml`

``` toml
packages = [
    { include = "<PACKAGE NAME>", from = "src" },
]
include = ["src/<PACKAGE NAME>/conf/**/.gitkeep"]
exclude = ["src/<PACKAGE NAME>/conf/local/*.yml"]
```

Where `<PACKAGE NAME>` is the name of your package, in this case `poetry-spaceflights`.

### Creating a wheel

Run `poetry build` and a wheel file should get created with your code inside the `dist/` folder. This folder is already in the `.gitignore` so no need to worry about deleting it after.

## Running a Packaged Pipeline in Databricks

To run a packaged kedro pipeline in databricks:

Create a job with python script type and upload the `run_kedro_pipeline.py` to databricks. Add the wheel file as a dependency for the job. In the parameters of the job specify the following:
`--package {{ cookiecutter.python_package }} --pipeline spaceflight --params env:dev`