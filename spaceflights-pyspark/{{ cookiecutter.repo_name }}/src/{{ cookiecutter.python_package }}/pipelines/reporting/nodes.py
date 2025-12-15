import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objs as go
import seaborn as sn
from pyspark.sql import DataFrame as SparkDataFrame
from pyspark.sql import functions as F


def compare_passenger_capacity_exp(preprocessed_shuttles: SparkDataFrame):
    """Aggregate passenger capacity by shuttle type (Spark API) and return Pandas for plotting."""
    grouped = (
        preprocessed_shuttles
        .groupBy("shuttle_type")
        .agg(F.avg("passenger_capacity").alias("passenger_capacity"))
        .orderBy("shuttle_type")
    )
    return grouped.toPandas()


def compare_passenger_capacity_go(preprocessed_shuttles: SparkDataFrame):
    """Aggregate passenger capacity by shuttle type (Spark API) and return a Plotly figure."""
    grouped = (
        preprocessed_shuttles
        .groupBy("shuttle_type")
        .agg(F.avg("passenger_capacity").alias("avg_passenger_capacity"))
        .orderBy("shuttle_type")
    )
    pdf = grouped.toPandas()

    fig = go.Figure(
        [
            go.Bar(
                x=pdf["shuttle_type"],
                y=pdf["avg_passenger_capacity"],
            )
        ]
    )
    return fig


def create_confusion_matrix(companies: pd.DataFrame):
    matplotlib.use('Agg')

    actuals = [0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1]
    predicted = [1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1]
    data = {"y_Actual": actuals, "y_Predicted": predicted}
    df = pd.DataFrame(data, columns=["y_Actual", "y_Predicted"])

    confusion_matrix = pd.crosstab(
        df["y_Actual"], df["y_Predicted"], rownames=["Actual"], colnames=["Predicted"]
    )

    fig, ax = plt.subplots(figsize=(8, 6))
    sn.heatmap(confusion_matrix, annot=True, fmt='d', cmap='Blues', ax=ax)
    ax.set_title('Confusion Matrix')
    plt.tight_layout()

    return fig
