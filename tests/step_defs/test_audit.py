"""Step definitions for audit.feature."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pytest_bdd import given, parsers, scenarios, when
from typer.testing import CliRunner

from praxis.cli import app

scenarios("../features/audit.feature")


@given("a Python CLI project with all checks passing")
def python_cli_project_passing(tmp_path: Path, context: dict[str, Any]) -> None:
    """Create a Python CLI project that passes all checks."""
    context["project_root"] = tmp_path

    # praxis.yaml
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: code
stage: execute
privacy_level: personal
environment: Home
"""
    )

    # pyproject.toml with all dependencies
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        """[tool.poetry]
name = "test-project"
version = "0.1.0"

[tool.poetry.scripts]
test-cli = "test_project.cli:app"

[tool.poetry.dependencies]
python = "^3.11"
typer = "^0.9.0"

[tool.poetry.group.dev.dependencies]
ruff = "^0.1.0"
mypy = "^1.0.0"
pytest-bdd = "^7.0.0"
"""
    )

    # src structure
    pkg = tmp_path / "src" / "test_project"
    pkg.mkdir(parents=True)
    (pkg / "__init__.py").write_text("")
    (pkg / "__main__.py").write_text("from .cli import app\napp()")
    (pkg / "cli.py").write_text("import typer\napp = typer.Typer()")

    # Hexagonal dirs
    (pkg / "domain").mkdir()
    (pkg / "domain" / "__init__.py").write_text("")
    (pkg / "application").mkdir()
    (pkg / "application" / "__init__.py").write_text("")
    (pkg / "infrastructure").mkdir()
    (pkg / "infrastructure" / "__init__.py").write_text("")

    # BDD tests
    features = tmp_path / "tests" / "features"
    features.mkdir(parents=True)
    (features / "example.feature").write_text("Feature: Example")


@given("a code project without pyproject.toml")
def code_project_no_pyproject(tmp_path: Path, context: dict[str, Any]) -> None:
    """Create a code project without pyproject.toml."""
    context["project_root"] = tmp_path

    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: code
stage: capture
privacy_level: personal
environment: Home
"""
    )


@given(parsers.parse('a project with domain "{domain}"'))
def project_with_domain(
    tmp_path: Path, context: dict[str, Any], domain: str
) -> None:
    """Create a project with specified domain."""
    context["project_root"] = tmp_path

    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        f"""domain: {domain}
stage: capture
privacy_level: personal
environment: Home
"""
    )


@given("a project with invalid praxis.yaml")
def invalid_praxis_yaml(tmp_path: Path, context: dict[str, Any]) -> None:
    """Create a project with invalid praxis.yaml."""
    context["project_root"] = tmp_path

    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: invalid_domain
stage: capture
"""
    )


@when("I run praxis audit")
def run_audit(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run praxis audit command."""
    project_root = context["project_root"]
    result = cli_runner.invoke(app, ["audit", str(project_root)])
    context["result"] = result


@when("I run praxis audit --strict")
def run_audit_strict(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run praxis audit with strict mode."""
    project_root = context["project_root"]
    result = cli_runner.invoke(app, ["audit", str(project_root), "--strict"])
    context["result"] = result


@when("I run praxis audit --json")
def run_audit_json(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run praxis audit with JSON output."""
    project_root = context["project_root"]
    result = cli_runner.invoke(app, ["audit", str(project_root), "--json"])
    context["result"] = result
