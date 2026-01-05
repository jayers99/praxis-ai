"""Python CLI project template following hexagonal architecture."""

from __future__ import annotations


class TemplateFileData:
    """A file to be created from a template."""

    def __init__(self, path: str, content: str) -> None:
        """Initialize template file data."""
        self.path = path
        self.content = content


class PythonCliTemplate:
    """Python CLI project template."""

    def __init__(self) -> None:
        """Initialize template."""
        self.name = "python-cli"
        self.domain = "code"
        self.files = _get_template_files()


def get_python_cli_template() -> PythonCliTemplate:
    """Get the Python CLI template."""
    return PythonCliTemplate()


def _get_template_files() -> list[TemplateFileData]:
    """Generate all template files for python-cli."""
    return [
        # pyproject.toml
        TemplateFileData(
            path="pyproject.toml",
            content="""[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.poetry]
name = "{package_name}"
version = "0.1.0"
description = ""
authors = []
readme = "README.md"
packages = [{include = "{package_name}", from = "src"}]

[tool.poetry.dependencies]
python = ">=3.10"
typer = ">=0.9.0"
pydantic = ">=2.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
pytest-bdd = "^8.0"
ruff = "^0.8"
mypy = "^1.0"

[tool.poetry.scripts]
{package_name} = "{package_name}.cli:app"

[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "W"]

[tool.mypy]
python_version = "3.10"
strict = true
packages = ["{package_name}"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
""",
        ),
        # src/{package_name}/__init__.py
        TemplateFileData(
            path="src/{package_name}/__init__.py",
            content='"""Main package for {project_name}."""\n\n__version__ = "0.1.0"\n',
        ),
        # src/{package_name}/__main__.py
        TemplateFileData(
            path="src/{package_name}/__main__.py",
            content="""\"\"\"Allow running as python -m {package_name}.\"\"\"

from {package_name}.cli import app

if __name__ == "__main__":
    app()
""",
        ),
        # src/{package_name}/cli.py
        TemplateFileData(
            path="src/{package_name}/cli.py",
            content="""\"\"\"CLI interface - thin Typer layer.\"\"\"

from __future__ import annotations

import typer

from {package_name} import __version__
from {package_name}.application.hello_service import say_hello

app = typer.Typer(
    name="{package_name}",
    help="{project_name} CLI",
    no_args_is_help=True,
)


def version_callback(value: bool) -> None:
    \"\"\"Print version and exit.\"\"\"
    if value:
        typer.echo(f"{package_name} """
            + """{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    \"\"\"{project_name} CLI.\"\"\"


@app.command(name="hello")
def hello_cmd(
    name: str = typer.Argument("World", help="Name to greet."),
) -> None:
    \"\"\"Say hello to someone.\"\"\"
    message = say_hello(name)
    typer.echo(message)


if __name__ == "__main__":
    app()
""",
        ),
        # src/{package_name}/domain/__init__.py
        TemplateFileData(
            path="src/{package_name}/domain/__init__.py",
            content='"""Domain layer - pure business logic."""\n',
        ),
        # src/{package_name}/domain/models.py
        TemplateFileData(
            path="src/{package_name}/domain/models.py",
            content="""\"\"\"Domain models.\"\"\"

from __future__ import annotations

from pydantic import BaseModel


class Greeting(BaseModel):
    \"\"\"A greeting message.\"\"\"

    recipient: str
    message: str
""",
        ),
        # src/{package_name}/application/__init__.py
        TemplateFileData(
            path="src/{package_name}/application/__init__.py",
            content='"""Application layer - use cases and orchestration."""\n',
        ),
        # src/{package_name}/application/hello_service.py
        TemplateFileData(
            path="src/{package_name}/application/hello_service.py",
            content="""\"\"\"Hello service - business logic for greetings.\"\"\"

from __future__ import annotations

from {package_name}.domain.models import Greeting


def say_hello(name: str) -> str:
    \"\"\"Generate a greeting message.

    Args:
        name: Name of the person to greet.

    Returns:
        Greeting message.
    \"\"\"
    greeting = Greeting(recipient=name, message=f"Hello, """
            + """{name}!")
    return greeting.message
""",
        ),
        # src/{package_name}/infrastructure/__init__.py
        TemplateFileData(
            path="src/{package_name}/infrastructure/__init__.py",
            content='"""Infrastructure layer - external integrations."""\n',
        ),
        # tests/__init__.py
        TemplateFileData(
            path="tests/__init__.py",
            content="",
        ),
        # tests/conftest.py
        TemplateFileData(
            path="tests/conftest.py",
            content="""\"\"\"Pytest configuration and fixtures.\"\"\"

import pytest
from typer.testing import CliRunner


@pytest.fixture
def cli_runner() -> CliRunner:
    \"\"\"Provide a Typer CLI test runner.\"\"\"
    return CliRunner()
""",
        ),
        # tests/features/__init__.py
        TemplateFileData(
            path="tests/features/__init__.py",
            content="",
        ),
        # tests/features/hello.feature
        TemplateFileData(
            path="tests/features/hello.feature",
            content="""Feature: Hello command
  As a user
  I want to run a hello command
  So that I can verify the CLI works

  Scenario: Say hello to the world
    When I run the hello command with no arguments
    Then the output should contain "Hello, World!"

  Scenario: Say hello to a specific person
    When I run the hello command with name "Alice"
    Then the output should contain "Hello, Alice!"
""",
        ),
        # tests/step_defs/__init__.py
        TemplateFileData(
            path="tests/step_defs/__init__.py",
            content="",
        ),
        # tests/step_defs/test_hello.py
        TemplateFileData(
            path="tests/step_defs/test_hello.py",
            content="""\"\"\"Step definitions for hello.feature.\"\"\"

from pytest_bdd import given, parsers, scenarios, then, when
from typer.testing import CliRunner

from {package_name}.cli import app

scenarios("../features/hello.feature")


@when("I run the hello command with no arguments", target_fixture="result")
def run_hello_no_args(cli_runner: CliRunner) -> object:
    \"\"\"Run hello command with no arguments.\"\"\"
    return cli_runner.invoke(app, ["hello"])


@when(
    parsers.parse('I run the hello command with name "{name}"'),
    target_fixture="result",
)
def run_hello_with_name(cli_runner: CliRunner, name: str) -> object:
    \"\"\"Run hello command with a name.\"\"\"
    return cli_runner.invoke(app, ["hello", name])


@then(parsers.parse('the output should contain "{text}"'))
def output_contains(result: object, text: str) -> None:
    \"\"\"Check that output contains expected text.\"\"\"
    assert hasattr(result, "output")
    assert text in result.output
""",
        ),
        # tests/test_hello_service.py
        TemplateFileData(
            path="tests/test_hello_service.py",
            content="""\"\"\"Unit tests for hello service.\"\"\"

from {package_name}.application.hello_service import say_hello


def test_say_hello_returns_greeting() -> None:
    \"\"\"Test that say_hello returns a greeting message.\"\"\"
    result = say_hello("Alice")
    assert result == "Hello, Alice!"


def test_say_hello_with_different_name() -> None:
    \"\"\"Test that say_hello works with different names.\"\"\"
    result = say_hello("Bob")
    assert result == "Hello, Bob!"
""",
        ),
        # README.md
        TemplateFileData(
            path="README.md",
            content="""# {project_name}

A Python CLI tool built with hexagonal architecture.

## Installation

```bash
poetry install
```

## Usage

```bash
poetry run {package_name} hello
poetry run {package_name} hello Alice
```

## Development

Run tests:
```bash
poetry run pytest
```

Lint:
```bash
poetry run ruff check .
```

Type check:
```bash
poetry run mypy .
```

## Architecture

This project follows hexagonal architecture:
- `domain/` - Pure business logic, no external dependencies
- `application/` - Use cases and orchestration
- `infrastructure/` - External integrations
- `cli.py` - Thin CLI adapter (Typer)

## Testing

Uses BDD (Behavior-Driven Development) with pytest-bdd:
- Feature files in `tests/features/`
- Step definitions in `tests/step_defs/`
""",
        ),
        # .gitignore
        TemplateFileData(
            path=".gitignore",
            content="""# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/

# MyPy
.mypy_cache/
.dmypy.json
dmypy.json

# Ruff
.ruff_cache/
""",
        ),
    ]
