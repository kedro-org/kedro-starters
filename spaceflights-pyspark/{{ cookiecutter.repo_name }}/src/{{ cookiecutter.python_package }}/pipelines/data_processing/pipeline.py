from kedro.pipeline import Node, Pipeline

from .nodes import (
    create_model_input_table,
    load_shuttles_to_spark,
    load_companies_to_spark,
    preprocess_companies_spark,
    preprocess_reviews_pandas,
    preprocess_shuttles_spark,
)


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            Node(
                func=load_shuttles_to_spark,
                inputs="shuttles",
                outputs="shuttles_spark",
                name="load_shuttles_to_spark_node",
            ),
            Node(
                func=load_companies_to_spark,
                inputs="companies",
                outputs="companies_spark",
                name="load_companies_to_spark_node",
            ),            
            Node(
                func=preprocess_companies_spark,
                inputs="companies_spark",
                outputs="preprocessed_companies",
                name="preprocess_companies_node",
            ),
            Node(
                func=preprocess_shuttles_spark,
                inputs="shuttles_spark",
                outputs="preprocessed_shuttles",
                name="preprocess_shuttles_node",
            ),
            Node(
                func=preprocess_reviews_pandas,
                inputs="reviews",
                outputs="preprocessed_reviews",
                name="preprocess_reviews_node",
            ),
            Node(
                func=create_model_input_table,
                inputs=["preprocessed_shuttles", "preprocessed_companies", "preprocessed_reviews"],
                outputs="model_input_table@spark",
                name="create_model_input_table_node",
            ),
        ]
    )
