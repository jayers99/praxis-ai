"""Step definitions for privacy_guardrails.feature."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pytest
from pytest_bdd import given, parsers, scenarios, then, when
from typer.testing import CliRunner

from praxis.cli import app

scenarios("../features/privacy_guardrails.feature")


@pytest.fixture
def privacy_cli_runner() -> CliRunner:
    """Provide a CLI runner with separated stderr."""
    return CliRunner(mix_stderr=False)


@given("I am in a temporary directory")
def setup_temp_dir(
    tmp_path: Path, context: dict[str, Any], request: pytest.FixtureRequest
) -> None:
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


@given(
    parsers.parse(
        'a praxis.yaml with domain "{domain}" stage "{stage}" and privacy "{privacy}"'
    )
)
def create_praxis_yaml_with_privacy(
    context: dict[str, Any],
    domain: str,
    stage: str,
    privacy: str,
) -> None:
    """Create praxis.yaml with domain, stage, and privacy level."""
    project_root = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"
    praxis_yaml.write_text(
        f"""domain: {domain}
stage: {stage}
privacy_level: {privacy}
environment: Home
"""
    )


@given(parsers.parse("{path} exists with valid frontmatter"))
def create_opinion_file(context: dict[str, Any], path: str) -> None:
    """Create an opinion file with valid frontmatter."""
    project_root = context["project_root"]
    full_path = project_root / path

    # Create parent directories
    full_path.parent.mkdir(parents=True, exist_ok=True)

    full_path.write_text(
        f"""---
status: active
version: "1.0"
---

# {path}

Test opinion content.
"""
    )


@given(
    parsers.parse(
        "opinions/_shared/first-principles.md exists with content containing {content}"
    )
)
def create_opinion_with_content(
    context: dict[str, Any],
    content: str,
) -> None:
    """Create an opinion file with specific content."""
    project_root = context["project_root"]
    opinions_dir = project_root / "opinions" / "_shared"
    opinions_dir.mkdir(parents=True, exist_ok=True)

    opinion_file = opinions_dir / "first-principles.md"
    # Remove quotes from content if present
    content = content.strip('"')
    opinion_file.write_text(
        f"""---
status: active
version: 1.0
---

# First Principles

This is a test opinion file.

Example content: {content}
"""
    )


@when(parsers.parse('I run "{command}"'))
def run_privacy_command(
    context: dict[str, Any],
    command: str,
    privacy_cli_runner: CliRunner,
) -> None:
    """Run a praxis CLI command with stderr separation."""
    # Parse command into args
    parts = command.split()
    if parts[0] == "praxis":
        parts = parts[1:]

    result = privacy_cli_runner.invoke(app, parts)
    context["result"] = result
    context["last_result"] = result


@then(parsers.parse('the stderr contains "{text}"'))
def check_stderr_contains(context: dict[str, Any], text: str) -> None:
    """Check that stderr contains the specified text."""
    result = context.get("last_result") or context.get("result")
    assert result is not None, "No command result found in context"
    assert text in result.stderr, f"Expected '{text}' in stderr, got: {result.stderr}"


@then(parsers.parse('the stderr does not contain "{text}"'))
def check_stderr_not_contains(context: dict[str, Any], text: str) -> None:
    """Check that stderr does not contain the specified text."""
    result = context.get("last_result") or context.get("result")
    assert result is not None, "No command result found in context"
    assert (
        text not in result.stderr
    ), f"Expected '{text}' not in stderr, got: {result.stderr}"


@then(parsers.parse('the output does not contain "{text}"'))
def check_output_not_contains(context: dict[str, Any], text: str) -> None:
    """Check that output does not contain the specified text."""
    result = context.get("last_result") or context.get("result")
    assert result is not None, "No command result found in context"
    # Check stdout for --prompt output
    stdout = result.stdout if hasattr(result, 'stdout') else result.output
    assert (
        text not in stdout
    ), f"Expected '{text}' not in output, got: {stdout}"


@then(parsers.parse('the output contains "{text}"'))
def check_output_contains_privacy(context: dict[str, Any], text: str) -> None:
    """Check that stdout contains the specified text."""
    result = context.get("last_result") or context.get("result")
    assert result is not None, "No command result found in context"
    # Check stdout for --prompt output
    stdout = result.stdout if hasattr(result, 'stdout') else result.output
    assert text in stdout, f"Expected '{text}' in output, got: {stdout}"


@when(parsers.parse('I save the output as "{name}"'))
def save_output_privacy(context: dict[str, Any], name: str) -> None:
    """Save the current output for later comparison."""
    if "saved_outputs" not in context:
        context["saved_outputs"] = {}
    result = context.get("last_result") or context.get("result")
    stdout = result.stdout if hasattr(result, 'stdout') else result.output
    context["saved_outputs"][name] = stdout


@then(parsers.parse('"{name1}" equals "{name2}"'))
def compare_saved_outputs(context: dict[str, Any], name1: str, name2: str) -> None:
    """Compare two saved outputs for equality."""
    saved = context.get("saved_outputs", {})
    assert name1 in saved, f"Output '{name1}' not found in saved outputs"
    assert name2 in saved, f"Output '{name2}' not found in saved outputs"
    assert saved[name1] == saved[name2], (
        f"Outputs differ:\n{name1}:\n{saved[name1]}\n\n{name2}:\n{saved[name2]}"
    )


@then(parsers.parse("the exit code is {code:d}"))
def check_exit_code_privacy(context: dict[str, Any], code: int) -> None:
    """Verify the exit code."""
    result = context.get("last_result") or context.get("result")
    assert result.exit_code == code, (
        f"Expected exit code {code}, got {result.exit_code}. "
        f"Stdout: {result.stdout if hasattr(result, 'stdout') else result.output}\n"
        f"Stderr: {result.stderr if hasattr(result, 'stderr') else ''}"
    )

