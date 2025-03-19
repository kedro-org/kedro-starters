from pathlib import Path

from kedro.templates.project.hooks.utils import (

    setup_template_tools,
    sort_requirements,
)


def main(selected_tools):
    current_dir = Path.cwd()
    requirements_file_path = current_dir / "requirements.txt"
    pyproject_file_path = current_dir / "pyproject.toml"
    python_package_name = '{{ cookiecutter.python_package }}'
    example_pipeline = "{{ cookiecutter.example_pipeline }}"

    # Handle template directories and requirements according to selected tools
    setup_template_tools(selected_tools, requirements_file_path, pyproject_file_path, python_package_name, example_pipeline)

    # Sort requirements.txt file in alphabetical order
    sort_requirements(requirements_file_path)


if __name__ == "__main__":
    # Get the selected tools from cookiecutter
    selected_tools = "{{ cookiecutter.tools }}"

    # Execute the script only if the PySpark and Kedro-Viz tool is selected.
    # This ensures the script doesn't run with kedro new --starter but only with the tools flow option.
    if "PySpark" in selected_tools and "Kedro Viz" in selected_tools:
        main(selected_tools)
