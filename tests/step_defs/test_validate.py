"""Step definitions for validate.feature."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pytest_bdd import given, parsers, scenarios, then, when
from typer.testing import CliRunner

from praxis.cli import app

scenarios("../features/validate.feature")


@given(parsers.parse('a project with domain "{domain}" and stage "{stage}"'))
def create_project(
    tmp_path: Path,
    context: dict[str, Any],
    domain: str,
    stage: str,
) -> None:
    """Create a temporary project with praxis.yaml."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        f"""domain: {domain}
stage: {stage}
privacy_level: personal
environment: Home
"""
    )


@given("a docs/sod.md file exists")
def create_sod(context: dict[str, Any]) -> None:
    """Create the SOD artifact file."""
    project_root = context["project_root"]
    docs_dir = project_root / "docs"
    docs_dir.mkdir(exist_ok=True)
    sod_path = docs_dir / "sod.md"
    sod_path.write_text("# Solution Overview Document\n")


@given("no docs/sod.md file exists")
def ensure_no_sod(context: dict[str, Any]) -> None:
    """Ensure no SOD file exists (no-op, just documenting the state)."""
    project_root = context["project_root"]
    sod_path = project_root / "docs" / "sod.md"
    if sod_path.exists():
        sod_path.unlink()


@given("a docs/brief.md file exists")
def create_brief(context: dict[str, Any]) -> None:
    """Create the brief artifact file."""
    project_root = context["project_root"]
    docs_dir = project_root / "docs"
    docs_dir.mkdir(exist_ok=True)
    brief_path = docs_dir / "brief.md"
    brief_path.write_text("# Creative Brief\n")


@given("no docs/brief.md file exists")
def ensure_no_brief(context: dict[str, Any]) -> None:
    """Ensure no brief file exists (no-op, just documenting the state)."""
    project_root = context["project_root"]
    brief_path = project_root / "docs" / "brief.md"
    if brief_path.exists():
        brief_path.unlink()


@given("a docs/plan.md file exists")
def create_plan(context: dict[str, Any]) -> None:
    """Create the plan artifact file."""
    project_root = context["project_root"]
    docs_dir = project_root / "docs"
    docs_dir.mkdir(exist_ok=True)
    plan_path = docs_dir / "plan.md"
    plan_path.write_text("# Learning Plan\n")


@given("no docs/plan.md file exists")
def ensure_no_plan(context: dict[str, Any]) -> None:
    """Ensure no plan file exists (no-op, just documenting the state)."""
    project_root = context["project_root"]
    plan_path = project_root / "docs" / "plan.md"
    if plan_path.exists():
        plan_path.unlink()


@given("a valid project with passing tests")
def create_valid_project_with_tests(
    tmp_path: Path,
    context: dict[str, Any],
) -> None:
    """Create a valid project with passing tests, lint, and types."""
    context["project_root"] = tmp_path

    # Create praxis.yaml
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: code
stage: explore
privacy_level: personal
environment: Home
"""
    )

    # Create pyproject.toml for poetry
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        """[tool.poetry]
name = "test-project"
version = "0.1.0"
description = "Test"
authors = ["Test <test@test.com>"]

[tool.poetry.dependencies]
python = "^3.11"

[tool.ruff]
line-length = 88

[tool.mypy]
python_version = "3.11"
files = ["src"]

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""
    )

    # Create a simple passing test
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    test_file = tests_dir / "test_example.py"
    test_file.write_text(
        """def test_example():
    assert True
"""
    )

    # Create src directory for mypy
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    init_file = src_dir / "__init__.py"
    init_file.write_text("")


@given(parsers.parse("a valid project with coverage threshold {threshold:d}"))
def create_valid_project_with_coverage(
    tmp_path: Path,
    context: dict[str, Any],
    threshold: int,
) -> None:
    """Create a valid project with coverage threshold configured."""
    context["project_root"] = tmp_path

    # Create praxis.yaml with coverage_threshold
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        f"""domain: code
stage: explore
privacy_level: personal
environment: Home
coverage_threshold: {threshold}
"""
    )

    # Create pyproject.toml for poetry
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        """[tool.poetry]
name = "test-project"
version = "0.1.0"
description = "Test"
authors = ["Test <test@test.com>"]

[tool.poetry.dependencies]
python = "^3.11"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
pytest-cov = "^4.0"

[tool.ruff]
line-length = 88

[tool.mypy]
python_version = "3.11"
files = ["src"]

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""
    )

    # Create a simple module with a function
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    init_file = src_dir / "__init__.py"
    init_file.write_text("")

    module_file = src_dir / "example.py"
    module_file.write_text(
        """def add(a: int, b: int) -> int:
    return a + b
"""
    )

    # Create a test that covers the function
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    test_file = tests_dir / "test_example.py"
    test_file.write_text(
        """from src.example import add

def test_add():
    assert add(1, 2) == 3
"""
    )


@when("I run praxis validate")
def run_validate(
    cli_runner: CliRunner,
    context: dict[str, Any],
) -> None:
    """Run the praxis validate command."""
    project_root = context["project_root"]
    result = cli_runner.invoke(app, ["validate", str(project_root)])
    context["result"] = result


@when(parsers.parse("I run praxis validate {flags}"))
def run_validate_with_flags(
    cli_runner: CliRunner,
    context: dict[str, Any],
    flags: str,
) -> None:
    """Run the praxis validate command with flags."""
    project_root = context["project_root"]
    args = ["validate", str(project_root)] + flags.split()
    result = cli_runner.invoke(app, args)
    context["result"] = result


@then(parsers.parse('the JSON output should contain "{key}"'))
def check_json_contains_key(context: dict[str, Any], key: str) -> None:
    """Verify the JSON output contains the specified key."""
    import json

    result = context["result"]
    try:
        output_data = json.loads(result.output)
        assert key in output_data, (
            f"Expected key '{key}' in JSON output. Got keys: {list(output_data.keys())}"
        )
    except json.JSONDecodeError as e:
        raise AssertionError(f"Invalid JSON output: {e}. Output: {result.output}")


@then(parsers.parse('the JSON version should be "{version}"'))
def check_json_version(context: dict[str, Any], version: str) -> None:
    """Verify the JSON output version field matches expected value."""
    import json

    result = context["result"]
    try:
        output_data = json.loads(result.output)
        assert "version" in output_data, (
            f"Expected 'version' key in JSON output. "
            f"Got keys: {list(output_data.keys())}"
        )
        assert output_data["version"] == version, (
            f"Expected version '{version}', got '{output_data['version']}'"
        )
    except json.JSONDecodeError as e:
        raise AssertionError(f"Invalid JSON output: {e}. Output: {result.output}")

