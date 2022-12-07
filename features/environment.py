"""Behave environment setup commands"""

import os
import shutil
import subprocess
import tempfile
import venv
from pathlib import Path

from typing import Set

_PATHS_TO_REMOVE: Set[Path] = set()


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

    if os.name == "posix":
        bin_dir = context.venv_dir / "bin"
    else:
        bin_dir = context.venv_dir / "Scripts"

    context.bin_dir = bin_dir
    context.pip = str(bin_dir / "pip")
    context.kedro = str(bin_dir / "kedro")
    context.python = str(bin_dir / "python")

    starters_root = Path(__file__).parents[1]
    starter_names = [
        "astro-airflow-iris",
        "pandas-iris",
        "pyspark",
        "pyspark-iris",
        "spaceflights",
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
