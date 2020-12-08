# Copyright 2020 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited ("QuantumBlack") name and logo
# (either separately or in combination, "QuantumBlack Trademarks") are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
#     or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.
import yaml

from behave import given, then

from features.steps.sh_run import run

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
        yaml.safe_dump(config, config_file, default_flow_style=False)


@given("I have run a non-interactive kedro new with the starter")
def create_project_from_config_file(context):
    """Behave step to run Kedro new given the config I previously created."""
    res = run(
        [
            context.kedro,
            "new",
            "--config",
            str(context.config_file),
            "--starter",
            context.starter_path,
        ]
    )
    assert res.returncode == OK_EXIT_CODE, res.stdout


@given("I have installed the Kedro project's dependencies")
def install_project_dependencies(context):
    res = run([context.kedro, "install"], cwd=context.root_project_dir)
    assert res.returncode == OK_EXIT_CODE, res.stdout


@given("I have run the Kedro pipeline")
def run_kedro_pipeline(context):
    """Behave step to run the newly created Kedro pipeline."""
    context.result = run([context.kedro, "run"], cwd=context.root_project_dir)


@then("I should get a successful exit code")
def check_status_code(context):
    if context.result.returncode != OK_EXIT_CODE:
        print(context.result.stdout)
        print(context.result.stderr)
        error = f"Expected exit code {OK_EXIT_CODE} but got {context.result.returncode}"
        assert False, error
