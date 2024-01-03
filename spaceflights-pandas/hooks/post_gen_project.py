from pathlib import Path

from kedro.templates.project.hooks.utils import (

    setup_template_tools,
    sort_requirements,
)


def main(example_pipeline):
    current_dir = Path.cwd()
    requirements_file_path = current_dir / "requirements.txt"
    pyproject_file_path = current_dir / "pyproject.toml"
    python_package_name = '{{ cookiecutter.python_package }}'
    selected_tools = "{{ cookiecutter.tools }}"

    # Handle template directories and requirements according to selected tools
    setup_template_tools(selected_tools, requirements_file_path, pyproject_file_path, python_package_name, example_pipeline)

    # Sort requirements.txt file in alphabetical order
    sort_requirements(requirements_file_path)


if __name__ == "__main__":
    # Get the selected tools from cookiecutter
    example_pipeline = "{{ cookiecutter.example_pipeline }}"

    # Ensure the script doesn't run with kedro new --starter but only with examples selected.
    # User cannot specify both starter and example.
    if example_pipeline == "True":
        main(example_pipeline)
