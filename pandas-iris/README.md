# [ARCHIVED] This starter is no longer maintained.
You can still find the starter code in older release tags: https://github.com/kedro-org/kedro-starters/tree/0.18.14/pandas-iris 

## The `pandas-iris` Kedro starter
This starter is unavailable in Kedro version `0.19.0` and beyond and the latest version of Kedro that supports it is Kedro `0.18.14`. To check the version of Kedro you have installed, type `kedro -V` in your terminal window. To install a specific version of Kedro, e.g. 0.18.14, type `pip install kedro==0.18.14`.

To create a project with this starter using `kedro new`, type the following (assuming Kedro version 0.18.14):

```
kedro new --starter=pandas-iris --checkout=0.18.14
```

### Introduction
The code in this repository demonstrates best practice when working with Kedro. It contains a Kedro starter template with some initial configuration and an example pipeline, and originates from the [Kedro Iris dataset example](https://docs.kedro.org/en/0.18.14/get_started/new_project.html).

#### An example pipeline using only native `Kedro`

![](./images/iris_pipeline.png)

This Kedro starter uses the simple and familiar [Iris dataset](https://www.kaggle.com/uciml/iris). It contains the code for an example machine learning pipeline that runs a 1-nearest neighbour classifier to classify an iris. 

The pipeline includes:

* A node to split the data into training dataset and testing dataset using a configurable ratio
* A node to run a simple 1-nearest neighbour classifier and make predictions
* A node to report the accuracy of the predictions performed by the model
