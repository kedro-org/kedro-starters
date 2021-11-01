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
    """Environment preparation before each test is run."""
    context.venv_dir = create_new_venv()
    bin_dir = context.venv_dir / "bin"
    context.pip = str(bin_dir / "pip")
    context.python = str(bin_dir / "python")
    context.kedro = str(bin_dir / "kedro")
    starters_root = Path(__file__).parents[1]
    starter_names = [
        "astro-iris",
        "pandas-iris",
        "pyspark",
        "pyspark-iris",
        "spaceflights",
    ]
    starters_paths = {
        starter: str(starters_root / starter) for starter in starter_names
    }
    context.starters_paths = starters_paths
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
