# The `spaceflights` Kedro starter

## Overview

This is a tutorial project, which was generated using `Kedro 0.16.5`. It is the completed version of the [spaceflights tutorial](https://kedro.readthedocs.io/en/stable/03_tutorial/01_spaceflights_tutorial.html) described in the [online Kedro documentation](https://kedro.readthedocs.io) and includes the data necessary to run the project.

The tutorial works through the steps necessary to create this project. To learn the most about Kedro, we recommend that you start with a blank template as the tutorial describes, and follow the workflow. However, if you prefer to read swiftly through the documentation and get to work on the code, you may want to generate a new Kedro project using this [starter](https://kedro.readthedocs.io/en/stable/02_get_started/06_starters.html) because the steps have been done for you.

To use this starter, create a new Kedro project using the commands below. To make sure you have the required dependencies, run it in your virtual environment (see [our documentation about virtual environments](https://kedro.readthedocs.io/en/stable/02_get_started/01_prerequisites.html#virtual-environments) for guidance on how to get set up):

```bash
pip install kedro==0.16.5
kedro new --starter=spaceflights
cd <my-project-name>  # change directory into newly created project directory
```

Install the required dependencies:

```bash
kedro install
```

Now you can run the project:

```bash
kedro run
```

To visualise the default pipeline, run:
```bash
kedro viz
```

This will open the default browser and display the following pipeline visualisation:

![](./images/pipeline_visualisation_with_layers.png)
