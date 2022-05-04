# Pipeline

> *Note:* This is a `README.md` boilerplate generated using `Kedro {{ cookiecutter.kedro_version }}`.

## Overview

[Transcoding](https://kedro.readthedocs.io/en/stable/data/data_catalog.html#transcoding-datasets) is used to convert the Spark DataFrames into pandas DataFrames after splitting the data into training and testing sets.

This pipeline:
1. splits the data into training dataset and testing dataset using a configurable ratio found in `conf/base/parameters.yml`
2. runs a simple 1-nearest neighbour model (`make_prediction` node) and makes prediction dataset
3. reports the model accuracy on a test set (`report_accuracy` node)

## Pipeline inputs

### `example_iris_data`

|      |                    |
| ---- | ------------------ |
| Type | `spark.SparkDataSet` |
| Description | Example iris data containing columns |


### `parameters`

|      |                    |
| ---- | ------------------ |
| Type | `dict` |
| Description | Project parameter dictionary that must contain the following keys: `train_fraction` (the ratio used to determine the train-test split), `random_state` (random generator to ensure train-test split is deterministic) and `target_column` (identify the target column in the dataset) |


## Pipeline intermediate outputs

### `X_train`

|      |                    |
| ---- | ------------------ |
| Type | `pyspark.sql.DataFrame` |
| Description | DataFrame containing train set features |

### `y_train`

|      |                    |
| ---- | ------------------ |
| Type | `pyspark.sql.DataFrame` |
| Description | Series containing train set target |

### `X_test`

|      |                    |
| ---- | ------------------ |
| Type | `pyspark.sql.DataFrame` |
| Description | DataFrame containing test set features |

### `y_test`

|      |                    |
| ---- | ------------------ |
| Type | `pyspark.sql.DataFrame` |
| Description | Series containing test set target |

### `y_pred`

|      |                    |
| ---- | ------------------ |
| Type | `pandas.Series` |
| Description | Predictions from the 1-nearest neighbour model |


## Pipeline outputs

### `None`