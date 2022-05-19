"""Behave environment setup commands"""

import os
import shutil
import stat
import subprocess
import tempfile
import venv
from pathlib import Path
from typing import Set

_PATHS_TO_REMOVE: Set[Path] = set()

from features.steps.sh_run import run

# def create_new_venv() -> Path:
#     """Create a new venv.
#     Returns:
#         path to created venv
#     """
#     # Create venv
#     venv_dir = Path(tempfile.mkdtemp()).resolve()
#     venv.main([str(venv_dir)])
#     return venv_dir

def call(cmd, env, verbose=False):
    res = run(cmd, env=env)
    if res.returncode or verbose:
        print(">", " ".join(cmd))
        print(res.stdout)
        print(res.stderr)
    assert res.returncode == 0

def before_scenario(context, scenario):
    """Environment preparation before each test is run."""
    # make a venv
    kedro_install_venv_dir = _create_new_venv()
    context.venv_dir = kedro_install_venv_dir
    context = _setup_context_with_venv(context, kedro_install_venv_dir)
    context.temp_dir = Path(tempfile.mkdtemp()).resolve()
    _PATHS_TO_REMOVE.add(context.temp_dir)
    


# def after_scenario(context, scenario):
#     rmtree(str(context.temp_dir))
#     rmtree(str(context.venv_dir))


def rmtree(top):
    if os.name != "posix":
        for root, _, files in os.walk(top, topdown=False):
            for name in files:
                os.chmod(os.path.join(root, name), stat.S_IWUSR)
    shutil.rmtree(top)

def _setup_context_with_venv(context, venv_dir):
    context.venv_dir = venv_dir
    # note the locations of some useful stuff
    # this is because exe resolution in subprocess doesn't respect a passed env
    if os.name == "posix":
        bin_dir = context.venv_dir / "bin"
        path_sep = ":"
    else:
        bin_dir = context.venv_dir / "Scripts"
        path_sep = ";"
    context.bin_dir = bin_dir
    context.pip = str(bin_dir / "pip")
    context.python = str(bin_dir / "python")
    context.kedro = str(bin_dir / "kedro")

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
    subprocess.run([context.pip, "install", "-r", "test_requirements.txt"])
    
    ##
    # clone the environment, remove any condas and venvs and insert our venv
    context.env = os.environ.copy()
    path = context.env["PATH"].split(path_sep)
    path = [p for p in path if not (Path(p).parent / "pyvenv.cfg").is_file()]
    path = [p for p in path if not (Path(p).parent / "conda-meta").is_dir()]
    path = [str(bin_dir)] + path
    # Activate environment
    context.env["PATH"] = path_sep.join(path)
    # Windows thinks the pip version check warning is a failure
    # so disable it here.
    context.env["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"

    call(
        [
            context.python,
            "-m",
            "pip",
            "install",
            "-U",
            "pip>=21.2",
            "setuptools>=38.0",
            "cookiecutter>=1.7.2",
            "wheel",
            "botocore",
            "PyYAML>=4.2, <6.0",
            "click<9.0",
        ],
        env=context.env,
    )

    call([context.python, "-m", "pip", "install", "."], env=context.env)
    return context
# -- pasting viz environment -- 

"""Behave environment setup commands"""


# _PATHS_TO_REMOVE: Set[Path] = set()


def after_scenario(context, scenario):
    for path in _PATHS_TO_REMOVE:
        # ignore errors when attempting to remove already removed directories
        shutil.rmtree(path, ignore_errors=True)


def _create_new_venv() -> Path:
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