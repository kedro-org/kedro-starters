# The `spaceflights-pyspark` Kedro starter

## Overview

This is a variation of the [spaceflights tutorial project](https://docs.kedro.org/en/stable/tutorial/spaceflights_tutorial.html) described in the [online Kedro documentation](https://docs.kedro.org) with `PySpark` setup.

The code in this repository demonstrates best practice when working with Kedro and PySpark. It contains a Kedro starter template with some initial configuration and two example pipelines, and originates from the [Kedro documentation about how to work with PySpark](https://docs.kedro.org/en/stable/integrations/pyspark_integration.html).

To create a project based on this starter, [ensure you have installed Kedro into a virtual environment](https://docs.kedro.org/en/stable/get_started/install.html). Then use the following command:

```bash
pip install kedro
kedro new --starter=spaceflights-pyspark
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
 

