"""Step definitions for templates.feature."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pytest_bdd import given, parsers, scenarios, then, when
from typer.testing import CliRunner

from praxis.cli import app

scenarios("../features/templates.feature")


@given(parsers.parse('a project with domain "{domain}" at stage "{stage}"'))
def project_with_domain_and_stage(
    tmp_path: Path, context: dict[str, Any], domain: str, stage: str
) -> None:
    """Create a project with specified domain and stage."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        f"""domain: {domain}
stage: {stage}
privacy_level: personal
environment: Home
"""
    )


@given(parsers.parse('"{filename}" already exists'))
def file_already_exists(context: dict[str, Any], filename: str) -> None:
    """Create a file that already exists."""
    project_root = context["project_root"]
    file_path = project_root / filename
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text("existing content")
    context["original_content"] = "existing content"


@given(parsers.parse('"{filename}" does not exist'))
def file_does_not_exist(context: dict[str, Any], filename: str) -> None:
    """Ensure file does not exist."""
    project_root = context["project_root"]
    file_path = project_root / filename
    if file_path.exists():
        file_path.unlink()


@when("I run praxis templates render --stage formalize")
def run_templates_render_formalize(
    cli_runner: CliRunner, context: dict[str, Any]
) -> None:
    """Run praxis templates render with --stage formalize."""
    project_root = context["project_root"]
    result = cli_runner.invoke(
        app,
        ["templates", "render", str(project_root), "--stage", "formalize"],
    )
    context["result"] = result


@when("I run praxis validate")
def run_validate(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run praxis validate."""
    project_root = context["project_root"]
    result = cli_runner.invoke(
        app,
        ["validate", str(project_root)],
    )
    context["result"] = result


@when("I run praxis status")
def run_status(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run praxis status."""
    project_root = context["project_root"]
    result = cli_runner.invoke(
        app,
        ["status", str(project_root)],
    )
    context["result"] = result


@then(parsers.parse('"{filename}" should be created'))
def file_should_be_created(context: dict[str, Any], filename: str) -> None:
    """Verify file was created."""
    project_root = context["project_root"]
    file_path = project_root / filename
    assert file_path.exists(), f"Expected {filename} to be created"


@then("the existing file should not be modified")
def existing_file_not_modified(context: dict[str, Any]) -> None:
    """Verify existing file was not modified."""
    project_root = context["project_root"]
    file_path = project_root / "docs" / "brief.md"
    current_content = file_path.read_text()
    assert (
        current_content == context["original_content"]
    ), "File was modified when it should have been skipped"
