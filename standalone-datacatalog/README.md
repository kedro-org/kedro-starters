# [ARCHIVED] This starter is no longer maintained.
You can still find the starter code in older release tags: https://github.com/kedro-org/kedro-starters/tree/0.18.14/standalone-datacatalog

## The `standalone-datacatalog` Kedro starter
This starter is unavailable in Kedro version `0.19.0` and beyond and the latest version of Kedro that supports it is Kedro `0.18.14`. To check the version of Kedro you have installed, type `kedro -V` in your terminal window. To install a specific version of Kedro, e.g. 0.18.14, type `pip install kedro==0.18.14`.

To create a project with this starter using `kedro new`, type the following (assuming Kedro version 0.18.14):

```
kedro new --starter=standalone-datacatalog --checkout=0.18.14
```

### Introduction
This starter, formerly known as `mini-kedro`, sets up a lightweight Kedro project that uses the Kedro [Data Catalog](https://docs.kedro.org/en/stable/data/index.html) as a registry for data without using any of the other features of Kedro.

The starter comprises a minimal setup to use the traditional [Iris dataset](https://www.kaggle.com/uciml/iris).

### Usage

To create a new project based on this starter:

```bash
kedro new --starter=standalone-datacatalog
```

You can call the project any name you choose. When created, the project contains the following:

* A `conf` directory, which contains an example `DataCatalog` configuration (`catalog.yml`):

 ```yaml
# conf/base/catalog.yml
example_dataset_1:
  type: pandas.CSVDataset
  filepath: folder/filepath.csv

example_dataset_2:
  type: spark.SparkDataset
  filepath: s3a://your_bucket/data/01_raw/example_dataset_2*
  credentials: dev_s3
  file_format: csv
  save_args:
    if_exists: replace
```

* A `data` directory, which contains an example dataset identical to the one used by the [`pandas-iris`](https://github.com/kedro-org/kedro-starters/tree/main/pandas-iris) starter

* An example Jupyter notebook, which shows how to instantiate the `DataCatalog` and interact with the example dataset:

```python
df = catalog.load("example_dataset_1")
df_2 = catalog.save("example_dataset_2")
```
