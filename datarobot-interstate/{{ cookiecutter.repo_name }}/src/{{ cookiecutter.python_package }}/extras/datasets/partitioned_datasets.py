import logging
from abc import ABC
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Dict, List, TypeAlias

import fsspec
import pandas as pd
from kedro.io import AbstractDataset
from kedro.io.core import get_filepath_str, get_protocol_and_path
from pandas.core.frame import DataFrame
from PIL import Image

log = logging.getLogger(__name__)


class PartitionedPandasDataframe(
    AbstractDataset[dict[str, pd.DataFrame], dict[str, pd.DataFrame]]
):
    def __init__(self, filepath: str):
        """Creates a new instance of ImageDataSet to load / save image data for given filepath.

        Args:
            filepath: The location of the image file to load / save data.
        """
        # parse the path and protocol (e.g. file, http, s3, etc.)
        protocol, path = get_protocol_and_path(filepath)
        self._protocol = protocol
        self._filepath = Path(path)
        self._fs = fsspec.filesystem(self._protocol)

    def _load(self) -> dict[str, DataFrame]:
        load_path = get_filepath_str(self._filepath, self._protocol)

        data = {}
        for partition in sorted(self._fs.ls(load_path)):
            file_path = load_path / Path(partition)
            partition = file_path.parts[-1].split(".")[0]
            data[partition] = pd.read_csv(file_path)

        return data

    def _save(self, data: dict[str, DataFrame]) -> None:
        save_path = get_filepath_str(self._filepath, self._protocol)
        Path(save_path).mkdir(parents=True, exist_ok=True)
        for partition, df in data.items():
            with self._fs.open(save_path / Path(f"{partition}.csv"), "wt") as f:
                df.to_csv(f, index=False)

    def _describe(self) -> Dict[str, Any]:
        """Returns a dict that describes the attributes of the dataset object.
        Returns:
            A dict whose keys are attribute names and values are attribute values.
        """
        return dict(
            filepath=self._filepath,
            protocol=self._protocol,
        )


@dataclass
class ResultFraction(ABC):
    name: str

    def __repr__(self) -> str:
        return f"ResultFraction(name={self.name})"


@dataclass
class ResultTextSnippet(ResultFraction):
    """
    This class represents a text snippet.
    """

    text: str


@dataclass
class ResultTable(ResultFraction):
    """
    This class represents a table.
    """

    table: pd.DataFrame


@dataclass
class ResultImage(ResultFraction):
    """
    This class represents an image.
    """

    image: Image.Image


class TestResult:
    """
    This class represents a single reporting result.
    """

    def __init__(
        self,
        test_name,
        reporting_snippets: List[ResultTextSnippet] = None,  # type: ignore
        reporting_tables: List[ResultTable] = None,  # type: ignore
        reporting_images: List[ResultImage] = None,  # type: ignore
    ):
        if reporting_snippets is None:
            reporting_snippets = []
        if reporting_tables is None:
            reporting_tables = []
        if reporting_images is None:
            reporting_images = []
        self.test_name = test_name
        self.reporting_snippets = reporting_snippets
        self.reporting_tables = reporting_tables
        self.reporting_images = reporting_images

    def get_all_image_names(self) -> List[str]:
        return [
            f"{self.test_name}/images/{image.name}.png"
            for image in self.reporting_images
        ]

    def __repr__(self) -> str:
        return f"TestResult(test_name={self.test_name}, reporting_snippets={self.reporting_snippets}, reporting_tables={self.reporting_tables}, reporting_images={self.reporting_images})"


class LatexSection:
    def __init__(
        self,
        test_name,
        latex_page: str,
        test_result_dict: dict[str, TestResult],
        latex_tables: str =  None,
    ):
        self.latex_page = latex_page
        self.test_name = test_name
        self.latex_tables = latex_tables
        self._from_test_result_dict(test_result_dict)

    def _from_test_result_dict(self, test_result_dict: dict[str, TestResult]) -> None:
        self.splits = test_result_dict.keys()
        # self.test_name = list(test_result_dict.values())[0].test_name
        self.reporting_snippets: List[ResultTextSnippet] = []
        self.reporting_tables: List[ResultTable] = []
        self.reporting_images: List[ResultImage] = []
        # merge all reporting snippets, tables, and images
        # but use the
        for test_result in test_result_dict.values():
            self.reporting_snippets.extend(test_result.reporting_snippets)
            self.reporting_tables.extend(test_result.reporting_tables)
            self.reporting_images.extend(test_result.reporting_images)


import json


class LatexSectionDataset(AbstractDataset[LatexSection, LatexSection]):
    def __init__(self, filepath: str):
        self._filepath = Path(filepath)

    def _save(self, data: LatexSection) -> None:
        # Create directories if they don't exist
        save_path = self._filepath / data.test_name
        save_path.mkdir(parents=True, exist_ok=True)

        # Save LaTeX pages
        with open(save_path / "latex_page.tex", "w") as f:
            f.write(data.latex_page)
        table_path = save_path / "tables"
        table_path.mkdir(exist_ok=True)
        if isinstance(data.latex_tables, str):
            with open(table_path / "latex_tables.tex", "w") as f:
                f.write(data.latex_tables)
        elif isinstance(data.latex_tables, dict):
            for table_name, table_content in data.latex_tables.items():
                with open(table_path / f"{table_name}.tex", "w") as f:
                    f.write(table_content)

        # Save metadata
        metadata = {"test_name": data.test_name, "splits": list(data.splits)}
        with open(save_path / "metadata.json", "w") as f:
            json.dump(metadata, f)

        # save all images as .pdf
        for image in data.reporting_images:
            image_path = save_path / "images"
            image_path.mkdir(exist_ok=True)
            image.image.save(
                image_path / f"{image.name}.png", format="png", save_all=True
            )
            image.image.save(
                image_path / f"{image.name}.pdf",
                format="pdf",
                resolution=1000.0,
                save_all=True,
            )

        # TODO: Optionally save the snippets, images, tables as files if needed

    def _load(self) -> LatexSection:
        with open(self._filepath / "latex_page.tex", "r") as f:
            latex_page = f.read()

        # Load tables
        latex_tables = None
        table_file = self._filepath / "latex_tables.tex"
        if table_file.exists():
            with open(table_file, "r") as f:
                latex_tables = f.read()
        else:
            table_path = self._filepath / "tables"
            if table_path.exists():
                latex_tables = {}
                for table_file in table_path.iterdir():
                    with open(table_file, "r") as f:
                        latex_tables[table_file.stem] = f.read()

        # Load metadata
        with open(self._filepath / "metadata.json", "r") as f:
            metadata = json.load(f)

        # TODO: Optionally load the snippets, images, tables as instances if needed
        test_result_dict = {}  # You might want to populate this from saved data

        return LatexSection(
            metadata["test_name"], latex_page, test_result_dict, latex_tables
        )

    def _describe(self) -> Dict[str, Any]:
        return dict(filepath=str(self._filepath))


class ReportingDataset(AbstractDataset[dict[str, TestResult], dict[str, TestResult]]):
    """
    This dataset class allows you to read and write compliance reporting results to a local file.
    """

    def __init__(self, filepath):
        protocol, path = get_protocol_and_path(filepath)
        self._protocol = protocol
        self._filepath = PurePosixPath(path)
        self._fs = fsspec.filesystem(self._protocol)
        load_path = get_filepath_str(self._filepath, self._protocol)
        load_path = Path(load_path)
        # get last folder name
        self.test_name = load_path.parts[-1]

    def _save(self, data: dict[str, TestResult]) -> None:
        """Save data to the specified filepath."""

        save_path = get_filepath_str(self._filepath, self._protocol)
        Path(save_path).mkdir(parents=True, exist_ok=True)
        for partition, test_result in data.items():
            self._save_test_result(test_result, partition)

    def _save_test_result(self, data: TestResult, partition: str) -> None:
        save_path = get_filepath_str(self._filepath, self._protocol)
        if data.reporting_snippets:
            snippet_path = Path(save_path) / Path("snippets")
            snippet_path.mkdir(parents=True, exist_ok=True)
            # save snippets
            for snippet in data.reporting_snippets:
                snippet_file = snippet_path / Path(f"{snippet.name}_{partition}.txt")
                with self._fs.open(snippet_file, mode="w") as f:
                    f.write(snippet.text)
        if data.reporting_tables:
            table_path = Path(save_path) / Path("tables")
            table_path.mkdir(parents=True, exist_ok=True)
            # save tables
            for table in data.reporting_tables:
                table_file = table_path / Path(f"{table.name}_{partition}.csv")
                with self._fs.open(table_file, mode="w") as f:
                    table.table.to_csv(f,index=False)
        if data.reporting_images:
            image_path = Path(save_path) / Path("images")
            image_path.mkdir(parents=True, exist_ok=True)
            # save images
            for image in data.reporting_images:
                image_file = image_path / Path(f"{image.name}_{partition}.png")
                with self._fs.open(image_file, mode="wb") as f:
                    image.image.save(f, format="PNG")

    def _load(self) -> dict[str, TestResult]:
        """Loads data from the image file.

        Returns:
            Data from the image file as a numpy array
        """
        load_path = get_filepath_str(self._filepath, self._protocol)

        load_path = Path(load_path)
        # get last folder name
        data: dict[str, TestResult] = {}

        for test_component in [d for d in load_path.iterdir() if d.is_dir()]:
            if test_component.name == "snippets":
                for snippet_file in sorted(test_component.iterdir()):
                    snippet_file_name = snippet_file.stem
                    # snippet_name = snippet_file_name.rsplit("_", 1)[0]
                    partition = snippet_file_name.rsplit("_", 1)[1]
                    with self._fs.open(snippet_file, mode="r") as f:
                        snippet_text = f.read()
                    snippet = ResultTextSnippet(snippet_file_name, snippet_text)
                    data = self._update_data(data, partition, snippet)
            elif test_component.name == "tables":
                for table_file in sorted(test_component.iterdir()):
                    table_file_name = table_file.stem
                    # table_name = table_file_name.rsplit("_", 1)[0]
                    partition = table_file_name.rsplit("_", 1)[1]
                    with self._fs.open(table_file, mode="r") as f:
                        table = pd.read_csv(f)
                    table = ResultTable(table_file_name, table)
                    data = self._update_data(data, partition, table)
            elif test_component.name == "images":
                for image_file in sorted(test_component.iterdir()):
                    image_file_name = image_file.stem
                    # image_name = image_file_name.rsplit("_", 1)[0]
                    partition = image_file_name.rsplit("_", 1)[1]
                    with self._fs.open(image_file, mode="rb") as f:
                        image = Image.open(f)
                        image.load()
                    image = ResultImage(image_file_name, image)
                    data = self._update_data(data, partition, image)
            else:
                log.error("Test component not supported:" + str(test_component))
                raise TypeError("Test component type not supported")
        return data

    def _update_data(
        self,
        data: dict[str, TestResult],
        partition: str,
        result_fraction: ResultFraction,
    ) -> dict[str, TestResult]:
        if partition not in data:
            data[partition] = TestResult(self.test_name)
        if isinstance(result_fraction, ResultTextSnippet):
            data[partition].reporting_snippets.append(result_fraction)
        elif isinstance(result_fraction, ResultTable):
            data[partition].reporting_tables.append(result_fraction)
        elif isinstance(result_fraction, ResultImage):
            data[partition].reporting_images.append(result_fraction)
        else:
            raise TypeError("ResultFraction type not supported")
        return data

    def _describe(self) -> Dict[str, Any]:
        """Returns a dict that describes the attributes of the dataset."""
        return dict(filepath=self._filepath, protocol=self._protocol)


# custom dataset for all the latex library files

LatexLibrary: TypeAlias = dict[str, str]


class LatexLibraryDataset(AbstractDataset[LatexLibrary, LatexLibrary]):
    def __init__(self, filepath: str):
        self._filepath = Path(filepath)

    def _save(self, data: dict[str, str]) -> None:
        # Create directories if they don't exist
        self._filepath.mkdir(parents=True, exist_ok=True)

        # Save LaTeX pages
        for filename, content in data.items():
            # create the relative folder structure
            (self._filepath / filename).parent.mkdir(parents=True, exist_ok=True)
            with open(self._filepath / filename, "w") as f:
                f.write(content)

    def _load(self) -> dict[str, str]:
        data = {}
        # recursively load all files in the folder - keeping track of the relative path
        for file in self._filepath.rglob("*.tex"):
            if file.is_file():
                with open(file, "r") as f:
                    data[str(file.relative_to(self._filepath))] = f.read()

        return data

    def _describe(self) -> Dict[str, Any]:
        return dict(filepath=str(self._filepath))
