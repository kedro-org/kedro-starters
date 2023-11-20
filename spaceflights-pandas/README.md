# The `spaceflights-pandas` Kedro starter

## Overview

This is a completed version of the [spaceflights tutorial project](https://docs.kedro.org/en/stable/tutorial/spaceflights_tutorial.html) described in the [online Kedro documentation](https://docs.kedro.org), including the data required to run the project.

The tutorial works through the steps necessary to create this project. To learn the most about Kedro, we recommend that you start with a blank template as the tutorial describes, and follow the workflow. However, if you prefer to read swiftly through the documentation and get to work on the code, you may want to generate a new Kedro project using this [starter](https://docs.kedro.org/en/stable/kedro_project_setup/starters.html) because the steps have been done for you.

To use this starter, create a new Kedro project using the commands below. To make sure you have the required dependencies, run it in your virtual environment (see [our documentation about virtual environments](https://docs.kedro.org/en/stable/get_started/install.html#virtual-environments) for guidance on how to get set up):

```bash
pip install kedro
kedro new --starter=spaceflights-pandas
cd <my-project-name>  # change directory into newly created project directory
```

Alternatively, you can follow the interactive `kedro new` flow to pick and choose which tools you want as part of your project and choose to add an example to get Spaceflights based example pipelines.
Depending on your tool selection you will get an example from either of the four spaceflights starters:
- [`spaceflights-pandas`](../spaceflights-pandas): The spaceflights tutorial example code.
- [`spaceflights-pandas-viz`](../spaceflights-pandas-viz): The spaceflights tutorial example code with viz feature examples (experiment tracking, plotting with plotly and matplotlib).
- [`spaceflights-pyspark`](../spaceflights-pyspark): An alternative Kedro Spaceflights example, using PySpark.
- [`spaceflights-pyspark-viz`](../spaceflights-pyspark-viz): An alternative Kedro Spaceflights example, using PySpark with viz feature examples (experiment tracking, plotting with plotly and matplotlib).

Install the required dependencies:

```bash
pip install -r requirements.txt
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
