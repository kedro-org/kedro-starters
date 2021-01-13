# Copyright 2021 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
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
# or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.

import shlex
import subprocess
from typing import Any, Union


def run(
    cmd: Union[list, str], split: bool = True, print_output: bool = False, **kwargs: Any
) -> subprocess.CompletedProcess:
    """Run a shell command.

    Args:
        cmd: A command string, or a command followed by program
            arguments that will be submitted to Popen to run.

        split: Flag that splits command to provide as multiple *args
            to Popen. Default is True.

        print_output: If True will print previously captured stdout.
            Default is False.

        kwargs: Extra options to pass to subprocess.

    Example:
    ::
        "ls"
        "ls -la"
        "chmod 754 local/file"

    Returns:
        Result with attributes args, returncode, stdout and stderr.

    """
    if isinstance(cmd, str) and split:
        cmd = shlex.split(cmd)
    # pylint: disable=subprocess-run-check
    result = subprocess.run(
        cmd, input="", stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs
    )
    result.stdout = result.stdout.decode("utf-8")
    result.stderr = result.stderr.decode("utf-8")
    if print_output:
        print(result.stdout)
    return result


def check_run(cmd: Union[list, str], print_output: bool = False) -> None:
    """
    Run cmd using subprocess.check_call (throws error if non-zero value
    returned)

    Args:
        cmd: command to be run
        print_output: whether to print output
    """
    if isinstance(cmd, str):
        split_cmd = shlex.split(cmd)
    else:
        split_cmd = cmd

    kwargs = dict()
    if not print_output:
        kwargs.update(stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    subprocess.check_call(split_cmd, **kwargs)
