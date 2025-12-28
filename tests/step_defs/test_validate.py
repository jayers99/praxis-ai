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


@when("I run praxis validate")
def run_validate(
    cli_runner: CliRunner,
    context: dict[str, Any],
) -> None:
    """Run the praxis validate command."""
    project_root = context["project_root"]
    result = cli_runner.invoke(app, ["validate", str(project_root)])
    context["result"] = result


@then(parsers.parse("the exit code should be {code:d}"))
def check_exit_code(context: dict[str, Any], code: int) -> None:
    """Verify the exit code."""
    result = context["result"]
    assert result.exit_code == code, (
        f"Expected exit code {code}, got {result.exit_code}. "
        f"Output: {result.output}"
    )


@then(parsers.parse('the output should contain "{text}"'))
def check_output_contains(context: dict[str, Any], text: str) -> None:
    """Verify the output contains expected text."""
    result = context["result"]
    assert text in result.output, (
        f"Expected '{text}' in output. Got: {result.output}"
    )
