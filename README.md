# kedro-starters

This repository contains all official [Kedro starters](https://docs.kedro.org/en/stable/kedro_project_setup/starters.html). A starter can be used to bootstrap a new Kedro project as follows:

```bash
kedro new --starter=<alias>
```

The following aliases are available:

* [Alias `astro-airflow-iris`](astro-airflow-iris): The [Kedro Iris dataset example project](https://docs.kedro.org/en/0.18.14/get_started/new_project.html) with a minimal setup for deploying the pipeline on Airflow with [Astronomer](https://www.astronomer.io/).

* [Alias `databricks-iris`](databricks-iris): The [Kedro Iris dataset example project](https://docs.kedro.org/en/0.18.14/get_started/new_project.html) with a minimal setup for running and deploying the pipeline on Databricks.

* [Alias `datarobot-interstate`](datarobot-interstate): The [Metro Interstate Traffic Volume dataset example project](http://archive.ics.uci.edu/dataset/492/metro+interstate+traffic+volume) with a minimal setup for running and deploying the pipeline on DataRobot.

* [Alias `spaceflights-pandas`](spaceflights-pandas): The [spaceflights tutorial](https://docs.kedro.org/en/stable/tutorial/spaceflights_tutorial.html) example code.

* [Alias `spaceflights-pandas-viz`](spaceflights-pandas-viz): The [spaceflights tutorial](https://docs.kedro.org/en/stable/tutorial/spaceflights_tutorial.html) example code with viz feature examples (experiment tracking, plotting with plotly and matplotlib).

* [Alias `spaceflights-pyspark`](spaceflights-pyspark): An alternative Kedro Spaceflights example, using [PySpark](https://docs.kedro.org/en/stable/integrations/pyspark_integration.html).

* [Alias `spaceflights-pyspark-viz`](spaceflights-pyspark-viz): An alternative Kedro Spaceflights example, using [PySpark](https://docs.kedro.org/en/stable/integrations/pyspark_integration.html) with viz feature examples (experiment tracking, plotting with plotly and matplotlib).


Archived starters which are no longer maintained:

* [Alias `pandas-iris`](pandas-iris): The [Kedro Iris dataset example project](https://docs.kedro.org/en/0.18.14/get_started/new_project.html)

* [Alias `pyspark-iris`](pyspark-iris): An alternative Kedro Iris dataset example, using [PySpark](https://docs.kedro.org/en/stable/integrations/pyspark_integration.html)

* [Alias `pyspark`](pyspark): The configuration and initialisation code for a [Kedro pipeline using PySpark](https://docs.kedro.org/en/stable/integrations/pyspark_integration.html)

* [Alias `standalone-datacatalog`](standalone-datacatalog): A minimum setup to use the traditional [Iris dataset](https://www.kaggle.com/uciml/iris) with Kedro's [`DataCatalog`](https://docs.kedro.org/en/stable/data/data_catalog.html), which is a core component of Kedro. This starter is of use in the exploratory phase of a project. For more information, read the guide to [standalone use of the `DataCatalog`](https://docs.kedro.org/en/stable/notebooks_and_ipython/kedro_as_a_data_registry.html). This starter was formerly known as `mini-kedro`.