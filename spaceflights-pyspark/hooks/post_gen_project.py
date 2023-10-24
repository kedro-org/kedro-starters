from pathlib import Path

from kedro.templates.project.hooks.utils import (
    parse_add_ons_input,
    setup_template_add_ons,
    sort_requirements,
)


def main(selected_add_ons_list):
    current_dir = Path.cwd()
    requirements_file_path = current_dir / "requirements.txt"
    pyproject_file_path = current_dir / "pyproject.toml"
    python_package_name = '{{ cookiecutter.python_package }}'

    # Handle template directories and requirements according to selected add-ons
    setup_template_add_ons(selected_add_ons_list, requirements_file_path, pyproject_file_path, python_package_name)

    # Sort requirements.txt file in alphabetical order
    sort_requirements(requirements_file_path)


if __name__ == "__main__":
    # Get the selected add-ons from cookiecutter
    selected_add_ons = "{{ cookiecutter.add_ons }}"
    # Parse the add-ons to get a list
    selected_add_ons_list = parse_add_ons_input(selected_add_ons)

    # Execute the script only if the PySpark add-on (represented by "6") is selected.
    # This ensures the script doesn't run with kedro new --starter but only with the add-ons flow option.
    if "6" in selected_add_ons_list:
        main(selected_add_ons_list)
