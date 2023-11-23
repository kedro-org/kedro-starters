# [ARCHIVED] This starter is no longer maintained.
You can still find the starter code in older release tags: https://github.com/kedro-org/kedro-starters/tree/0.18.14/pyspark 

## The `pyspark` Kedro starter
This starter is unavailable in Kedro version `0.19.0` and beyond and the latest version of Kedro that supports it is Kedro `0.18.14`. To check the version of Kedro you have installed, type `kedro -V` in your terminal window. To install a specific version of Kedro, e.g. 0.18.14, type `pip install kedro==0.18.14`.

To create a project with this starter using `kedro new`, type the following (assuming Kedro version 0.18.14):

```
kedro new --starter=pyspark --checkout=0.18.14
``` 

### Introduction
The code in this repository demonstrates best practice when working with Kedro and PySpark. It contains a Kedro starter template with some initial configuration and an example pipeline, and originates from the [Kedro documentation about how to work with PySpark](https://docs.kedro.org/en/stable/integrations/pyspark_integration.html).

### Features

#### Single configuration in `/conf/base/spark.yml`

While Spark allows you to specify many different [configuration options](https://spark.apache.org/docs/latest/configuration.html), this starter uses `/conf/base/spark.yml` as a single configuration location.

#### `SparkSession` initialisation

This Kedro starter contains the initialisation code for `SparkSession` in the `ProjectContext` and takes its configuration from `/conf/base/spark.yml`. Modify this code if you want to further customise your `SparkSession`, e.g. to use [YARN](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/YARN.html).
