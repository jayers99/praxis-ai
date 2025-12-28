"""Step definitions for status.feature."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pytest_bdd import given, scenarios, when
from typer.testing import CliRunner

from praxis.cli import app

scenarios("../features/status.feature")


@given('a valid project at stage "capture"')
def valid_project_capture(tmp_path: Path, context: dict[str, Any]) -> None:
    """Create a valid project at capture stage."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: code
stage: capture
privacy_level: personal
environment: Home
"""
    )


@given('a valid project at stage "execute" with docs/sod.md')
def valid_project_execute_with_sod(tmp_path: Path, context: dict[str, Any]) -> None:
    """Create a valid project at execute stage with SOD."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: code
stage: execute
privacy_level: personal
environment: Home
"""
    )
    # Create SOD artifact
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    sod = docs_dir / "sod.md"
    sod.write_text("# Solution Overview Document\n")


@given('a valid project at stage "execute"')
def valid_project_execute(tmp_path: Path, context: dict[str, Any]) -> None:
    """Create a valid project at execute stage (no SOD)."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: code
stage: execute
privacy_level: personal
environment: Home
"""
    )


@given('a valid project at stage "close"')
def valid_project_close(tmp_path: Path, context: dict[str, Any]) -> None:
    """Create a valid project at close stage."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: code
stage: close
privacy_level: personal
environment: Home
"""
    )


@given("a project with invalid praxis.yaml")
def invalid_project(tmp_path: Path, context: dict[str, Any]) -> None:
    """Create a project with invalid praxis.yaml."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: invalid_domain
stage: capture
"""
    )


@when("I run praxis status")
def run_status(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run praxis status command."""
    project_root = context["project_root"]
    result = cli_runner.invoke(app, ["status", str(project_root)])
    context["result"] = result
