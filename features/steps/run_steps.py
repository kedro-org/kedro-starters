import subprocess
from pathlib import Path

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


@given("I have run a non-interactive kedro new without starter")
@when("I run a non-interactive kedro new without starter")
def create_project_without_starter(context):
    """Behave step to run kedro new given the config I previously created."""
    res = subprocess.run(
        [context.kedro, "new", "-c", str(context.config_file)],
        env=context.env,
        cwd=context.temp_dir,
    )
    assert res.returncode == OK_EXIT_CODE, res
    # prevent telemetry from prompting for input during e2e tests
    telemetry_file = context.root_project_dir / ".telemetry"
    telemetry_file.write_text("consent: false", encoding="utf-8")


@given('I have prepared a config file with tools "{tools}"')
def create_config_file_with_tools(context, tools):
    """Behave step to create a temporary config file
    (given the existing temp directory) and store it in the context.
    It takes a custom tools list and sets example prompt to `n`.
    """

    context.config_file = context.temp_dir / "config.yml"
    context.project_name = "project-dummy"
    context.root_project_dir = context.temp_dir / context.project_name
    context.package_name = context.project_name.replace("-", "_")
    config = {
        "tools": tools,
        "example_pipeline": "y",
        "project_name": context.project_name,
        "repo_name": context.project_name,
        "output_dir": str(context.temp_dir),
        "python_package": context.package_name,
    }
    with context.config_file.open("w") as config_file:
        yaml.dump(config, config_file, default_flow_style=False)


@then('the expected tool directories and files should be created with "{tools}"')
def check_created_project_structure_from_tools(context, tools):
    """Behave step to check the subdirectories created by kedro new with tools."""

    def is_created(name):
        """Check if path exists."""
        return (context.root_project_dir / name).exists()

    # Base checks for any project
    for path in ["README.md", "src", "pyproject.toml", "requirements.txt"]:
        assert is_created(path), f"{path} does not exist"

    tools_list = (
        tools.split(",") if tools != "all" else ["lint", "test", "log", "docs", "data", "pyspark", "viz"]
    )

    if "lint" in tools_list:  # lint tool
        pass  # No files are added

    if "test" in tools_list:  # test tool
        assert is_created("tests"), "tests directory does not exist"

    if "log" in tools_list:  # log tool
        assert is_created("conf/logging.yml"), "logging configuration does not exist"

    if "docs" in tools_list:  # docs tool
        assert is_created("docs"), "docs directory does not exist"

    if "data" in tools_list:  # data tool
        assert is_created("data"), "data directory does not exist"

    if "pyspark" in tools_list:  # PySpark tool
        assert is_created("conf/base/spark.yml"), "spark.yml does not exist"

    if "viz" in tools_list:  # viz tool
        expected_reporting_path = Path(
            f"src/{context.package_name}/pipelines/reporting"
        )
        assert is_created(
            expected_reporting_path
        ), "reporting pipeline directory does not exist"


@given("I have installed the Kedro project's dependencies")
def install_project_dependencies(context):
    reqs_path = "requirements.txt"
    res = subprocess.run(
        [context.pip, "install", "-r", reqs_path, "-U"], cwd=context.root_project_dir
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
        [context.python, "-m", "ruff", "check", "src"], cwd=context.root_project_dir
    )


@then("I should get a successful exit code")
def check_status_code(context):
    if context.result.returncode != OK_EXIT_CODE:
        print(context.result.stdout)
        print(context.result.stderr)
        assert False, "Expected exit code {}" " but got {}".format(
            OK_EXIT_CODE, context.result.returncode
        )


@when('I execute the kedro command "{command}"')
def exec_kedro_target(context, command):
    """Execute Kedro target."""
    split_command = command.split()
    cmd = [context.kedro, *split_command]
    context.result = subprocess.run(cmd, env=context.env, cwd=str(context.root_project_dir))


@when("I install the project's python package")
def install_project_package_via_pip(context):
    """Install a python package using pip."""
    dist_dir = context.root_project_dir / "dist"
    (whl_file,) = dist_dir.glob("*.whl")
    subprocess.run([context.pip, "install", str(whl_file)], env=context.env)


@when("I execute the installed project")
def exec_project(context):
    """Execute installed Kedro project target."""
    context.result = subprocess.run(
        [context.python, "-m", context.project_name.replace("-", "_")],
        cwd=context.root_project_dir,
        env=context.env
    )
