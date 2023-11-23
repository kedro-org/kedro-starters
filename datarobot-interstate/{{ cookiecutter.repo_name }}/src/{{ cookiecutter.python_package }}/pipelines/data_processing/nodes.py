"""
This is a boilerplate pipeline
generated using Kedro 0.18.13
"""

from typing import Any, Dict, Tuple
from io import BytesIO
import zipfile
import pandas as pd


def extract_data(
    web_data_request,
) -> pd.DataFrame:
    if web_data_request.status_code == 200:
        zip_file = zipfile.ZipFile(BytesIO(web_data_request.content))
        file_list = zip_file.namelist()
        for file_name in file_list:
            if ".csv" in file_name:
                with zip_file.open(file_name) as csv_file:
                    df = pd.read_csv(
                        csv_file,
                        compression="gzip",
                        header=0,
                    )
            else:
                pass
        zip_file.close()
    else:
        print("Failed to download the zip file")

    return df


def segment_data(
    data: pd.DataFrame, parameters: Dict[str, Any]
) -> dict[str, pd.DataFrame]:
    """Create new partitions and save using PartitionedDataset.

    Returns:
        Dictionary with the partitions to create.
    """
    try:
        data = data.drop(columns="Unnamed: 0")
    except:
        pass

    segments = {}

    if parameters["segment_column"] is None:
        segments["all_series"] = data
    else:
        assert (
            len(data.loc[:, parameters["segment_column"]].unique()) > 1
        ), "There must be at least 2 segments"
        for s in data.loc[:, parameters["segment_column"]].unique():
            partition = data.loc[data.loc[:, parameters["segment_column"]] == s, :]
            segments[s] = partition

    return segments


def split_data(
    data: Dict[str, pd.DataFrame], parameters: Dict[str, Any]
) -> Tuple[Dict[str, pd.DataFrame], Dict[str, pd.DataFrame]]:
    #     Args:
    #         data: Data containing features and target.
    #         parameters: Parameters defined in parameters.yml.
    #     Returns:
    #         Split data.
    #     """

    data_train = {}
    data_test = {}

    for s in data:
        if parameters["partitioning_method"] == "datetime":
            segment = data[s].sort_values(by=parameters["datetime_column"])
            segment_train = segment.head(
                int(parameters["train_fraction"] * len(segment))
            )
        elif parameters["partitioning_method"] == "random":
            segment = data[s]
            segment_train = segment.sample(
                frac=parameters["train_fraction"],
                random_state=parameters["random_state"],
            )
        else:
            raise NotImplementedError(
                "to implement split_data for group and stratified partitioning_method"
            )

        segment_test = segment.drop(segment_train.index)

        data_train[s] = segment_train
        data_test[s] = segment_test

    return data_train, data_test
