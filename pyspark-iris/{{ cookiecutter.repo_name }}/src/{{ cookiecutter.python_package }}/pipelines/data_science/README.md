# Data Science pipeline

> *Note:* This `README.md` was generated using `Kedro 0.16.2` for illustration purposes. Please modify it according to your pipeline structure and contents.

## Overview

This modular pipeline illustrates a PySpark-based data science pipeline which:
1. Trains a simple random forest classifier (`train_model` node)
2. Makes predictions given a trained model (`predict` node)
3. Reports the model's predictions accuracy (`report_accuracy` node)


## Pipeline inputs

### `training_data`

|             |                                                |
| ----------- | ---------------------------------------------- |
| Type        | `pyspark.sql.DataFrame`                        |
| Description | DataFrame containing the training dataset      |

### `testing_data`

|             |                                                |
| ----------- | ---------------------------------------------- |
| Type        | `pyspark.sql.DataFrame`                        |
| Description | DataFrame containing testing dataset           |

### `parameters`

|      |                    |
| ---- | ------------------ |
| Type | `dict` |
| Description | Project parameter dictionary specifying the following key: `example_num_trees` (number of trees to train the random forest classifier) |


## Pipeline outputs

### `example_classifier`

|             |                                   |
| ----------- | --------------------------------- |
| Type        | `RandomForestClassifier`          |
| Description | Example logistic regression model |
