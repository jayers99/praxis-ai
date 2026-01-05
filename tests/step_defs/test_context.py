"""Step definitions for context.feature."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pytest_bdd import given, parsers, scenarios, then, when
from typer.testing import CliRunner

from praxis.cli import app

scenarios("../features/context.feature")


@given("a valid Praxis project with praxis.yaml")
def valid_project(tmp_path: Path, context: dict[str, Any]) -> None:
    """Create a valid Praxis project."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: code
stage: capture
privacy_level: personal
environment: Home
"""
    )


@given("an opinions directory structure exists")
def create_opinions_structure(context: dict[str, Any]) -> None:
    """Create basic opinions directory structure."""
    project_root: Path = context["project_root"]
    opinions_dir = project_root / "opinions"
    opinions_dir.mkdir(exist_ok=True)
    (opinions_dir / "_shared").mkdir(exist_ok=True)
    (opinions_dir / "code").mkdir(exist_ok=True)


@given(parsers.parse('opinion file "{filepath}" exists'))
def create_opinion_file(context: dict[str, Any], filepath: str) -> None:
    """Create an opinion file with valid frontmatter."""
    project_root: Path = context["project_root"]
    opinions_dir = project_root / "opinions"
    file_path = opinions_dir / filepath
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(
        """---
domain: code
version: "1.0"
status: active
---

# Principles

Test opinion content.
"""
    )


@given(parsers.parse('a Praxis project at stage "{stage}" with domain "{domain}"'))
def project_at_stage_with_domain(tmp_path: Path, context: dict[str, Any], stage: str, domain: str) -> None:
    """Create a Praxis project at a specific stage and domain."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        f"""domain: {domain}
stage: {stage}
privacy_level: personal
environment: Home
"""
    )


@given(parsers.parse('a Praxis project with domain "{domain}" and stage "{stage}"'))
def project_with_domain_and_stage(tmp_path: Path, context: dict[str, Any], domain: str, stage: str) -> None:
    """Create a Praxis project with specific domain and stage."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        f"""domain: {domain}
stage: {stage}
privacy_level: personal
environment: Home
"""
    )


@given(parsers.parse('a Praxis project with domain "{domain}" and subtype "{subtype}"'))
def project_with_domain_and_subtype(tmp_path: Path, context: dict[str, Any], domain: str, subtype: str) -> None:
    """Create a Praxis project with specific domain and subtype."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        f"""domain: {domain}
stage: capture
subtype: {subtype}
privacy_level: personal
environment: Home
"""
    )


@given(parsers.parse('a file "{filepath}" exists'))
def file_exists(context: dict[str, Any], filepath: str) -> None:
    """Create a file at the specified path."""
    project_root: Path = context["project_root"]
    file_path = project_root / filepath
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(f"# {filepath}\n\nSample content for testing.\n")


@given(parsers.parse('no file "{filepath}" exists'))
def file_not_exists(context: dict[str, Any], filepath: str) -> None:
    """Ensure file does not exist."""
    project_root: Path = context["project_root"]
    file_path = project_root / filepath
    if file_path.exists():
        file_path.unlink()


@given("a directory without praxis.yaml")
def directory_without_yaml(tmp_path: Path, context: dict[str, Any]) -> None:
    """Create an empty directory."""
    context["project_root"] = tmp_path


@given("a praxis.yaml with invalid domain value")
def invalid_domain_yaml(tmp_path: Path, context: dict[str, Any]) -> None:
    """Create a praxis.yaml with invalid domain."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: invalid_domain
stage: capture
privacy_level: personal
environment: Home
"""
    )


@when("I run praxis context")
def run_context(context: dict[str, Any]) -> None:
    """Run praxis context command."""
    project_root: Path = context["project_root"]
    runner = CliRunner()
    result = runner.invoke(app, ["context", str(project_root)])
    context["result"] = result
    context["output"] = result.stdout


@when("I run praxis context with --json")
def run_context_json(context: dict[str, Any]) -> None:
    """Run praxis context with --json flag."""
    project_root: Path = context["project_root"]
    runner = CliRunner()
    result = runner.invoke(app, ["context", str(project_root), "--json"])
    context["result"] = result
    context["output"] = result.stdout


@when("I run praxis context with --quiet")
def run_context_quiet(context: dict[str, Any]) -> None:
    """Run praxis context with --quiet flag."""
    project_root: Path = context["project_root"]
    runner = CliRunner()
    result = runner.invoke(app, ["context", str(project_root), "--quiet"])
    context["result"] = result
    context["output"] = result.stdout


@when("I run praxis context twice")
def run_context_twice(context: dict[str, Any]) -> None:
    """Run praxis context command twice."""
    project_root: Path = context["project_root"]
    runner = CliRunner()

    result1 = runner.invoke(app, ["context", str(project_root), "--json"])
    result2 = runner.invoke(app, ["context", str(project_root), "--json"])

    context["result"] = result1
    context["output1"] = result1.stdout
    context["output2"] = result2.stdout


@then(parsers.parse("the exit code should be {code:d}"))
def check_exit_code(context: dict[str, Any], code: int) -> None:
    """Check the exit code matches expected."""
    assert context["result"].exit_code == code


@then(parsers.parse('the output should contain "{text}"'))
def output_contains(context: dict[str, Any], text: str) -> None:
    """Check output contains text."""
    assert text in context["output"]


@then("the output is valid JSON")
def output_is_json(context: dict[str, Any]) -> None:
    """Check output is valid JSON."""
    try:
        parsed = json.loads(context["output"])
        context["json_output"] = parsed
    except json.JSONDecodeError as e:
        raise AssertionError(f"Output is not valid JSON: {e}")


@then(parsers.parse('the JSON contains field "{field}"'))
def json_contains_field(context: dict[str, Any], field: str) -> None:
    """Check JSON contains the specified field."""
    if "json_output" not in context:
        parsed = json.loads(context["output"])
        context["json_output"] = parsed

    assert field in context["json_output"], f"Field '{field}' not found in JSON output"


@then(parsers.parse('the JSON field "{field}" equals "{value}"'))
def json_field_equals(context: dict[str, Any], field: str, value: str) -> None:
    """Check JSON field equals the specified value."""
    if "json_output" not in context:
        parsed = json.loads(context["output"])
        context["json_output"] = parsed

    # Handle nested fields (e.g., "formalize_artifact.path")
    parts = field.split(".")
    obj = context["json_output"]
    for part in parts:
        obj = obj[part]

    assert str(obj) == value, f"Field '{field}' = '{obj}', expected '{value}'"


@then(parsers.parse('the JSON field "{field}" is not null'))
def json_field_not_null(context: dict[str, Any], field: str) -> None:
    """Check JSON field is not null."""
    if "json_output" not in context:
        parsed = json.loads(context["output"])
        context["json_output"] = parsed

    # Handle nested fields
    parts = field.split(".")
    obj = context["json_output"]
    for part in parts:
        obj = obj[part]

    assert obj is not None, f"Field '{field}' is null"


@then(parsers.parse('the JSON field "{field}" is null'))
def json_field_is_null(context: dict[str, Any], field: str) -> None:
    """Check JSON field is null."""
    if "json_output" not in context:
        parsed = json.loads(context["output"])
        context["json_output"] = parsed

    # Handle nested fields
    parts = field.split(".")
    obj = context["json_output"]
    for part in parts:
        obj = obj[part]

    assert obj is None, f"Field '{field}' is not null: {obj}"


@then(parsers.parse('the JSON field "{field}" is an array'))
def json_field_is_array(context: dict[str, Any], field: str) -> None:
    """Check JSON field is an array."""
    if "json_output" not in context:
        parsed = json.loads(context["output"])
        context["json_output"] = parsed

    # Handle nested fields
    parts = field.split(".")
    obj = context["json_output"]
    for part in parts:
        obj = obj[part]

    assert isinstance(obj, list), f"Field '{field}' is not an array"


@then("the opinions array is not empty")
def opinions_not_empty(context: dict[str, Any]) -> None:
    """Check opinions array is not empty."""
    if "json_output" not in context:
        parsed = json.loads(context["output"])
        context["json_output"] = parsed

    opinions = context["json_output"]["opinions"]
    assert len(opinions) > 0, "Opinions array is empty"


@then("both outputs are identical")
def outputs_identical(context: dict[str, Any]) -> None:
    """Check that both outputs are identical."""
    output1 = context["output1"]
    output2 = context["output2"]

    # Parse JSON to compare structured data (ignoring whitespace differences)
    json1 = json.loads(output1)
    json2 = json.loads(output2)

    assert json1 == json2, "Outputs are not identical"


@then("the output should contain error message")
def output_contains_error(context: dict[str, Any]) -> None:
    """Check output contains an error message."""
    output = context["output"]
    # Check for common error indicators
    assert "✗" in output or "error" in output.lower() or "Error" in output


@then("the output is empty")
def output_is_empty(context: dict[str, Any]) -> None:
    """Check output is empty."""
    assert context["output"].strip() == "", f"Output is not empty: {context['output']}"
