"""Step definitions for cli_automation.feature."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pytest_bdd import given, parsers, scenarios, then, when
from typer.testing import CliRunner

from praxis.cli import app

scenarios("../features/cli_automation.feature")


@given("an empty project directory")
def empty_project_directory(tmp_path: Path, context: dict[str, Any]) -> None:
    """Use the pytest tmp_path as an empty project directory."""
    context["project_root"] = tmp_path


@given("a valid praxis project at capture stage")
def valid_praxis_project(tmp_path: Path, context: dict[str, Any]) -> None:
    """Create a valid praxis project at capture stage."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: code
stage: capture
privacy_level: personal
environment: Home
"""
    )


@when("I run praxis init --domain code --privacy personal --json")
def run_init_json(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run praxis init with --json flag."""
    project_root = context["project_root"]
    result = cli_runner.invoke(
        app,
        ["init", str(project_root), "--domain", "code", "--privacy", "personal", "--json"],
    )
    context["result"] = result


@when("I run praxis init --json")
def run_init_json_no_flags(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run praxis init with only --json flag (missing required flags)."""
    project_root = context["project_root"]
    result = cli_runner.invoke(
        app,
        ["init", str(project_root), "--json"],
    )
    context["result"] = result


@when("I run praxis init --domain code --privacy personal --quiet")
def run_init_quiet(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run praxis init with --quiet flag."""
    project_root = context["project_root"]
    result = cli_runner.invoke(
        app,
        ["init", str(project_root), "--domain", "code", "--privacy", "personal", "--quiet"],
    )
    context["result"] = result


@when("I run praxis validate --json")
def run_validate_json(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run praxis validate with --json flag."""
    project_root = context["project_root"]
    result = cli_runner.invoke(app, ["validate", str(project_root), "--json"])
    context["result"] = result


@when("I run praxis validate --quiet")
def run_validate_quiet(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run praxis validate with --quiet flag."""
    project_root = context["project_root"]
    result = cli_runner.invoke(app, ["validate", str(project_root), "--quiet"])
    context["result"] = result


@when("I run praxis stage sense --json")
def run_stage_json(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run praxis stage with --json flag."""
    project_root = context["project_root"]
    result = cli_runner.invoke(app, ["stage", "sense", str(project_root), "--json"])
    context["result"] = result


@when("I run praxis stage sense --quiet")
def run_stage_quiet(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run praxis stage with --quiet flag."""
    project_root = context["project_root"]
    result = cli_runner.invoke(app, ["stage", "sense", str(project_root), "--quiet"])
    context["result"] = result


@when("I run praxis status --json")
def run_status_json(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run praxis status with --json flag."""
    project_root = context["project_root"]
    result = cli_runner.invoke(app, ["status", str(project_root), "--json"])
    context["result"] = result


@when("I run praxis status --quiet")
def run_status_quiet(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run praxis status with --quiet flag."""
    project_root = context["project_root"]
    result = cli_runner.invoke(app, ["status", str(project_root), "--quiet"])
    context["result"] = result


@when("I run praxis audit --quiet")
def run_audit_quiet(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run praxis audit with --quiet flag."""
    project_root = context["project_root"]
    result = cli_runner.invoke(app, ["audit", str(project_root), "--quiet"])
    context["result"] = result


@then("the output should be valid JSON")
def check_valid_json(context: dict[str, Any]) -> None:
    """Verify the output is valid JSON."""
    result = context["result"]
    try:
        context["json_output"] = json.loads(result.output)
    except json.JSONDecodeError as e:
        raise AssertionError(f"Output is not valid JSON: {e}\nOutput: {result.output}")


@then(parsers.parse('the JSON should have key "{key}"'))
def check_json_has_key(context: dict[str, Any], key: str) -> None:
    """Verify the JSON output has a specific key."""
    json_output = context.get("json_output")
    if json_output is None:
        # Parse if not already parsed
        result = context["result"]
        json_output = json.loads(result.output)
    assert key in json_output, f"Expected key '{key}' in JSON. Got keys: {list(json_output.keys())}"


@then("the output should be empty")
def check_output_empty(context: dict[str, Any]) -> None:
    """Verify the output is empty (or only whitespace)."""
    result = context["result"]
    assert result.output.strip() == "", f"Expected empty output, got: {result.output}"
