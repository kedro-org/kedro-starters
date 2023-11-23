# The `datarobot-interstate` Kedro starter

## Introduction

The code in this repository demonstrates best practice when working with Kedro on DataRobot. It contains a Kedro starter template with some initial configuration and an example pipeline.

This starter contains a project created with example code based on the familiar [Metro Interstate Traffic Volume dataset](http://archive.ics.uci.edu/dataset/492/metro+interstate+traffic+volume).

## Getting started

The starter template can be used to start a new project using the [`starter` option](https://docs.kedro.org/en/stable/kedro_project_setup/starters.html) in `kedro new`:

```bash
pip install --upgrade pip
pip install --verbose kedro
kedro new --starter=kedro-starters/datarobot-interstate
```

When prompted, enter the `project_name`, which is used to set the `repo_name` and `python_package` name. The new project is portable and can be moved to any directory of your choice.

## Customization

#### Add `conf/local/credentials.yml` with DataRobot API Endpoint and Token

```bash
datarobot:
    endpoint: https://datarobot.ms.com/api/v2
    token: <your_token>
```

See the documentation on [DataRobot Developer Tools](https://docs.datarobot.com/en/docs/platform/account-mgmt/acct-settings/api-key-mgmt.html) for more information.

#### Configure `parameters` in  `conf/base/parameters.yml` or `conf/prod/parameters.yml`

```bash
target_column: <your_target>
segment_column: <your_segment>
datetime_column: <your_datetime>
task_type: <your_task_type> # regression, binary_classification, multiclass_classification, clustering, anomaly_detection
partitioning_method: <your_partitioning_method> # datetime, random, group, stratified
train_fraction: <your_train_fraction>
random_state: <your_random_state>
```

## How to run your dr-flow pipeline
Run the full set of pipelines in your `env_name` environment (e.g. `prod`, default `base` if not provided), by typing the following into your terminal from the project directory:

```bash
pip install --verbose -r src/requirements.txt
kedro run --env=<env_name>
```

## How to visualise your dr-flow pipeline
Start Kedro-Viz for the full set of pipelines by typing the following into your terminal from the project directory:

```bash
kedro viz
```
The command opens a browser tab to serve the visualisation at http://127.0.0.1:4141/.
