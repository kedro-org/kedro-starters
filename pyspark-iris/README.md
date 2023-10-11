# The `pyspark-iris` Kedro starter

## Introduction

The code in this repository demonstrates best practice when working with Kedro and PySpark. It contains a Kedro starter template with some initial configuration and an example pipeline, and originates from the [Kedro documentation about how to work with PySpark](https://docs.kedro.org/en/stable/integrations/pyspark_integration.html).

## Getting started

The starter template can be used to start a new project using the [`starter` option](https://docs.kedro.org/en/stable/kedro_project_setup/starters.html) in `kedro new`:

```bash
kedro new --starter=pyspark-iris
```

As a reference, the [How to use Kedro on a Databricks cluster](https://docs.kedro.org/en/stable/deployment/databricks/index.html) tutorial bootstraps the project using this starter.

## Features

### Single configuration in `/conf/base/spark.yml`

While Spark allows you to specify many different [configuration options](https://spark.apache.org/docs/latest/configuration.html), this starter uses `/conf/base/spark.yml` as a single configuration location.

### `SparkSession` initialisation

This Kedro starter contains the initialisation code for `SparkSession` in the `ProjectContext` and takes its configuration from `/conf/base/spark.yml`. Modify this code if you want to further customise your `SparkSession`, e.g. to use [YARN](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/YARN.html).

### Configures `MemoryDataset` to work with Spark objects
Out of the box, Kedro's `MemoryDataset` works with Spark's `DataFrame`. However, it doesn't work with other Spark objects such as machine learning models unless you add further configuration. This Kedro starter demonstrates how to configure `MemoryDataset` for Spark's machine learning model in the `catalog.yml`.

> Note: The use of `MemoryDataset` is encouraged to propagate Spark's `DataFrame` between nodes in the pipeline. A best practice is to delay triggering Spark actions for as long as needed to take advantage of Spark's lazy evaluation.

### An example machine learning pipeline that uses only `PySpark` and `Kedro`

![Iris Pipeline Visualisation](./images/iris_pipeline.png)

This Kedro starter uses the simple and familiar [Iris dataset](https://www.kaggle.com/uciml/iris). It contains the code for an example machine learning pipeline that runs a 1-nearest neighbour classifier to classify an iris. 
[Transcoding](https://docs.kedro.org/en/stable/data/data_catalog_yaml_examples.html#read-the-same-file-using-two-different-datasets) is used to convert the Spark Dataframes into pandas DataFrames after splitting the data into training and testing sets.

The pipeline includes:

* A node to split the data into training dataset and testing dataset using a configurable ratio
* A node to run a simple 1-nearest neighbour classifier and make predictions
* A node to report the accuracy of the predictions performed by the model
