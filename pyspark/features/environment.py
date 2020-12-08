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

"""Behave environment setup commands"""

import os
import shutil
import stat
import subprocess
import tempfile
import venv
from pathlib import Path


def create_new_venv() -> Path:
    """Create a new venv.
    Returns:
        path to created venv
    """
    # Create venv
    venv_dir = Path(tempfile.mkdtemp())
    venv.main([str(venv_dir)])
    return venv_dir


def before_scenario(context, scenario):
    """Environment preparation before each test is run.
    """

    context.venv_dir = create_new_venv()
    bin_dir = context.venv_dir / "bin"
    context.pip = str(bin_dir / "pip")
    context.python = str(bin_dir / "python")
    context.kedro = str(bin_dir / "kedro")
    context.starter_path = str(Path(__file__).parents[1])
    subprocess.run([context.python, "-m", "pip", "install", "-U", "pip", "wheel"])
    subprocess.run([context.pip, "install", "-r", "test_requirements.txt"])
    context.temp_dir = Path(tempfile.mkdtemp())


def after_scenario(context, scenario):
    rmtree(str(context.temp_dir))
    rmtree(str(context.venv_dir))


def rmtree(top):
    if os.name != "posix":
        for root, _, files in os.walk(top, topdown=False):
            for name in files:
                os.chmod(os.path.join(root, name), stat.S_IWUSR)
    shutil.rmtree(top)
