# Data Engineering pipeline

> *Note:* This `README.md` was generated using `Kedro 0.16.2` for illustration purposes. Please modify it according to your pipeline structure and contents.

## Overview

This modular pipeline illustrates a PySpark-based data engineering pipeline which:
1. Extracting, transforming and selecting features from the dataset (`transform_features` node)
2. Split the dataset into training dataset and testing dataset based on a configurable ratio (`split_data` node)

## Pipeline inputs

### `example_iris_data`

|             |                                                          |
| ----------- | ---------------------------------------------------------| 
| Type        | `spark.SparkDataSet`                                     |
| Description | Input data to perform features engineering and splitting |

### `params:example_test_data_ratio`

|             |                                                                                         |
| ----------- | --------------------------------------------------------------------------------------- |
| Type        | `float`                                                                                 |
| Description | The split ratio parameter that identifies what percentage of rows goes to the train set |

## Pipeline outputs

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