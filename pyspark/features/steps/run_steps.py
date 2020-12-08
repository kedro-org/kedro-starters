import subprocess

import yaml

from behave import given, then

OK_EXIT_CODE = 0


@given("I have prepared a config file")
def create_configuration_file(context):
    """Behave step to create a temporary config file
    (given the existing temp directory)
    and store it in the context.
    """
    context.config_file = context.temp_dir / "config.yml"
    context.project_name = "project-dummy"

    root_project_dir = context.temp_dir / context.project_name
    context.root_project_dir = root_project_dir
    config = {
        "project_name": context.project_name,
        "repo_name": context.project_name,
        "output_dir": str(context.temp_dir),
        "python_package": context.project_name.replace("-", "_"),
        "include_example": False,
    }
    with context.config_file.open("w") as config_file:
        yaml.dump(config, config_file, default_flow_style=False)


@given("I have run a non-interactive kedro new with the starter")
def create_project_from_config_file(context):
    """Behave step to run Kedro new given the config I previously created."""
    res = subprocess.run(
        [
            context.kedro,
            "new",
            "--config",
            str(context.config_file),
            "--starter",
            context.starter_path,
        ]
    )
    assert res.returncode == OK_EXIT_CODE


@given("I have installed the Kedro project's dependencies")
def install_project_dependencies(context):
    res = subprocess.run([context.kedro, "install"], cwd=context.root_project_dir)
    assert res.returncode == OK_EXIT_CODE


@given("I have executed the CLI command to list Kedro pipelines")
def run_kedro_pipeline(context):
    """Behave step to list Kedro pipelines in a project."""
    context.result = subprocess.run(
        [context.kedro, "pipeline", "list"], cwd=context.root_project_dir
    )


@then("I should get a successful exit code")
def check_status_code(context):
    if context.result.returncode != OK_EXIT_CODE:
        print(context.result.stdout)
        print(context.result.stderr)
        assert False, "Expected exit code {}" " but got {}".format(
            OK_EXIT_CODE, context.result.returncode
        )
