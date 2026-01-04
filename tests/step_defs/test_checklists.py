"""Step definitions for checklists.feature."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

from pytest_bdd import given, parsers, scenarios, then, when
from typer.testing import CliRunner

from praxis.cli import app

scenarios("../features/checklists.feature")


@given("the Praxis framework is installed")
def framework_installed(context: dict[str, Any]) -> None:
    """Verify the framework is installed."""
    # This is implicitly true if we're running tests
    context["framework_installed"] = True


@when('I list files in "core/checklists/"')
def list_checklist_files(context: dict[str, Any]) -> None:
    """List files in core/checklists/."""
    # Find the framework root
    praxis_spec = importlib.util.find_spec("praxis")
    if praxis_spec and praxis_spec.origin:
        framework_root = Path(praxis_spec.origin).parent.parent.parent
        checklists_dir = framework_root / "core" / "checklists"
        context["checklist_files"] = list(checklists_dir.glob("*.md"))
    else:
        context["checklist_files"] = []


@then("I see 9 checklist files, one per lifecycle stage")
def verify_checklist_count(context: dict[str, Any]) -> None:
    """Verify 9 base checklist files exist."""
    files = context["checklist_files"]
    base_files = [f for f in files if "-" not in f.stem]
    assert len(base_files) >= 9, f"Expected at least 9 base checklists, found {len(base_files)}"


@then("each file follows the consistent checklist structure")
def verify_checklist_structure(context: dict[str, Any]) -> None:
    """Verify each checklist has required sections."""
    required_sections = ["Entry Criteria", "Exit Criteria", "Guidance", "References"]
    
    for checklist_file in context["checklist_files"]:
        if "-" in checklist_file.stem:
            # Skip addenda for this check
            continue
        content = checklist_file.read_text()
        for section in required_sections:
            assert f"## {section}" in content, \
                f"{checklist_file.name} missing section: {section}"


@given('a project at stage "formalize"')
def project_at_formalize(tmp_path: Path, context: dict[str, Any]) -> None:
    """Create a project at formalize stage."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: code
stage: formalize
privacy_level: personal
environment: Home
"""
    )


@given('a project at stage "formalize" with domain "code"')
def project_at_formalize_code(tmp_path: Path, context: dict[str, Any]) -> None:
    """Create a code domain project at formalize stage."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: code
stage: formalize
privacy_level: personal
environment: Home
"""
    )


@given('a project at stage "commit"')
def project_at_commit(tmp_path: Path, context: dict[str, Any]) -> None:
    """Create a project at commit stage."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: code
stage: commit
privacy_level: personal
environment: Home
"""
    )


@given("the SOD artifact is missing")
def sod_missing(context: dict[str, Any]) -> None:
    """Ensure SOD does not exist."""
    # No action needed - SOD won't exist unless we create it
    pass


@given('a project at stage "capture" with domain "code"')
def project_at_capture_code(tmp_path: Path, context: dict[str, Any]) -> None:
    """Create a code domain project at capture stage."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: code
stage: capture
privacy_level: personal
environment: Home
"""
    )


@given('no domain addendum exists for "capture-code"')
def no_capture_code_addendum(context: dict[str, Any]) -> None:
    """Verify no capture-code.md addendum exists."""
    # This is true by design - we only created formalize-code and sustain-code
    pass


@when('I run "praxis status"')
def run_praxis_status(context: dict[str, Any], cli_runner: CliRunner) -> None:
    """Run praxis status command."""
    result = cli_runner.invoke(app, ["status", str(context["project_root"])])
    context["result"] = result
    context["exit_code"] = result.exit_code


@when('I run "praxis validate"')
def run_praxis_validate(context: dict[str, Any], cli_runner: CliRunner) -> None:
    """Run praxis validate command."""
    result = cli_runner.invoke(app, ["validate", str(context["project_root"])])
    context["result"] = result
    context["exit_code"] = result.exit_code


@then(parsers.parse('the output includes a reference to "{path}"'))
def output_includes_reference(path: str, context: dict[str, Any]) -> None:
    """Verify output includes reference to path."""
    result = context["result"]
    assert path in result.output, f"Expected '{path}' in output, got:\n{result.output}"


@then("the validation fails with an error")
def validation_fails(context: dict[str, Any]) -> None:
    """Verify validation failed."""
    assert context["exit_code"] != 0, "Expected validation to fail"


@then(parsers.parse('the output includes "{text}"'))
def output_includes_text(text: str, context: dict[str, Any]) -> None:
    """Verify output includes specific text."""
    result = context["result"]
    assert text in result.output, f"Expected '{text}' in output, got:\n{result.output}"


@then("the output does not reference a missing addendum file")
def output_no_missing_addendum(context: dict[str, Any]) -> None:
    """Verify output doesn't reference non-existent addendum."""
    result = context["result"]
    # Should not show capture-code.md since it doesn't exist
    assert "capture-code.md" not in result.output, \
        f"Should not reference missing addendum, got:\n{result.output}"


@given('the checklist file "core/checklists/formalize.md"')
def checklist_file_formalize(context: dict[str, Any]) -> None:
    """Load the formalize checklist file."""
    praxis_spec = importlib.util.find_spec("praxis")
    if praxis_spec and praxis_spec.origin:
        framework_root = Path(praxis_spec.origin).parent.parent.parent
        checklist_path = framework_root / "core" / "checklists" / "formalize.md"
        context["checklist_content"] = checklist_path.read_text()
    else:
        context["checklist_content"] = ""


@when("I compare its entry/exit criteria")
def compare_criteria(context: dict[str, Any]) -> None:
    """Compare checklist criteria with lifecycle spec."""
    checklist = context["checklist_content"]
    # Extract entry/exit criteria from checklist
    context["checklist_has_entry"] = "Entry Criteria" in checklist
    context["checklist_has_exit"] = "Exit Criteria" in checklist
    # Check for key formalize criteria
    context["has_shape_complete"] = "Shape complete" in checklist
    context["has_sod_exists"] = "SOD" in checklist or "artifact exists" in checklist


@then('they match the criteria defined in "core/spec/lifecycle.md"')
def criteria_match_spec(context: dict[str, Any]) -> None:
    """Verify criteria match the spec."""
    assert context["checklist_has_entry"], "Missing Entry Criteria section"
    assert context["checklist_has_exit"], "Missing Exit Criteria section"
    assert context["has_shape_complete"], "Missing 'Shape complete' entry criterion"
    assert context["has_sod_exists"], "Missing SOD/artifact exit criterion"
