from kedro.pipeline import Node, Pipeline

from .nodes import (
    create_model_input_table,
    load_shuttles_to_csv,
    preprocess_companies,
    preprocess_reviews,
    preprocess_shuttles,
)


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            Node(
                func=load_shuttles_to_csv,
                inputs="shuttles_excel",
                outputs="shuttles@csv",
                name="load_shuttles_to_csv_node",
            ),
            Node(
                func=preprocess_companies,
                inputs="companies",
                outputs="preprocessed_companies",
                name="preprocess_companies_node",
            ),
            Node(
                func=preprocess_shuttles,
                inputs="shuttles@spark",
                outputs="preprocessed_shuttles",
                name="preprocess_shuttles_node",
            ),
            Node(
                func=preprocess_reviews,
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
