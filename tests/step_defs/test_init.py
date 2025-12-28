"""Step definitions for init.feature."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pytest_bdd import given, parsers, scenarios, then, when
from typer.testing import CliRunner

from praxis.cli import app

scenarios("../features/init.feature")


@given("an empty directory")
def empty_directory(tmp_path: Path, context: dict[str, Any]) -> None:
    """Use the pytest tmp_path as an empty project directory."""
    context["project_root"] = tmp_path


@given("a directory with existing praxis.yaml")
def directory_with_praxis_yaml(tmp_path: Path, context: dict[str, Any]) -> None:
    """Create a directory with an existing praxis.yaml."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: write
stage: capture
privacy_level: public
environment: Home
"""
    )
    context["original_content"] = praxis_yaml.read_text()


@when(parsers.parse('I run praxis init with domain "{domain}" and privacy "{privacy}"'))
def run_init_with_flags(
    cli_runner: CliRunner,
    context: dict[str, Any],
    domain: str,
    privacy: str,
) -> None:
    """Run praxis init with domain and privacy flags."""
    project_root = context["project_root"]
    result = cli_runner.invoke(
        app,
        ["init", str(project_root), "--domain", domain, "--privacy", privacy],
    )
    context["result"] = result


@when("I run praxis init with --force")
def run_init_with_force(
    cli_runner: CliRunner,
    context: dict[str, Any],
) -> None:
    """Run praxis init with --force flag."""
    project_root = context["project_root"]
    result = cli_runner.invoke(
        app,
        [
            "init", str(project_root),
            "--domain", "code", "--privacy", "personal", "--force",
        ],
    )
    context["result"] = result


@then(parsers.parse('praxis.yaml should exist with domain "{domain}"'))
def check_praxis_yaml_domain(context: dict[str, Any], domain: str) -> None:
    """Verify praxis.yaml exists with the expected domain."""
    project_root = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"
    assert praxis_yaml.exists(), "praxis.yaml should exist"
    content = yaml.safe_load(praxis_yaml.read_text())
    assert content["domain"] == domain, (
        f"Expected domain '{domain}', got '{content.get('domain')}'"
    )


@then("CLAUDE.md should exist")
def check_claude_md_exists(context: dict[str, Any]) -> None:
    """Verify CLAUDE.md exists."""
    project_root = context["project_root"]
    claude_md = project_root / "CLAUDE.md"
    assert claude_md.exists(), "CLAUDE.md should exist"


@then("docs/capture.md should exist")
def check_capture_md_exists(context: dict[str, Any]) -> None:
    """Verify docs/capture.md exists."""
    project_root = context["project_root"]
    capture_md = project_root / "docs" / "capture.md"
    assert capture_md.exists(), "docs/capture.md should exist"


@then("praxis.yaml should be updated")
def check_praxis_yaml_updated(context: dict[str, Any]) -> None:
    """Verify praxis.yaml was updated (different from original)."""
    project_root = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"
    current_content = praxis_yaml.read_text()
    # The domain should now be "code" instead of "write"
    content = yaml.safe_load(current_content)
    assert content["domain"] == "code", (
        f"Expected domain 'code' after --force, got '{content.get('domain')}'"
    )
