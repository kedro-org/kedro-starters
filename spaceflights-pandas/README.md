# The `spaceflights-pandas` Kedro starter

## Overview

This is a completed version of the [spaceflights tutorial project](https://docs.kedro.org/en/stable/tutorial/spaceflights_tutorial.html) described in the [online Kedro documentation](https://docs.kedro.org), including the data required to run the project. 

To create a project based on this starter, [ensure you have installed Kedro into a virtual environment](https://docs.kedro.org/en/stable/get_started/install.html). Then use the following command:

```bash
pip install kedro
kedro new --starter=spaceflights-pandas
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

