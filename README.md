# kedro-starters

This repository contains all official [Kedro starters](https://kedro.readthedocs.io/en/stable/get_started/starters.html). A starter can be used to bootstrap a new Kedro project as follows:

```bash
kedro new --starter=<alias>
```

The following aliases are available:

* [Alias `astro-airflow-iris`](astro-airflow-iris): The [Kedro Iris dataset example project](https://kedro.readthedocs.io/en/stable/get_started/example_project.html) with a minimal setup for deploying the pipeline on Airflow with [Astronomer](https://www.astronomer.io/).

* [Alias `pandas-iris`](pandas-iris): The [Kedro Iris dataset example project](https://kedro.readthedocs.io/en/stable/get_started/example_project.html)

* [Alias `pyspark-iris`](pyspark-iris): An alternative Kedro Iris dataset example, using [PySpark](https://kedro.readthedocs.io/en/stable/tools_integration/pyspark.html)

* [Alias `pyspark`](pyspark): The configuration and initialisation code for a [Kedro pipeline using PySpark](https://kedro.readthedocs.io/en/stable/tools_integration/pyspark.html)

* [Alias `spaceflights`](spaceflights): The [spaceflights tutorial](https://kedro.readthedocs.io/en/stable/tutorial/spaceflights_tutorial.html) example code

* [Alias `standalone-datacatalog`](standalone-datacatalog): A minimum setup to use the traditional [Iris dataset](https://www.kaggle.com/uciml/iris) with Kedro's [`DataCatalog`](https://kedro.readthedocs.io/en/stable/05_data/01_data_catalog.html), which is a core component of Kedro. This starter is of use in the exploratory phase of a project. For more information, read the guide to [standalone use of the `DataCatalog`](https://kedro.readthedocs.io/en/stable//02_get_started/07_standalone_use_of_datacatalog.html). This starter was formerly known as `mini-kedro`.