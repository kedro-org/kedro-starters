# Pipeline data_science

> *Note:* This is a `README.md` boilerplate generated using `Kedro {{ cookiecutter.kedro_version }}`.

## Overview

This modular pipeline:
1. splits the data into training dataset and testing dataset using a configurable ratio found in `conf/base/parameters.yml`
2. runs a simple 1-nearest neighbour model (`train` node) and makes prediction dataset.
3. reports the model accuracy on a test set (`evaluate_model` node)

## Pipeline inputs

### `X_train`

|      |                    |
| ---- | ------------------ |
| Type | `pandas.DataFrame` |
| Description | DataFrame containing train set features |

### `y_train`

|      |                    |
| ---- | ------------------ |
| Type | `pandas.Series` |
| Description | DataFrame containing train set of species. |

### `X_test`

|      |                    |
| ---- | ------------------ |
| Type | `pandas.DataFrame` |
| Description | DataFrame containing test set features |

### `y_test`

|      |                    |
| ---- | ------------------ |
| Type | `pandas.Series` |
| Description | DataFrame containing test set of species |

### `parameters`

|      |                    |
| ---- | ------------------ |
| Type | `dict` |
| Description | Project parameter dictionary that must contain the following keys: `train_fraction` (the ratio used to determine the train-test split), `random_state` (random generator to ensure train-test split is deterministic) and `target_column` (identify the target column in the dataset)  |

## Pipeline outputs

### `y_pred`

|      |                    |
| ---- | ------------------ |
| Type | `pandas.DataFrame` |
| Description | Predictions from the 1-nearest neighbour model |
