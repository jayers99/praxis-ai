"""Step definitions for opinions.feature."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

import pytest
from pytest_bdd import given, parsers, scenarios, then, when
from typer.testing import CliRunner

from praxis.cli import app

scenarios("../features/opinions.feature")


@given("I am in a temporary directory")
def setup_temp_dir(tmp_path: Path, context: dict[str, Any], request: pytest.FixtureRequest) -> None:
    """Set up temporary directory with cleanup."""
    context["project_root"] = tmp_path
    original_dir = os.getcwd()
    os.chdir(tmp_path)

    # Ensure we restore the original directory even if test fails
    def restore_cwd() -> None:
        os.chdir(original_dir)

    request.addfinalizer(restore_cwd)


@given("I have an opinions directory structure")
def create_opinions_dir(context: dict[str, Any]) -> None:
    """Create basic opinions directory."""
    project_root = context["project_root"]
    opinions_dir = project_root / "opinions"
    opinions_dir.mkdir(exist_ok=True)
    (opinions_dir / "_shared").mkdir(exist_ok=True)
    (opinions_dir / "code").mkdir(exist_ok=True)
    (opinions_dir / "create").mkdir(exist_ok=True)


@given(parsers.parse('a praxis.yaml with domain "{domain}" and stage "{stage}"'))
def create_praxis_yaml(
    context: dict[str, Any],
    domain: str,
    stage: str,
) -> None:
    """Create praxis.yaml with specified domain and stage."""
    project_root = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"
    praxis_yaml.write_text(
        f"""domain: {domain}
stage: {stage}
privacy_level: personal
environment: Home
"""
    )


@given(parsers.parse('a praxis.yaml with domain "{domain}" and stage "{stage}" ' 'and subtype "{subtype}"'))
def create_praxis_yaml_with_subtype(
    context: dict[str, Any],
    domain: str,
    stage: str,
    subtype: str,
) -> None:
    """Create praxis.yaml with domain, stage, and subtype."""
    project_root = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"
    praxis_yaml.write_text(
        f"""domain: {domain}
stage: {stage}
subtype: {subtype}
privacy_level: personal
environment: Home
"""
    )


@given("no praxis.yaml exists")
def ensure_no_praxis_yaml(context: dict[str, Any]) -> None:
    """Ensure no praxis.yaml exists."""
    project_root = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"
    if praxis_yaml.exists():
        praxis_yaml.unlink()


@given(parsers.parse("{path} exists with valid frontmatter"))
def create_opinion_file(context: dict[str, Any], path: str) -> None:
    """Create an opinion file with valid frontmatter."""
    project_root = context["project_root"]
    full_path = project_root / path

    # Create parent directories
    full_path.parent.mkdir(parents=True, exist_ok=True)

    # Determine domain from path
    parts = path.split("/")
    if "_shared" in parts:
        domain_line = ""  # No domain for shared files
    else:
        domain = parts[1] if len(parts) > 1 else "code"
        domain_line = f"domain: {domain}\n"

    full_path.write_text(
        f"""---
{domain_line}version: "1.0"
status: active
---

# {path}

Test opinion content.
"""
    )


@given("the opinions directory does not exist")
def remove_opinions_dir(context: dict[str, Any]) -> None:
    """Ensure opinions directory does not exist."""
    project_root = context["project_root"]
    opinions_dir = project_root / "opinions"
    if opinions_dir.exists():
        import shutil

        shutil.rmtree(opinions_dir)


@when(parsers.parse('I run "{command}"'))
def run_command(
    context: dict[str, Any],
    command: str,
    cli_runner: CliRunner,
) -> None:
    """Run a praxis CLI command."""
    # Parse command into args
    parts = command.split()
    if parts[0] == "praxis":
        parts = parts[1:]

    result = cli_runner.invoke(app, parts)
    context["result"] = result


@when(parsers.parse('I save the output as "{name}"'))
def save_output(context: dict[str, Any], name: str) -> None:
    """Save the current output for later comparison."""
    if "saved_outputs" not in context:
        context["saved_outputs"] = {}
    context["saved_outputs"][name] = context["result"].output


@then(parsers.parse('the output contains "{text}"'))
def check_output_contains(context: dict[str, Any], text: str) -> None:
    """Verify output contains expected text."""
    result = context["result"]
    assert text in result.output, f"Expected '{text}' in output. Got: {result.output}"


@then(parsers.parse('the stderr contains "{text}"'))
def check_stderr_contains(context: dict[str, Any], text: str) -> None:
    """Verify stderr contains expected text."""
    result = context["result"]
    # In Typer testing, stderr is often in output or we need to check separately
    # For now, check combined output
    output = result.output
    assert text in output, f"Expected '{text}' in stderr/output. Got: {output}"


@then(parsers.parse("the exit code is {code:d}"))
def check_exit_code(context: dict[str, Any], code: int) -> None:
    """Verify exit code."""
    result = context["result"]
    assert result.exit_code == code, f"Expected exit code {code}, got {result.exit_code}. " f"Output: {result.output}"


@then("the output is valid JSON")
def check_valid_json(context: dict[str, Any]) -> None:
    """Verify output is valid JSON."""
    result = context["result"]
    try:
        context["json_output"] = json.loads(result.output)
    except json.JSONDecodeError as e:
        raise AssertionError(f"Output is not valid JSON: {e}. Got: {result.output}")


@then(parsers.parse('the JSON contains key "{key}"'))
def check_json_key(context: dict[str, Any], key: str) -> None:
    """Verify JSON contains expected key."""
    json_output = context.get("json_output")
    if json_output is None:
        json_output = json.loads(context["result"].output)
        context["json_output"] = json_output
    assert key in json_output, f"Expected key '{key}' in JSON. Got: {json_output}"


@then(parsers.parse('"{first}" equals "{second}"'))
def check_outputs_equal(context: dict[str, Any], first: str, second: str) -> None:
    """Verify two saved outputs are equal."""
    saved = context.get("saved_outputs", {})
    assert first in saved, f"Output '{first}' not saved"
    assert second in saved, f"Output '{second}' not saved"
    assert saved[first] == saved[second], f"Outputs differ:\n{first}:\n{saved[first]}\n{second}:\n{saved[second]}"
