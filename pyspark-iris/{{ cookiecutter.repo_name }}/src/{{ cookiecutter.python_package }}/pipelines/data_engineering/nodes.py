"""Example nodes to solve some common data engineering problems using PySpark,
such as:
* Extracting, transforming and selecting features
* Split data into training and testing datasets
"""

from typing import List

from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.sql import DataFrame


def transform_features(data: DataFrame) -> DataFrame:
    """Node for transforming 4 feature columns in the dataset
    into a single features vector column, as well as transforming
    the textual representation of the species column into a numeric one.

    For more information, please visit:
    https://spark.apache.org/docs/latest/ml-features
    """
    raw_feature_columns = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    # merge 4 feature columns into a single features vector column
    vector_assembler = VectorAssembler(
        inputCols=raw_feature_columns, outputCol="features"
    )
    transformed_data = vector_assembler.transform(data).drop(*raw_feature_columns)

    # convert the textual representation of the species into numerical label column
    raw_target_column = "species"
    indexer = StringIndexer(inputCol=raw_target_column, outputCol="label")
    transformed_data = (
        indexer.fit(transformed_data)
        .transform(transformed_data)
        .drop(raw_target_column)
    )
    return transformed_data


def split_data(
    transformed_data: DataFrame, example_test_data_ratio: float
) -> List[DataFrame]:
    """Node for splitting the classical Iris data set into training and test
    sets, each split into features and labels.
    The split ratio parameter is taken from conf/base/parameters.yml.
    """
    example_train_data_ratio = 1 - example_test_data_ratio
    training_data, testing_data = transformed_data.randomSplit(
        [example_train_data_ratio, example_test_data_ratio]
    )
    return [training_data, testing_data]
