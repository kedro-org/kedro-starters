# [ARCHIVED] This starter is no longer maintained.
You can still find the starter code in older release tags: https://github.com/kedro-org/kedro-starters/releases/tag/0.19.14

# The `spaceflights-pandas-viz` Kedro starter
This starter is unavailable in Kedro version `1.0.0` and beyond and the latest version of Kedro that supports it is Kedro `0.19.14`. To check the version of Kedro you have installed, type `kedro -V` in your terminal window. To install a specific version of Kedro, e.g. 0.19.14, type `pip install kedro==0.19.14`.

## Overview

This is a completed version of the [spaceflights tutorial project](https://docs.kedro.org/en/stable/tutorial/spaceflights_tutorial.html) described in the [online Kedro documentation](https://docs.kedro.org) and the extra tutorial sections on [visualisation with Kedro-Viz](https://docs.kedro.org/projects/kedro-viz/en/stable/kedro-viz_visualisation.html). It includes the data required to run the project. 

To create a project based on this starter, [ensure you have installed Kedro into a virtual environment](https://docs.kedro.org/en/stable/get_started/install.html). Then use the following command:

```bash
pip install kedro
kedro new --starter=spaceflights-pandas-viz
```

After the project is created, navigate to the newly created project directory:

```bash
cd <my-project-name>  # change directory 
```

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

