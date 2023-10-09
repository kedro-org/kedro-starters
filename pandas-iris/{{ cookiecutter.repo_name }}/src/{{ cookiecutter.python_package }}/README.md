# Pipeline

> *Note:* This is a `README.md` boilerplate generated using `Kedro {{ cookiecutter.kedro_version }}`.

## Overview

This pipeline:
1. splits the data into training dataset and testing dataset using a configurable ratio found in `conf/base/parameters.yml`
2. runs a simple 1-nearest neighbour model (`make_prediction` node) and makes prediction dataset
3. reports the model accuracy on a test set (`report_accuracy` node)

## Pipeline inputs

### `example_iris_data`

|      |                    |
| ---- | ------------------ |
| Type | `pandas.CSVDataset` |
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
| Type | `pandas.DataFrame` |
| Description | DataFrame containing train set features |

### `y_train`

|      |                    |
| ---- | ------------------ |
| Type | `pandas.Series` |
| Description | Series containing train set target. |

### `X_test`

|      |                    |
| ---- | ------------------ |
| Type | `pandas.DataFrame` |
| Description | DataFrame containing test set features |

### `y_test`

|      |                    |
| ---- | ------------------ |
| Type | `pandas.Series` |
| Description | Series containing test set target |

### `y_pred`

|      |                    |
| ---- | ------------------ |
| Type | `pandas.Series` |
| Description | Predictions from the 1-nearest neighbour model |


## Pipeline outputs

### `None`
