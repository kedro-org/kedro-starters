# {{ cookiecutter.repo_name }}

Live on [{{ cookiecutter.repo_name }}.waylonwalker.com](https://{{ cookiecutter.repo_name }}.waylonwalker.com/)

Listing python packages from pypi, and finding available single word packages.

## Install

``` bash
pip install -r requirements.txt
```

## Run the Pipeline

``` bash
# Run with existing package data
python {{ cookiecutter.repo_name }}.py

# Full run
python {{ cookiecutter.repo_name }}.py --full
```

## Scheduled on GitHub actions

This pipeline run daily at `0:0` to generate a `packages.json`,
`unavailable.json`, `avalilable.json`.

## Development


``` bash
pip install -e ".[dev]"
```

This project includes a `pre-commit-config`, this ensures that each commit made
to the project passes all checks that are also ran in CI. To setup pre-commit
in your development environment run the follow command.

``` bash
pre-commit install
```
