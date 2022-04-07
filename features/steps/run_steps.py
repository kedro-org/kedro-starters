import subprocess

import yaml
from behave import given, then, when

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


@given("I have run a non-interactive kedro new with the starter {starter_name}")
def create_project_from_config_file(context, starter_name):
    """Behave step to run Kedro new given the config I previously created."""
    res = subprocess.run(
        [
            context.kedro,
            "new",
            "--config",
            str(context.config_file),
            "--starter",
            context.starters_paths[starter_name],
        ]
    )
    assert res.returncode == OK_EXIT_CODE
    # prevent telemetry from prompting for input during e2e tests
    telemetry_file = context.root_project_dir / ".telemetry"
    telemetry_file.write_text("consent: false", encoding="utf-8")


@given("I have installed the Kedro project's dependencies")
def install_project_dependencies(context):
    reqs_path = "src/requirements.txt"
    res = subprocess.run(
        [context.pip, "install", "-r", reqs_path], cwd=context.root_project_dir
    )
    assert res.returncode == OK_EXIT_CODE


@when("I run the Kedro pipeline")
def run_kedro_pipeline(context):
    """Behave step to run the newly created Kedro pipeline."""
    context.result = subprocess.run(
        [context.kedro, "run"], cwd=context.root_project_dir
    )


@when("I execute the CLI command to list Kedro pipelines")
def list_kedro_pipelines(context):
    """Behave step to list Kedro pipelines in a project."""
    context.result = subprocess.run(
        [context.kedro, "registry", "list"], cwd=context.root_project_dir
    )


@when("I lint the project")
def lint_project(context):
    context.result = subprocess.run(
        [context.kedro, "lint", "--check-only"], cwd=context.root_project_dir
    )


@then("I should get a successful exit code")
def check_status_code(context):
    if context.result.returncode != OK_EXIT_CODE:
        print(context.result.stdout)
        print(context.result.stderr)
        assert False, "Expected exit code {}" " but got {}".format(
            OK_EXIT_CODE, context.result.returncode
        )
