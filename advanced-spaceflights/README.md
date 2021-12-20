# The `advanced-spaceflights` Kedro starter

## Overview

This is an advanced version of the [spaceflights tutorial project](https://kedro.readthedocs.io/en/stable/03_tutorial/01_spaceflights_tutorial.html) described in the [online Kedro documentation](https://kedro.readthedocs.io) extended to highlight more complex features within Kedro and to be a more representative example of a real-world Kedro Project.

To use this starter, create a new Kedro project using the commands below. To make sure you have the required dependencies, run it in your virtual environment (see [our documentation about virtual environments](https://kedro.readthedocs.io/en/stable/02_get_started/01_prerequisites.html#virtual-environments) for guidance on how to get set up):

```bash
pip install kedro
kedro new --starter=advanced-spaceflights
cd <my-project-name>  # change directory into newly created project directory
```

Install the required dependencies:

```bash
pip install -r src/requirements.txt
```

Now you can run the project:

```bash
kedro run
```