"""Step definitions for stage_history.feature."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml
from pytest_bdd import given, parsers, scenarios, then, when
from typer.testing import CliRunner

from praxis.cli import app

scenarios("../features/stage_history.feature")


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


@given(parsers.parse('a project at stage "{stage}" without history field'))
def project_at_stage_no_history(
    tmp_path: Path, context: dict[str, Any], stage: str
) -> None:
    """Create a project at the given stage without history field."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        f"""domain: code
stage: {stage}
privacy_level: personal
environment: Home
"""
    )


@given(
    parsers.parse('the project has transitioned through "{s1}" to "{s2}" to "{s3}"')
)
def project_with_history(
    context: dict[str, Any], s1: str, s2: str, s3: str
) -> None:
    """Create a project with existing history."""
    project_root = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"

    # Read current yaml
    content = yaml.safe_load(praxis_yaml.read_text())

    # Add history
    content["history"] = [
        {
            "timestamp": "2026-01-01T10:00:00Z",
            "from_stage": s1,
            "to_stage": s2,
        },
        {
            "timestamp": "2026-01-02T10:00:00Z",
            "from_stage": s2,
            "to_stage": s3,
        },
    ]

    praxis_yaml.write_text(yaml.safe_dump(content, default_flow_style=False, sort_keys=False))


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


@when(parsers.parse('I run praxis stage "{new_stage}" with reason "{reason}"'))
def run_stage_with_reason(
    cli_runner: CliRunner,
    context: dict[str, Any],
    new_stage: str,
    reason: str,
) -> None:
    """Run praxis stage command with --reason flag."""
    project_root = context["project_root"]
    result = cli_runner.invoke(
        app, ["stage", new_stage, str(project_root), "--reason", reason]
    )
    context["result"] = result


@when(parsers.parse('I run praxis stage "{new_stage}" with --json flag'))
def run_stage_with_json(
    cli_runner: CliRunner,
    context: dict[str, Any],
    new_stage: str,
) -> None:
    """Run praxis stage command with --json flag."""
    project_root = context["project_root"]
    result = cli_runner.invoke(app, ["stage", new_stage, str(project_root), "--json"])
    context["result"] = result


@when("I run praxis status")
def run_status(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run praxis status command."""
    project_root = context["project_root"]
    result = cli_runner.invoke(app, ["status", str(project_root)])
    context["result"] = result


@then(
    parsers.parse('praxis.yaml should contain a history entry with from_stage "{stage}"')
)
def check_history_from_stage(context: dict[str, Any], stage: str) -> None:
    """Verify praxis.yaml has a history entry with the expected from_stage."""
    project_root = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"
    content = yaml.safe_load(praxis_yaml.read_text())

    assert "history" in content, "praxis.yaml should have a 'history' field"
    history = content["history"]
    assert isinstance(history, list), "history should be a list"

    found = any(entry.get("from_stage") == stage for entry in history)
    assert found, f"No history entry found with from_stage '{stage}'. History: {history}"


@then(
    parsers.parse('praxis.yaml should contain a history entry with to_stage "{stage}"')
)
def check_history_to_stage(context: dict[str, Any], stage: str) -> None:
    """Verify praxis.yaml has a history entry with the expected to_stage."""
    project_root = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"
    content = yaml.safe_load(praxis_yaml.read_text())

    assert "history" in content, "praxis.yaml should have a 'history' field"
    history = content["history"]

    found = any(entry.get("to_stage") == stage for entry in history)
    assert found, f"No history entry found with to_stage '{stage}'. History: {history}"


@then("praxis.yaml should contain a history entry with timestamp")
def check_history_timestamp(context: dict[str, Any]) -> None:
    """Verify praxis.yaml has a history entry with a timestamp."""
    project_root = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"
    content = yaml.safe_load(praxis_yaml.read_text())

    assert "history" in content, "praxis.yaml should have a 'history' field"
    history = content["history"]

    assert len(history) > 0, "history should not be empty"
    assert "timestamp" in history[-1], "Latest history entry should have a timestamp"
    assert history[-1]["timestamp"], "timestamp should not be empty"


@then(parsers.parse('praxis.yaml should contain a contract_id matching "{pattern}"'))
def check_contract_id(context: dict[str, Any], pattern: str) -> None:
    """Verify praxis.yaml has a contract_id matching the pattern."""
    project_root = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"
    content = yaml.safe_load(praxis_yaml.read_text())

    assert "history" in content, "praxis.yaml should have a 'history' field"
    history = content["history"]

    # Find entry with contract_id
    contract_ids = [entry.get("contract_id") for entry in history if "contract_id" in entry]
    assert len(contract_ids) > 0, f"No contract_id found in history: {history}"

    # Check pattern match
    contract_id = contract_ids[-1]  # Get most recent
    assert re.match(pattern, contract_id), (
        f"contract_id '{contract_id}' does not match pattern '{pattern}'"
    )


@then(parsers.parse('praxis.yaml should contain a history entry with reason "{reason}"'))
def check_history_reason(context: dict[str, Any], reason: str) -> None:
    """Verify praxis.yaml has a history entry with the expected reason."""
    project_root = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"
    content = yaml.safe_load(praxis_yaml.read_text())

    assert "history" in content, "praxis.yaml should have a 'history' field"
    history = content["history"]

    found = any(entry.get("reason") == reason for entry in history)
    assert found, f"No history entry found with reason '{reason}'. History: {history}"


@then("praxis.yaml should contain a history section")
def check_history_section(context: dict[str, Any]) -> None:
    """Verify praxis.yaml has a history section."""
    project_root = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"
    content = yaml.safe_load(praxis_yaml.read_text())

    assert "history" in content, "praxis.yaml should have a 'history' field"
    assert isinstance(content["history"], list), "history should be a list"


@then(parsers.parse("praxis.yaml should have {count:d} history entries"))
def check_history_count(context: dict[str, Any], count: int) -> None:
    """Verify praxis.yaml has the expected number of history entries."""
    project_root = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"
    content = yaml.safe_load(praxis_yaml.read_text())

    assert "history" in content, "praxis.yaml should have a 'history' field"
    history = content["history"]
    assert len(history) == count, (
        f"Expected {count} history entries, got {len(history)}. History: {history}"
    )


@then("praxis.yaml should contain a history entry without reason")
def check_history_no_reason(context: dict[str, Any]) -> None:
    """Verify praxis.yaml has a history entry without reason field."""
    project_root = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"
    content = yaml.safe_load(praxis_yaml.read_text())

    assert "history" in content, "praxis.yaml should have a 'history' field"
    history = content["history"]
    assert len(history) > 0, "history should not be empty"

    # Check that the latest entry doesn't have a reason (or it's None)
    latest = history[-1]
    assert "reason" not in latest or latest.get("reason") is None, (
        f"Latest history entry should not have a reason. Got: {latest}"
    )
