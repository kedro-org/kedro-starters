"""Behave environment setup commands"""
from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import tempfile
import venv
from pathlib import Path
from typing import Any, Set

_PATHS_TO_REMOVE: Set[Path] = set()




def run(
    cmd: list | str, split: bool = True, print_output: bool = False, **kwargs: Any
) -> subprocess.CompletedProcess:
    """Run a shell command.

    Args:
        cmd: A command string, or a command followed by program
            arguments that will be submitted to Popen to run.

        split: Flag that splits command to provide as multiple *args
            to Popen. Default is True.

        print_output: If True will print previously captured stdout.
            Default is False.

        **kwargs: Extra options to pass to subprocess.

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
    result = subprocess.run(cmd, input="", capture_output=True, **kwargs)  # noqa: PLW1510
    result.stdout = result.stdout.decode("utf-8")
    result.stderr = result.stderr.decode("utf-8")
    if print_output:
        print(result.stdout)
    return result

def call(cmd, env):
    res = run(cmd, env=env)
    if res.returncode:
        print(res.stdout)
        print(res.stderr)
        assert False

def create_new_venv() -> Path:
    """Create a new venv.
    Returns:
        path to created venv
    """
    # Create venv
    venv_dir = _create_tmp_dir()
    venv.main([str(venv_dir)])
    return venv_dir


def _create_tmp_dir() -> Path:
    """Create a temp directory and add it to _PATHS_TO_REMOVE"""
    tmp_dir = Path(tempfile.mkdtemp()).resolve()
    _PATHS_TO_REMOVE.add(tmp_dir)
    return tmp_dir


def before_scenario(context, scenario):
    """Environment preparation before each test is run."""
    kedro_install_venv_dir = create_new_venv()
    context.venv_dir = kedro_install_venv_dir
    context.env = os.environ.copy()

    if os.name == "posix":
        bin_dir = context.venv_dir / "bin"
    else:
        bin_dir = context.venv_dir / "Scripts"

    context.bin_dir = bin_dir
    context.pip = str(bin_dir / "pip")
    context.kedro = str(bin_dir / "kedro")
    context.python = str(bin_dir / "python")

    # Fix Pip version
    call(
        [
            context.python,
            "-m",
            "pip",
            "install",
            "-U",
            # pip==23.3 breaks dependency resolution
            "pip==23.3.1",
        ],
        env=context.env,
    )


    starters_root = Path(__file__).parents[1]
    starter_names = [
        "astro-airflow-iris",
        "databricks-iris",
        "spaceflights-pandas",
        "spaceflights-pyspark",
        "spaceflights-pandas-viz",
        "spaceflights-pyspark-viz",
    ]
    starters_paths = {
        starter: str(starters_root / starter) for starter in starter_names
    }
    context.starters_paths = starters_paths
    subprocess.run([context.python, "-m", "pip", "install", "-r", "test_requirements.txt"])
    context.temp_dir = Path(tempfile.mkdtemp()).resolve()
    _PATHS_TO_REMOVE.add(context.temp_dir)


def after_all(context):
    for path in _PATHS_TO_REMOVE:
        # ignore errors when attempting to remove already removed directories
        shutil.rmtree(path, ignore_errors=True)
