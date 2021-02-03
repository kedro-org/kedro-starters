import re
import sys

from click import secho

REPO_REGEX = r"^\w+(-*\w+)*$"
repo_name = '{{ cookiecutter.repo_name }}'
pkg_name = "{{ cookiecutter.python_package }}"

if not re.match(REPO_REGEX, repo_name):
    secho(f"`{repo_name}` is not a valid repository name. It must contain "
          f"only word symbols and/or hyphens, must also start and "
          f"end with alphanumeric symbol.", fg="red", err=True)
    # exits with status 1 to indicate failure
    sys.exit(1)

base_message = f"`{pkg_name}` is not a valid Python package name."
if not re.match(r"^[a-zA-Z_]", pkg_name):
    print(base_message + " It must start with a letter or underscore.")
    sys.exit(1)
if len(pkg_name) < 2:
    print(base_message + " It must be at least 2 characters long.")
    sys.exit(1)
if not re.match(r"^\w+$", pkg_name[1:]):
    print(
        base_message + " It must contain only letters, digits, and/or underscores."
    )
    sys.exit(1)

