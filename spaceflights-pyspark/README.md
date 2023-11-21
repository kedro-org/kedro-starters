# The `spaceflights-pyspark` Kedro starter

## Overview

This is a variation of the [spaceflights tutorial project](https://docs.kedro.org/en/stable/tutorial/spaceflights_tutorial.html) described in the [online Kedro documentation](https://docs.kedro.org) with `PySpark` setup.

The code in this repository demonstrates best practice when working with Kedro and PySpark. It contains a Kedro starter template with some initial configuration and two example pipelines, and originates from the [Kedro documentation about how to work with PySpark](https://docs.kedro.org/en/stable/integrations/pyspark_integration.html).

To use this starter, create a new Kedro project using the commands below. To make sure you have the required dependencies, run it in your virtual environment (see [our documentation about virtual environments](https://docs.kedro.org/en/stable/get_started/install.html#virtual-environments) for guidance on how to get set up):

```bash
pip install kedro
kedro new --starter=spaceflights-pyspark
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

## Features

### Single configuration in `/conf/base/spark.yml`

While Spark allows you to specify many different [configuration options](https://spark.apache.org/docs/latest/configuration.html), this starter uses `/conf/base/spark.yml` as a single configuration location.

### `SparkSession` initialisation with `SparkHooks`

This Kedro starter contains the initialisation code for `SparkSession` in `hooks.py` and takes its configuration from `/conf/base/spark.yml`. Modify the `SparkHooks` code if you want to further customise your `SparkSession`, e.g. to use [YARN](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/YARN.html).

### Uses transcoding to handle the same data in different formats

In some cases it can be desirable to handle one dataset in different ways, for example to load a parquet file into your pipeline using `pandas` and to save it using `spark`. In this starter, one of the input datasets `shuttles`, is an excel file. 
It's not possible to load an excel file directly into Spark, so we use transcoding to save the file as a `pandas.CSVDataset` first which then allows us to load it as a `spark.SparkDataset` further on in the pipeline.
 

