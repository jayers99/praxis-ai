"""Step definitions for new.feature."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pytest
import yaml
from pytest_bdd import given, parsers, scenarios, then, when
from typer.testing import CliRunner

from praxis.cli import app

scenarios("../features/new.feature")


@given("an empty directory")
def empty_directory(tmp_path: Path, context: dict[str, Any]) -> None:
    """Use the pytest tmp_path as an empty parent directory."""
    context["project_root"] = tmp_path


@then(parsers.parse('praxis.yaml should exist with domain "{domain}"'))
def check_praxis_yaml_domain(context: dict[str, Any], domain: str) -> None:
    """Verify praxis.yaml exists with the expected domain."""
    project_root: Path = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"
    assert praxis_yaml.exists(), "praxis.yaml should exist"
    content = yaml.safe_load(praxis_yaml.read_text())
    assert content["domain"] == domain, (
        f"Expected domain '{domain}', got '{content.get('domain')}'"
    )


@then("CLAUDE.md should exist")
def check_claude_md_exists(context: dict[str, Any]) -> None:
    """Verify CLAUDE.md exists."""
    project_root: Path = context["project_root"]
    claude_md = project_root / "CLAUDE.md"
    assert claude_md.exists(), "CLAUDE.md should exist"


@then("docs/capture.md should exist")
def check_capture_md_exists(context: dict[str, Any]) -> None:
    """Verify docs/capture.md exists."""
    project_root: Path = context["project_root"]
    capture_md = project_root / "docs" / "capture.md"
    assert capture_md.exists(), "docs/capture.md should exist"


@given("PRAXIS_HOME is not set")
def praxis_home_not_set(context: dict[str, Any]) -> None:
    """Unset PRAXIS_HOME for this scenario."""
    context["original_praxis_home"] = os.environ.get("PRAXIS_HOME")
    if "PRAXIS_HOME" in os.environ:
        del os.environ["PRAXIS_HOME"]


@when(
    parsers.parse(
        'I run praxis new "{name}" with domain "{domain}" and privacy "{privacy}"'
    )
)
def run_new_with_flags(
    cli_runner: CliRunner,
    context: dict[str, Any],
    name: str,
    domain: str,
    privacy: str,
) -> None:
    """Run praxis new with required flags and explicit --path."""
    parent_dir: Path = context["project_root"]
    result = cli_runner.invoke(
        app,
        [
            "new",
            name,
            "--domain",
            domain,
            "--subtype",
            "cli",
            "--privacy",
            privacy,
            "--env",
            "Home",
            "--path",
            str(parent_dir),
        ],
    )
    context["result"] = result
    context["project_root"] = parent_dir / name


@when(
    parsers.parse(
        'I run praxis new "{name}" with domain "{domain}" and privacy "{privacy}" --json'
    )
)
def run_new_json_no_path(
    cli_runner: CliRunner,
    context: dict[str, Any],
    name: str,
    domain: str,
    privacy: str,
) -> None:
    """Run praxis new --json without --path (should error if PRAXIS_HOME missing)."""
    result = cli_runner.invoke(
        app,
        [
            "new",
            name,
            "--domain",
            domain,
            "--privacy",
            privacy,
            "--json",
        ],
    )
    context["result"] = result


@pytest.fixture(autouse=True)
def restore_praxis_home(context: dict[str, Any]):
    """Restore PRAXIS_HOME after each scenario."""
    yield
    original = context.get("original_praxis_home")
    if original is not None:
        os.environ["PRAXIS_HOME"] = original
    elif "PRAXIS_HOME" in os.environ:
        del os.environ["PRAXIS_HOME"]
