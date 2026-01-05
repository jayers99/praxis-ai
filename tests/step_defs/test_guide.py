"""Step definitions for guide.feature."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pytest_bdd import given, parsers, scenarios, then, when
from typer.testing import CliRunner

from praxis.cli import app

scenarios("../features/guide.feature")


@given("the user is in any directory")
def user_in_any_directory(tmp_path: Path, context: dict[str, Any]) -> None:
    """Set up a temporary directory for the user."""
    context["cwd"] = tmp_path


@when(parsers.parse('the user runs "{command}"'))
def run_command(command: str, context: dict[str, Any]) -> None:
    """Run a praxis command."""
    runner = CliRunner()
    # Parse the command to extract arguments
    parts = command.split()
    if parts[0] == "praxis":
        parts = parts[1:]  # Remove "praxis" prefix

    result = runner.invoke(app, parts)
    context["result"] = result
    context["exit_code"] = result.exit_code
    context["output"] = result.stdout


@then(parsers.parse("the exit code should be {expected_code:d}"))
def check_exit_code(expected_code: int, context: dict[str, Any]) -> None:
    """Check the exit code matches expected value."""
    assert context["exit_code"] == expected_code, (
        f"Expected exit code {expected_code}, got {context['exit_code']}\n" f"Output: {context['output']}"
    )


@then("the output contains all 9 lifecycle stages")
def check_lifecycle_stages(context: dict[str, Any]) -> None:
    """Check that all 9 lifecycle stages are present."""
    output = context["output"]
    stages = [
        "Capture",
        "Sense",
        "Explore",
        "Shape",
        "Formalize",
        "Commit",
        "Execute",
        "Sustain",
        "Close",
    ]
    for stage in stages:
        assert stage in output, f"Stage '{stage}' not found in output"


@then("the output explains the Formalize hinge concept")
def check_formalize_hinge(context: dict[str, Any]) -> None:
    """Check that Formalize hinge concept is explained."""
    output = context["output"]
    # Look for key hinge concept phrases
    assert "hinge" in output.lower() or "HINGE" in output, "Formalize hinge concept not found in output"
    assert (
        "exploration" in output.lower() and "execution" in output.lower()
    ), "Exploration/execution boundary not explained"


@then(parsers.parse('the output contains a reference to "{file_path}"'))
def check_file_reference(file_path: str, context: dict[str, Any]) -> None:
    """Check that output contains a reference to the specified file."""
    output = context["output"]
    assert file_path in output, f"Reference to '{file_path}' not found in output"


@then("the output is less than 50 lines")
def check_line_count(context: dict[str, Any]) -> None:
    """Check that output is less than 50 lines."""
    output = context["output"]
    line_count = len(output.splitlines())
    assert line_count < 50, f"Output has {line_count} lines (expected < 50)"


@then("the output lists all 5 privacy levels")
def check_privacy_levels(context: dict[str, Any]) -> None:
    """Check that all 5 privacy levels are present."""
    output = context["output"]
    levels = [
        "Public",
        "Public – Trusted Collaborators",
        "Personal",
        "Confidential",
        "Restricted",
    ]
    for level in levels:
        assert level in output, f"Privacy level '{level}' not found in output"


@then("the output explains behavioral constraints for each level")
def check_behavioral_constraints(context: dict[str, Any]) -> None:
    """Check that behavioral constraints are explained."""
    output = context["output"]
    # Look for constraint-related keywords
    constraint_keywords = ["storage", "AI", "collaboration", "artifact"]
    found = sum(1 for kw in constraint_keywords if kw.lower() in output.lower())
    assert found >= 2, f"Expected behavioral constraint keywords, found only {found}"


@then("the output describes the code domain purpose")
def check_code_domain_purpose(context: dict[str, Any]) -> None:
    """Check that code domain purpose is described."""
    output = context["output"]
    assert "code" in output.lower() or "CODE" in output, "Code domain not identified in output"
    # Check for purpose-related content
    assert "functional" in output.lower() or "system" in output.lower(), "Code domain purpose not described"


@then(parsers.parse('the output mentions the required formalize artifact "{artifact}"'))
def check_formalize_artifact(artifact: str, context: dict[str, Any]) -> None:
    """Check that the formalize artifact is mentioned."""
    output = context["output"]
    assert artifact in output, f"Artifact '{artifact}' not found in output"


@then(parsers.parse('the output contains "{text}"'))
def check_output_contains(text: str, context: dict[str, Any]) -> None:
    """Check that output contains the specified text."""
    output = context["output"]
    assert text in output, f"Text '{text}' not found in output"


@then("the output lists valid domain options")
def check_valid_domains(context: dict[str, Any]) -> None:
    """Check that valid domain options are listed."""
    output = context["output"]
    domains = ["code", "create", "write", "learn", "observe"]
    found = sum(1 for domain in domains if domain in output.lower())
    assert found >= 3, f"Expected domain options, found only {found} domains"


@then("the output lists available guide topics")
def check_guide_topics(context: dict[str, Any]) -> None:
    """Check that available guide topics are listed."""
    output = context["output"]
    topics = ["lifecycle", "privacy", "domain"]
    found = sum(1 for topic in topics if topic in output.lower())
    assert found >= 2, f"Expected guide topics, found only {found} topics"
