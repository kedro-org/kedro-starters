import pandas as pd
from pyspark.sql import Column
from pyspark.sql import DataFrame as SparkDataFrame
from pyspark.sql.functions import regexp_replace
from pyspark.sql.types import DoubleType


def _is_true(x: Column) -> Column:
    return x == "t"


def _parse_percentage(x: Column) -> Column:
    x = regexp_replace(x, "%", "")
    x = x.cast("float") / 100
    return x


def _parse_money(x: Column) -> Column:
    x = regexp_replace(x, "[$£€]", "")
    x = regexp_replace(x, ",", "")
    x = x.cast(DoubleType())
    return x


def load_shuttles_to_spark(shuttles: pd.DataFrame) -> pd.DataFrame:
    """
    Pass through the locally loaded pandas DataFrame so it can be saved by a SparkDataset.
    Useful when developing locally but using a remote Spark session (e.g., Databricks
    Serverless via Databricks Connect) to store the data as a Spark DataFrame.
    """
    return shuttles

def load_companies_to_spark(companies: pd.DataFrame) -> pd.DataFrame:
    """
    Return the pandas DataFrame unchanged so a SparkDataset can convert and save it
    to remote Spark storage. Intended for workflows where data is local but Spark
    processing runs remotely (e.g., Databricks Serverless with Databricks Connect).
    """
    return companies

def preprocess_shuttles_spark(shuttles: SparkDataFrame) -> SparkDataFrame:
    """Preprocesses the data for shuttles.

    Args:
        shuttles: Raw data.
    Returns:
        Preprocessed data, with `price` converted to a float and `d_check_complete`,
        `moon_clearance_complete` converted to boolean.
    """
    shuttles = shuttles.withColumn("d_check_complete", _is_true(shuttles.d_check_complete))
    shuttles = shuttles.withColumn("moon_clearance_complete", _is_true(shuttles.moon_clearance_complete))
    shuttles = shuttles.withColumn("price", _parse_money(shuttles.price))

    # Drop columns that aren't used for model training
    shuttles = shuttles.drop('shuttle_location', 'engine_type', 'engine_vendor', 'cancellation_policy')
    return shuttles

def preprocess_companies_spark(companies: SparkDataFrame) -> SparkDataFrame:
    """Preprocesses the data for companies.

    Args:
        companies: Raw data.
    Returns:
        Preprocessed data, with `company_rating` converted to a float and
        `iata_approved` converted to boolean.
    """
    companies = companies.withColumn("iata_approved", _is_true(companies.iata_approved))
    companies = companies.withColumn("company_rating", _parse_percentage(companies.company_rating))

    # Drop columns that aren't used for model training
    companies = companies.drop('company_location', 'total_fleet_count')
    return companies

def preprocess_reviews_pandas(reviews: pd.DataFrame) -> pd.DataFrame:
    # Drop columns that aren't used for model training
    cols_to_drop = [
        'review_scores_comfort',
        'review_scores_amenities',
        'review_scores_trip',
        'review_scores_crew',
        'review_scores_location',
        'review_scores_price',
        'number_of_reviews',
        'reviews_per_month',
    ]
    return reviews.drop(columns=cols_to_drop, errors="ignore")


def create_model_input_table(
    shuttles: SparkDataFrame, companies: SparkDataFrame, reviews: SparkDataFrame
) -> SparkDataFrame:
    """Combines all data to create a model input table.

    Args:
        shuttles: Preprocessed data for shuttles.
        companies: Preprocessed data for companies.
        reviews: Raw data for reviews.
    Returns:
        Model input table.

    """
    # Rename columns to prevent duplicates
    shuttles = shuttles.withColumnRenamed("id", "shuttle_id")
    companies = companies.withColumnRenamed("id", "company_id")

    rated_shuttles = shuttles.join(reviews, "shuttle_id", how="left")
    model_input_table = rated_shuttles.join(companies, "company_id", how="left")
    model_input_table = model_input_table.dropna()
    return model_input_table
