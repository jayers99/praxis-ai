"""Step definitions for stage.feature."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pytest_bdd import given, parsers, scenarios, then, when
from typer.testing import CliRunner

from praxis.cli import app

scenarios("../features/stage.feature")


@given(parsers.parse('a project at stage "{stage}"'))
def project_at_stage(tmp_path: Path, context: dict[str, Any], stage: str) -> None:
    """Create a project at the given stage."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        f"""domain: code
stage: {stage}
privacy_level: personal
environment: Home
"""
    )


@given(parsers.parse('a project at stage "{stage}" with docs/sod.md'))
def project_at_stage_with_sod(
    tmp_path: Path, context: dict[str, Any], stage: str
) -> None:
    """Create a project at the given stage with SOD artifact."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        f"""domain: code
stage: {stage}
privacy_level: personal
environment: Home
"""
    )
    # Create SOD
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    sod = docs_dir / "sod.md"
    sod.write_text("# Solution Overview Document\n")


@given(parsers.parse('a project at stage "{stage}" with CLAUDE.md'))
def project_at_stage_with_claude_md(
    tmp_path: Path, context: dict[str, Any], stage: str
) -> None:
    """Create a project at the given stage with CLAUDE.md."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        f"""domain: code
stage: {stage}
privacy_level: personal
environment: Home
"""
    )
    # Create CLAUDE.md with stage line
    claude_md = tmp_path / "CLAUDE.md"
    claude_md.write_text(
        f"""# Test Project

## Current State

- **Domain:** code
- **Stage:** {stage}
- **Privacy:** personal
"""
    )


@when(parsers.parse('I run praxis stage "{new_stage}"'))
def run_stage(
    cli_runner: CliRunner,
    context: dict[str, Any],
    new_stage: str,
) -> None:
    """Run praxis stage command."""
    project_root = context["project_root"]
    result = cli_runner.invoke(app, ["stage", new_stage, str(project_root)])
    context["result"] = result


@then(parsers.parse('praxis.yaml should have stage "{stage}"'))
def check_praxis_yaml_stage(context: dict[str, Any], stage: str) -> None:
    """Verify praxis.yaml has the expected stage."""
    project_root = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"
    content = yaml.safe_load(praxis_yaml.read_text())
    assert content["stage"] == stage, (
        f"Expected stage '{stage}', got '{content.get('stage')}'"
    )


@then(parsers.parse('CLAUDE.md should show stage "{stage}"'))
def check_claude_md_stage(context: dict[str, Any], stage: str) -> None:
    """Verify CLAUDE.md has the expected stage."""
    project_root = context["project_root"]
    claude_md = project_root / "CLAUDE.md"
    content = claude_md.read_text()
    assert f"**Stage:** {stage}" in content, (
        f"Expected '**Stage:** {stage}' in CLAUDE.md. Got: {content}"
    )
