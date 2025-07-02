# [ARCHIVED] This starter is no longer maintained.
You can still find the starter code in older release tags: https://github.com/kedro-org/kedro-starters/releases/tag/0.19.14

# The `spaceflights-pyspark-viz` Kedro starter
This starter is unavailable in Kedro version `1.0.0` and beyond and the latest version of Kedro that supports it is Kedro `0.19.14`. To check the version of Kedro you have installed, type `kedro -V` in your terminal window. To install a specific version of Kedro, e.g. 0.19.14, type `pip install kedro==0.19.14`.

## Overview

This is a completed version of the [spaceflights tutorial project](https://docs.kedro.org/en/stable/tutorial/spaceflights_tutorial.html) and the extra tutorial sections on [visualisation with Kedro-Viz](https://docs.kedro.org/projects/kedro-viz/en/stable/kedro-viz_visualisation.html). This project includes the data required to run it. The code in this repository demonstrates best practice when working with Kedro and PySpark.

To create a project based on this starter, [ensure you have installed Kedro into a virtual environment](https://docs.kedro.org/en/stable/get_started/install.html). Then use the following command:

```bash
pip install kedro
kedro new --starter=spaceflights-pyspark-viz
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

## Features

### Single configuration in `/conf/base/spark.yml`

While Spark allows you to specify many different [configuration options](https://spark.apache.org/docs/latest/configuration.html), this starter uses `/conf/base/spark.yml` as a single configuration location.

### `SparkSession` initialisation with `SparkHooks`

This Kedro starter contains the initialisation code for `SparkSession` in `hooks.py` and takes its configuration from `/conf/base/spark.yml`. Modify the `SparkHooks` code if you want to further customise your `SparkSession`, e.g. to use [YARN](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/YARN.html).

### Uses transcoding to handle the same data in different formats

In some cases it can be desirable to handle one dataset in different ways, for example to load a parquet file into your pipeline using `pandas` and to save it using `spark`. In this starter, one of the input datasets `shuttles`, is an excel file. 
It's not possible to load an excel file directly into Spark, so we use transcoding to save the file as a `pandas.CSVDataset` first which then allows us to load it as a `spark.SparkDataset` further on in the pipeline.
 

