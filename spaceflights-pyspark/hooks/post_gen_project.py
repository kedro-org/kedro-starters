from pathlib import Path

from kedro.templates.project.hooks.utils import (

    setup_template_add_ons,
    sort_requirements,
)
from kedro.framework.cli.starters import _parse_add_ons_input


def main(selected_add_ons):
    current_dir = Path.cwd()
    requirements_file_path = current_dir / "requirements.txt"
    pyproject_file_path = current_dir / "pyproject.toml"
    python_package_name = '{{ cookiecutter.python_package }}'
    example_pipeline = "{{ cookiecutter.example_pipeline }}"

    # Handle template directories and requirements according to selected add-ons
    setup_template_add_ons(selected_add_ons, requirements_file_path, pyproject_file_path, python_package_name, example_pipeline)

    # Sort requirements.txt file in alphabetical order
    sort_requirements(requirements_file_path)


if __name__ == "__main__":
    # Get the selected add-ons from cookiecutter
    selected_add_ons = "{{ cookiecutter.add_ons }}"

    # Execute the script only if the Pyspark add-on is selected.
    # This ensures the script doesn't run with kedro new --starter but only with the add-ons flow option.
    if "Pyspark" in selected_add_ons:
        main(selected_add_ons)
