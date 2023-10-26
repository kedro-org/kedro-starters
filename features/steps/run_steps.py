import subprocess

import yaml
import os, requests, platform
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
    print("!!!!!!!!!!!!!!", context.starters_paths)
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
    reqs_path = "requirements.txt"
    res = subprocess.run(
        [context.pip, "install", "-r", reqs_path, "-U"], cwd=context.root_project_dir
    )
    assert res.returncode == OK_EXIT_CODE

@given("I have setup hadoop binary")
def setup_hadoop(context):
    if platform.system() != 'Windows':
        return
    # Define the URLs of the files to download
    winutils_url = "https://github.com/steveloughran/winutils/raw/master/hadoop-2.7.1/bin/winutils.exe"
    hadoop_dll_url = "https://github.com/steveloughran/winutils/raw/master/hadoop-2.7.1/bin/hadoop.dll"

    # Specify the local file paths
    winutils_local_path = "winutils.exe"
    hadoop_dll_local_path = "hadoop.dll"
    hadoop_bin_dir = "C:\\hadoop\\bin"

    # Download winutils.exe and hadoop.dll
    response1 = requests.get(winutils_url)
    with open(winutils_local_path, "wb") as file1:
        file1.write(response1.content)

    response2 = requests.get(hadoop_dll_url)
    with open(hadoop_dll_local_path, "wb") as file2:
        file2.write(response2.content)

    # Move hadoop.dll to C:\Windows\System32
    os.rename(hadoop_dll_local_path, os.path.join("C:\\Windows\\System32", os.path.basename(hadoop_dll_local_path)))

    # Create C:\hadoop\bin directory
    if not os.path.exists(hadoop_bin_dir):
        os.makedirs(hadoop_bin_dir)

    # Move winutils.exe to C:\hadoop\bin
    os.rename(winutils_local_path, os.path.join(hadoop_bin_dir, os.path.basename(winutils_local_path)))

    # Set the HADOOP_HOME environment variable
    os.system(f"setx /M HADOOP_HOME {hadoop_bin_dir}")


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
