"""Step definitions for status.feature."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pytest_bdd import given, parsers, scenarios, then, when
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


@given(parsers.parse('a Praxis project with domain "{domain}" and stage "{stage}"'))
def project_with_domain_and_stage(tmp_path: Path, context: dict[str, Any], domain: str, stage: str) -> None:
    """Create a project with specific domain and stage."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        f"""domain: {domain}
stage: {stage}
privacy_level: personal
environment: Home
"""
    )


@given("docs/sod.md does not exist")
def sod_does_not_exist(context: dict[str, Any]) -> None:
    """Ensure docs/sod.md does not exist."""
    project_root = context["project_root"]
    sod_path = project_root / "docs" / "sod.md"
    if sod_path.exists():
        sod_path.unlink()


@given("docs/sod.md exists")
def sod_exists(context: dict[str, Any]) -> None:
    """Ensure docs/sod.md exists."""
    project_root = context["project_root"]
    docs_dir = project_root / "docs"
    docs_dir.mkdir(exist_ok=True)
    sod_path = docs_dir / "sod.md"
    sod_path.write_text("# Solution Overview Document\n")


@given("docs/brief.md does not exist")
def brief_does_not_exist(context: dict[str, Any]) -> None:
    """Ensure docs/brief.md does not exist."""
    project_root = context["project_root"]
    brief_path = project_root / "docs" / "brief.md"
    if brief_path.exists():
        brief_path.unlink()


@given("a Praxis project with an invalid domain value in praxis.yaml")
def project_with_invalid_domain(tmp_path: Path, context: dict[str, Any]) -> None:
    """Create a project with an invalid domain value."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: invalid_domain
stage: capture
privacy_level: personal
environment: Home
"""
    )


@when("I run praxis status")
def run_status(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run praxis status command."""
    project_root = context["project_root"]
    result = cli_runner.invoke(app, ["status", str(project_root)])
    context["result"] = result


@when("I run praxis status with --json")
def run_status_json(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run praxis status command with --json flag."""
    project_root = context["project_root"]
    result = cli_runner.invoke(app, ["status", str(project_root), "--json"])
    context["result"] = result


@then(parsers.parse('the output includes a "{action}" action for "{target}"'))
def output_includes_action_for_target(context: dict[str, Any], action: str, target: str) -> None:
    """Check that output includes a specific action for a target."""
    result = context["result"]
    output = result.output

    # Map action to icon
    action_icons = {
        "create": "+",
        "edit": "~",
        "run": "▶",
        "review": "?",
        "fix": "!",
    }
    icon = action_icons.get(action, action)

    # Check for icon + action pattern with target
    action_word = action.capitalize()
    expected_patterns = [
        f"{icon} {action_word} {target}",
    ]

    found = any(pattern in output for pattern in expected_patterns)
    assert found, f"Expected '{action}' action for '{target}' not found in output.\n" f"Output: {output}"


# Alias to handle "an" vs "a" article grammar in Gherkin steps
# (e.g., "an edit action" vs "a create action")
@then(parsers.parse('the output includes an "{action}" action for "{target}"'))
def output_includes_an_action_for_target(context: dict[str, Any], action: str, target: str) -> None:
    """Check that output includes a specific action for a target.

    This is an alias for 'the output includes a "{action}" action for "{target}"'
    to handle proper grammar with actions that start with vowels (e.g., "edit").
    """
    output_includes_action_for_target(context, action, target)


@then("1-3 next steps are shown")
def one_to_three_next_steps(context: dict[str, Any]) -> None:
    """Check that 1-3 next steps are shown."""
    result = context["result"]
    output = result.output

    # Count lines with action icons
    action_icons = ["+", "~", "▶", "?", "!"]
    step_lines = [
        line for line in output.split("\n") if any(line.strip().startswith(icon + " ") for icon in action_icons)
    ]

    assert 1 <= len(step_lines) <= 3, (
        f"Expected 1-3 next steps, found {len(step_lines)}.\n" f"Step lines: {step_lines}\n" f"Output: {output}"
    )


@then('the first next step is a "fix" action')
def first_step_is_fix(context: dict[str, Any]) -> None:
    """Check that the first next step is a fix action."""
    result = context["result"]
    output = result.output

    # Find the Next Steps section and the first step
    lines = output.split("\n")
    in_next_steps = False
    for line in lines:
        if "Next Steps:" in line:
            in_next_steps = True
            continue
        if in_next_steps and line.strip().startswith("!"):
            return  # Found fix action as first step
        if in_next_steps and line.strip() and not line.strip().startswith("Legend:"):
            # First non-empty line after "Next Steps:" that isn't legend
            assert line.strip().startswith("!"), f"Expected first step to be '!' (fix), got: {line}"
            return

    assert False, f"No fix action found as first step.\nOutput: {output}"


@then(parsers.parse('the step includes the target "{target}"'))
def step_includes_target(context: dict[str, Any], target: str) -> None:
    """Check that a step includes the target."""
    result = context["result"]
    assert target in result.output, f"Expected target '{target}' not found in output.\n" f"Output: {result.output}"


@then('the JSON output contains "next_steps" array')
def json_contains_next_steps(context: dict[str, Any]) -> None:
    """Check that JSON output contains next_steps array."""
    result = context["result"]
    try:
        data = json.loads(result.output)
    except json.JSONDecodeError:
        assert False, f"Output is not valid JSON.\nOutput: {result.output}"

    assert "next_steps" in data, f"Expected 'next_steps' in JSON output.\n" f"Keys: {list(data.keys())}"
    assert isinstance(data["next_steps"], list), (
        f"Expected 'next_steps' to be a list.\n" f"Type: {type(data['next_steps'])}"
    )


@then("the next_steps array has 1 to 3 items")
def next_steps_has_1_to_3_items(context: dict[str, Any]) -> None:
    """Check that next_steps array has 1 to 3 items."""
    result = context["result"]
    data = json.loads(result.output)
    next_steps = data.get("next_steps", [])

    assert 1 <= len(next_steps) <= 3, f"Expected 1-3 next_steps, got {len(next_steps)}.\n" f"Steps: {next_steps}"


@then(parsers.parse('the output includes a "{action}" action'))
def output_includes_action(context: dict[str, Any], action: str) -> None:
    """Check that output includes a specific action type."""
    result = context["result"]
    output = result.output

    # Map action to icon
    action_icons = {
        "create": "+",
        "edit": "~",
        "run": "▶",
        "review": "?",
        "fix": "!",
    }
    icon = action_icons.get(action, action)

    assert f"{icon} " in output or f"{icon} {action.capitalize()}" in output, (
        f"Expected '{action}' action not found in output.\n" f"Output: {output}"
    )


@then(parsers.parse('the run step includes "{text}"'))
def run_step_includes_text(context: dict[str, Any], text: str) -> None:
    """Check that a run step includes specific text."""
    result = context["result"]
    output = result.output

    # Find run steps (lines starting with ▶)
    run_lines = [line for line in output.split("\n") if line.strip().startswith("▶")]

    found = any(text in line for line in run_lines)
    assert found, f"Expected text '{text}' in run step not found.\n" f"Run lines: {run_lines}\n" f"Output: {output}"
