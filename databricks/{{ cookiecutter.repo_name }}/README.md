# {{ cookiecutter.python_package }}

## Overview

This is a sample Kedro project for Databricks, which was generated using `Kedro {{ cookiecutter.kedro_version }}`.

Take a look at the [Kedro documentation](https://kedro.readthedocs.io) for more info on Kedro.

## Rules and guidelines

In order to get the best out of the template:

* Use virtualenv and poetry to manage your environment and dependencies respectivelt (you can still use setup.py and requirements.txt)
* Install the pre-commit hooks to ensure code is linted/tested before committing (depends on poetry)
* Don't remove any lines from the `.gitignore` file we provide
* Make sure your results can be reproduced by following a [data engineering convention](https://kedro.readthedocs.io/en/stable/faq/faq.html#what-is-data-engineering-convention)
* Don't commit data to your repository
* Don't commit any credentials or your local configuration to your repository. Keep all your credentials and local configuration in `conf/local/`


## Managing your local development environment

This section will cover how to manage your local development enviroment using:

For the virtual enviroment:
1. `virtualenv`
2. `conda`

For dependencies:

1. `poetry`
2. `setup.py/requirements.txt`

### Pre-requisites

Install the version of python you would like to use. Follow the instructions [here](https://www.python.org/downloads/) for your system. Make sure the `python` and `pip` commands are using the right version of python you need for your project. If you would like to have multiple versions of python installed, make sure to use the correct version for your virtual environment. If you want to use virtualenv install it using `pip install virtualenv`. For conda follow the instructions [here](https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation) to install conda.

### Virtual Environment Option 1: virtualenv

#### Creating the virtual environment

Create a new virtual environment inside the root folder of your repo: 

```
virtualenv .venv
```

This will create a virtualenv with the default version of python you installed virtualenv with inside a folder called `.venv`.

If you would like to create a virtualenv with a different python version, simply append the path of the python executable you would like to use to the `-p` argument: 

```
virtualenv .venv -p /usr/local/bin/python3.9
```

Here `/usr/local/bin/python3.9` is the path to python 3.9 on a MacOS machine, but it can be a Windows path for Windows setups as well.

#### Activating and Deactivating the virtual environment

To activate the virtual environment

MacOS and Linux:

```
source .venv/bin/activate
```

Windows:

```
.venv\Scripts\activate
```

To deactivate the virtual environment run `deactivate`.

#### Cleaning up the virtual environment

In order to delete or reacreate the virtual environment, simply delete the `.venv` folder that the environment is in. Then you can rerun the command above to create a new environment.

### Virtual Environment Option 2: conda

#### Creating the virtual environment

To create a new virtual environment with conda run:

```
conda create --name iris_databricks python=3.9 -y
```

This will create a virtual environment with python 3.9 named `iris_databricks`.

#### Activating and Deactivating the virtual environment

To activate the virtual environment run:

```
conda activate iris_databricks
```

To deactivate the virtual environment run:

```
conda deactivate
```

#### Cleaning up the virtual environment

If you want to delete or reacreate the virtual environment with another python version or try with a clean environment you can do so by running:

```
conda env remove --name iris_databricks
```

Then you can rerun the commands above to recreate the environment.

### Dependency Management Option 1: Using Poetry

Install poetry: `pip install poetry`. Depending on your IDE, you can add the poetry environment or it will be picked up automatically.

Follow [this guide](https://python-poetry.org/docs/basic-usage/#specifying-dependencies) on how to use poetry for managing dependencies.

Poetry allows you to add dependencies in groups, keeping development dependencies outside package dependencies. To add a package dependency: `poetry add <package>`. Any dependency added to the base will be included in the package, all others will be optional.

To add a dependency to a specific group, say `dev`, run: 

```
poetry add <package> --group dev
```

You can also modify the `pyproject.toml` file directly but always be sure to run a `poetry lock` right after to ensure the `poetry.lock` file is up to date.

You will notice multiple dependency groups in the provided `pyproject.toml` file. This is to segregate which dependency belongs to what and ensure only the necessary package dependencies are included in the final wheel file.

To install the dependencies defined using poetry run:

```
poetry install
```

### Dependency Management Option 2: Using requirements.txt and setup.py

To generate or update the dependency requirements for your project:

```
kedro build-reqs
```

This will `pip-compile` the contents of `src/requirements.txt` into a new file `src/requirements.lock`. You can see the output of the resolution by opening `src/requirements.lock`.

After this, if you'd like to update your project requirements, please update `src/requirements.txt` and re-run `kedro build-reqs`.

[Further information about project dependencies](https://kedro.readthedocs.io/en/stable/kedro_project_setup/dependencies.html#project-specific-dependencies)

To install them, run:

```
pip install -r src/requirements.txt
```


## How to run your Kedro pipeline

You can run your Kedro project with:

```
kedro run
```

## How to test your Kedro project

Have a look at the file `src/tests/test_run.py` for instructions on how to write your tests. You can run your tests as follows:

```
pytest
```

## How to work with Kedro and notebooks locally

> Note: Using `kedro jupyter` or `kedro ipython` to run your notebook provides these variables in scope: `context`, `catalog`, and `startup_error`.
>
> Jupyter, JupyterLab, and IPython are already included in the project requirements by default, so once you have run `poetry install` or `pip install -r src/requirements.txt` you will not need to take any extra steps before you use them.

### Jupyter
To use Jupyter notebooks in your Kedro project, you need to install Jupyter (included in the pyproject.toml and requirements.txt).

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

To package your project into a wheel file, run `poetry build` or `kedro package` from the root directory of the folder (depending on whether you are using poetry or setup.py to manage your dependecies).

### Creating a wheel

Run `poetry build` or `kedro package` and a wheel file should get created with your code inside the `dist/` folder. This folder is already in the `.gitignore` so no need to worry about deleting it after.

## Running a Packaged Pipeline in Databricks

For instructions on how to run your pipeline on Databricks follow [this guide](https://docs.kedro.org/en/stable/deployment/databricks.html) from the Kedro docs.