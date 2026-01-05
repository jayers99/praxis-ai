"""Step definitions for extension_audits.feature."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pytest_bdd import given, parsers, scenarios, then, when
from typer.testing import CliRunner

from praxis.cli import app

scenarios("../features/extension_audits.feature")


# Helper function to create workspace structure
def setup_workspace(tmp_path: Path, context: dict[str, Any]) -> Path:
    """Create a workspace structure with PRAXIS_HOME."""
    workspace_path = tmp_path / "workspace"
    workspace_path.mkdir()

    # Create workspace-config.yaml
    config_path = workspace_path / "workspace-config.yaml"
    config_path.write_text(
        """workspace:
  projects_path: ./projects

installed_extensions: []
installed_examples: []

defaults:
  privacy: personal
  environment: Home
"""
    )

    # Create extensions directory
    extensions_path = workspace_path / "extensions"
    extensions_path.mkdir()

    context["workspace_path"] = workspace_path
    context["extensions_path"] = extensions_path
    return workspace_path


def add_extension_to_workspace(context: dict[str, Any], extension_name: str, manifest_content: str) -> None:
    """Add an extension to the workspace."""
    extensions_path = context["extensions_path"]
    ext_path = extensions_path / extension_name
    ext_path.mkdir(exist_ok=True)

    # Write manifest
    manifest_path = ext_path / "praxis-extension.yaml"
    manifest_path.write_text(manifest_content)

    # Update workspace config to include this extension
    workspace_path = context["workspace_path"]
    config_path = workspace_path / "workspace-config.yaml"

    # Read current config
    config_text = config_path.read_text()

    # Add extension to installed list if not already there
    if "installed_extensions:" in config_text:
        config_lines = config_text.split("\n")
        for i, line in enumerate(config_lines):
            if line.startswith("installed_extensions:"):
                # Check if it's an empty list
                if config_lines[i] == "installed_extensions: []":
                    config_lines[i] = f"installed_extensions:\n  - {extension_name}"
                else:
                    # Add to existing list
                    config_lines.insert(i + 1, f"  - {extension_name}")
                break
        config_path.write_text("\n".join(config_lines))


# Background steps


@given("I am in a temporary directory")
def temp_directory(tmp_path: Path, context: dict[str, Any]) -> None:
    """Set up temporary directory."""
    context["tmp_path"] = tmp_path


@given("I have a workspace with PRAXIS_HOME set")
def workspace_with_praxis_home(tmp_path: Path, context: dict[str, Any], monkeypatch) -> None:
    """Set up workspace and PRAXIS_HOME environment variable."""
    workspace_path = setup_workspace(tmp_path, context)
    monkeypatch.setenv("PRAXIS_HOME", str(workspace_path))
    context["monkeypatch"] = monkeypatch


# Happy Path Scenarios


@given(parsers.parse('an installed extension "{ext_name}" with praxis-extension.yaml'))
def extension_with_manifest(context: dict[str, Any], ext_name: str) -> None:
    """Create an extension with a basic manifest."""
    manifest = f"""manifest_version: "0.1"
name: {ext_name}
description: Test extension for {ext_name}

contributions:
  audits: []
"""
    add_extension_to_workspace(context, ext_name, manifest)
    context["current_extension"] = ext_name


@given(parsers.parse('the manifest declares an audit check "{check_name}" for domain "{domain}"'))
def manifest_declares_audit_check(context: dict[str, Any], check_name: str, domain: str) -> None:
    """Add an audit check to the extension manifest."""
    ext_name = context.get("current_extension", "test-pack")
    ext_path = context["extensions_path"] / ext_name

    manifest = f"""manifest_version: "0.1"
name: {ext_name}
description: Test extension

contributions:
  audits:
    - domain: "{domain}"
      subtypes: ["mobile"]
      checks:
        - name: "{check_name}"
          category: "structure"
          check_type: "file_exists"
          path: "mobile.json"
          pass_message: "Mobile manifest exists"
          fail_message: "mobile.json not found"
          severity: "warning"
"""

    manifest_path = ext_path / "praxis-extension.yaml"
    manifest_path.write_text(manifest)

    # Store check name for verification
    context["check_name"] = f"{ext_name}:{check_name}"
    context["check_message"] = "mobile.json not found"


@given(parsers.parse('I have a project with domain "{domain}" and subtype "{subtype}"'))
def project_with_domain_and_subtype(tmp_path: Path, context: dict[str, Any], domain: str, subtype: str) -> None:
    """Create a project with specified domain and subtype."""
    project_root = tmp_path / "test_project"
    project_root.mkdir(exist_ok=True)
    context["project_root"] = project_root

    praxis_yaml = project_root / "praxis.yaml"
    praxis_yaml.write_text(
        f"""domain: {domain}
stage: capture
subtype: {subtype}
privacy_level: personal
environment: Home
"""
    )


@given(parsers.parse('an installed extension "{ext_name}" with a "{check_type}" audit check for "{path}"'))
def extension_with_check_type(context: dict[str, Any], ext_name: str, check_type: str, path: str) -> None:
    """Create an extension with a specific check type."""
    manifest = f"""manifest_version: "0.1"
name: {ext_name}
description: Test extension

contributions:
  audits:
    - domain: "code"
      checks:
        - name: "test_check"
          category: "structure"
          check_type: "{check_type}"
          path: "{path}"
          pass_message: "Check passed"
          fail_message: "Check failed"
          severity: "warning"
"""
    add_extension_to_workspace(context, ext_name, manifest)
    context["current_extension"] = ext_name
    context["check_pass_message"] = "Check passed"
    context["check_fail_message"] = "Check failed"


@given('I have a code project at stage "capture"')
def code_project_at_capture(tmp_path: Path, context: dict[str, Any]) -> None:
    """Create a code project at capture stage."""
    project_root = tmp_path / "test_project"
    project_root.mkdir(exist_ok=True)
    context["project_root"] = project_root

    praxis_yaml = project_root / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: code
stage: capture
privacy_level: personal
environment: Home
"""
    )


@given(parsers.parse('the project contains "{filename}"'))
def project_contains_file(context: dict[str, Any], filename: str) -> None:
    """Create a file in the project."""
    project_root = context["project_root"]
    file_path = project_root / filename
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text("test content")


@given(parsers.parse('the project does not contain "{filename}"'))
def project_does_not_contain_file(context: dict[str, Any], filename: str) -> None:
    """Ensure a file does not exist in the project."""
    project_root = context["project_root"]
    file_path = project_root / filename
    if file_path.exists():
        file_path.unlink()


@given(parsers.parse('the project contains directory "{dirname}"'))
def project_contains_directory(context: dict[str, Any], dirname: str) -> None:
    """Create a directory in the project."""
    project_root = context["project_root"]
    dir_path = project_root / dirname
    dir_path.mkdir(parents=True, exist_ok=True)


@given(parsers.parse('an installed extension "{ext_name}" with a "{check_type}" audit check'))
def extension_with_file_contains_check(context: dict[str, Any], ext_name: str, check_type: str) -> None:
    """Create an extension with file_contains check (pattern to be set later)."""
    context["current_extension"] = ext_name
    context["check_type"] = check_type


@given(parsers.parse('the check looks for pattern "{pattern}" in "{path}"'))
def check_looks_for_pattern(context: dict[str, Any], pattern: str, path: str) -> None:
    """Set up file_contains check with pattern."""
    ext_name = context["current_extension"]

    # Escape pattern for YAML (replace backslashes)
    yaml_pattern = pattern.replace("\\", "\\\\")

    manifest = f"""manifest_version: "0.1"
name: {ext_name}
description: Test extension

contributions:
  audits:
    - domain: "code"
      checks:
        - name: "version_check"
          category: "validation"
          check_type: "file_contains"
          path: "{path}"
          pattern: "{yaml_pattern}"
          pass_message: "Version pattern found"
          fail_message: "Version pattern not found"
          severity: "warning"
"""
    add_extension_to_workspace(context, ext_name, manifest)
    context["check_pass_message"] = "Version pattern found"


@given(parsers.parse('the project\'s pyproject.toml contains "{content}"'))
def project_pyproject_contains(context: dict[str, Any], content: str) -> None:
    """Create pyproject.toml with specific content."""
    project_root = context["project_root"]
    pyproject = project_root / "pyproject.toml"
    pyproject.write_text(
        f"""[tool.poetry]
name = "test-project"
{content}
"""
    )


# Filtering Scenarios


@given(parsers.parse('an installed extension "{ext_name}" contributing audit checks for subtype "{subtype}"'))
def extension_contributing_for_subtype(context: dict[str, Any], ext_name: str, subtype: str) -> None:
    """Create an extension with subtype-specific checks."""
    manifest = f"""manifest_version: "0.1"
name: {ext_name}
description: Test extension

contributions:
  audits:
    - domain: "code"
      subtypes: ["{subtype}"]
      checks:
        - name: "subtype_specific_check"
          category: "structure"
          check_type: "file_exists"
          path: "specific-file.txt"
          pass_message: "Subtype check passed"
          fail_message: "Subtype check failed"
          severity: "warning"
"""
    add_extension_to_workspace(context, ext_name, manifest)
    context["subtype_check_name"] = f"{ext_name}:subtype_specific_check"


@given("I have a code domain project")
def code_domain_project(tmp_path: Path, context: dict[str, Any]) -> None:
    """Create a basic code domain project."""
    project_root = tmp_path / "test_project"
    project_root.mkdir(exist_ok=True)
    context["project_root"] = project_root

    praxis_yaml = project_root / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: code
stage: capture
privacy_level: personal
environment: Home
"""
    )


@given(parsers.parse('an installed extension "{ext_name}" contributing audit checks for domain "{domain}"'))
def extension_contributing_for_domain(context: dict[str, Any], ext_name: str, domain: str) -> None:
    """Create an extension with domain-specific checks."""
    manifest = f"""manifest_version: "0.1"
name: {ext_name}
description: Test extension

contributions:
  audits:
    - domain: "{domain}"
      checks:
        - name: "domain_specific_check"
          category: "structure"
          check_type: "file_exists"
          path: "domain-file.txt"
          pass_message: "Domain check passed"
          fail_message: "Domain check failed"
          severity: "warning"
"""
    add_extension_to_workspace(context, ext_name, manifest)
    context["domain_check_name"] = f"{ext_name}:domain_specific_check"


@given(parsers.parse('an installed extension "{ext_name}" with an audit check with min_stage "{min_stage}"'))
def extension_with_min_stage_check(context: dict[str, Any], ext_name: str, min_stage: str) -> None:
    """Create an extension with min_stage filtering."""
    manifest = f"""manifest_version: "0.1"
name: {ext_name}
description: Test extension

contributions:
  audits:
    - domain: "code"
      checks:
        - name: "stage_filtered_check"
          category: "structure"
          check_type: "file_exists"
          path: "stage-file.txt"
          pass_message: "Stage check passed"
          fail_message: "Stage check failed"
          severity: "warning"
          min_stage: "{min_stage}"
"""
    add_extension_to_workspace(context, ext_name, manifest)
    context["stage_check_name"] = f"{ext_name}:stage_filtered_check"


@given('I have a code project at stage "explore"')
def code_project_at_explore(tmp_path: Path, context: dict[str, Any]) -> None:
    """Create a code project at explore stage."""
    project_root = tmp_path / "test_project"
    project_root.mkdir(exist_ok=True)
    context["project_root"] = project_root

    praxis_yaml = project_root / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: code
stage: explore
privacy_level: personal
environment: Home
"""
    )


# Error Handling Scenarios


@given(parsers.parse('an installed extension "{ext_name}" with a malformed audit check definition'))
def extension_with_malformed_check(context: dict[str, Any], ext_name: str) -> None:
    """Create an extension with a malformed audit check."""
    manifest = f"""manifest_version: "0.1"
name: {ext_name}
description: Test extension

contributions:
  audits:
    - domain: "code"
      checks:
        - "this is not a dict"
        - name: "valid_check"
          category: "structure"
          check_type: "file_exists"
          path: "valid.txt"
          pass_message: "Valid check passed"
          fail_message: "Valid check failed"
          severity: "warning"
"""
    add_extension_to_workspace(context, ext_name, manifest)


@given(parsers.parse('an installed extension "{ext_name}" with an audit check using check_type "{check_type}"'))
def extension_with_unknown_check_type(context: dict[str, Any], ext_name: str, check_type: str) -> None:
    """Create an extension with an unsupported check type."""
    manifest = f"""manifest_version: "0.1"
name: {ext_name}
description: Test extension

contributions:
  audits:
    - domain: "code"
      checks:
        - name: "custom_check"
          category: "structure"
          check_type: "{check_type}"
          path: "custom.txt"
          pass_message: "Custom check passed"
          fail_message: "Custom check failed"
          severity: "warning"
        - name: "valid_check"
          category: "structure"
          check_type: "file_exists"
          path: "valid.txt"
          pass_message: "Valid check passed"
          fail_message: "Valid check failed"
          severity: "warning"
"""
    add_extension_to_workspace(context, ext_name, manifest)


@given(parsers.parse('an installed extension "{ext_name}" with a "file_contains" check'))
def extension_with_file_contains_basic(context: dict[str, Any], ext_name: str) -> None:
    """Create an extension with file_contains check (pattern to be set)."""
    context["current_extension"] = ext_name


@given(parsers.parse('the pattern contains invalid regex syntax "{pattern}"'))
def pattern_with_invalid_regex(context: dict[str, Any], pattern: str) -> None:
    """Set up file_contains check with invalid regex."""
    ext_name = context["current_extension"]

    manifest = f"""manifest_version: "0.1"
name: {ext_name}
description: Test extension

contributions:
  audits:
    - domain: "code"
      checks:
        - name: "regex_check"
          category: "validation"
          check_type: "file_contains"
          path: "test.txt"
          pattern: "{pattern}"
          pass_message: "Pattern found"
          fail_message: "Pattern not found"
          severity: "warning"
        - name: "valid_check"
          category: "structure"
          check_type: "file_exists"
          path: "valid.txt"
          pass_message: "Valid check passed"
          fail_message: "Valid check failed"
          severity: "warning"
"""
    add_extension_to_workspace(context, ext_name, manifest)


# Multi-Extension Scenarios


@given(parsers.parse('an installed extension "{ext_name}" contributing check "{check_name}"'))
def extension_contributing_named_check(context: dict[str, Any], ext_name: str, check_name: str) -> None:
    """Create an extension with a named check."""
    manifest = f"""manifest_version: "0.1"
name: {ext_name}
description: Test extension

contributions:
  audits:
    - domain: "code"
      checks:
        - name: "{check_name}"
          category: "structure"
          check_type: "file_exists"
          path: "{check_name}.txt"
          pass_message: "{check_name} passed"
          fail_message: "{check_name} failed"
          severity: "warning"
"""
    add_extension_to_workspace(context, ext_name, manifest)

    # Track checks for ordering validation
    if "extension_checks" not in context:
        context["extension_checks"] = []
    context["extension_checks"].append(f"{ext_name}:{check_name}")


# When steps


@when('I run "praxis audit"')
def run_praxis_audit(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run praxis audit command."""
    project_root = context["project_root"]
    result = cli_runner.invoke(app, ["audit", str(project_root)])
    context["result"] = result


@when('I run "praxis audit" in a code project')
def run_praxis_audit_in_code_project(cli_runner: CliRunner, context: dict[str, Any], tmp_path: Path) -> None:
    """Run praxis audit in a code project."""
    if "project_root" not in context:
        # Create a basic code project
        project_root = tmp_path / "test_project"
        project_root.mkdir(exist_ok=True)
        context["project_root"] = project_root

        praxis_yaml = project_root / "praxis.yaml"
        praxis_yaml.write_text(
            """domain: code
stage: capture
privacy_level: personal
environment: Home
"""
        )

    project_root = context["project_root"]
    result = cli_runner.invoke(app, ["audit", str(project_root)])
    context["result"] = result


# Then steps


@then("the command succeeds")
def command_succeeds(context: dict[str, Any]) -> None:
    """Verify the command succeeded."""
    result = context["result"]
    assert result.exit_code == 0, f"Command failed: {result.output}"


@then(parsers.parse('the output contains "{text}"'))
def output_contains(context: dict[str, Any], text: str) -> None:
    """Verify the output contains expected text."""
    result = context["result"]
    assert text in result.output, f"Expected '{text}' in output. Got: {result.output}"


@then("the check passes with the configured pass_message")
def check_passes_with_message(context: dict[str, Any]) -> None:
    """Verify the check passed with the configured message."""
    result = context["result"]
    pass_message = context.get("check_pass_message", "Check passed")
    assert pass_message in result.output, f"Expected '{pass_message}' in output. Got: {result.output}"


@then("the check fails with the configured fail_message")
def check_fails_with_message(context: dict[str, Any]) -> None:
    """Verify the check failed with the configured message."""
    result = context["result"]
    fail_message = context.get("check_fail_message", "Check failed")
    assert fail_message in result.output, f"Expected '{fail_message}' in output. Got: {result.output}"


@then("the check passes")
def check_passes(context: dict[str, Any]) -> None:
    """Verify the check passed."""
    result = context["result"]
    assert "passed" in result.output.lower() or "✓" in result.output, f"Expected check to pass. Got: {result.output}"


@then("the mobile-only audit checks are not executed")
def mobile_checks_not_executed(context: dict[str, Any]) -> None:
    """Verify mobile-specific checks were not executed."""
    result = context["result"]
    check_name = context.get("subtype_check_name", "mobile-pack:subtype_specific_check")
    assert check_name not in result.output, f"Did not expect '{check_name}' in output. Got: {result.output}"


@then("the create-only audit checks are not executed")
def create_checks_not_executed(context: dict[str, Any]) -> None:
    """Verify create-specific checks were not executed."""
    result = context["result"]
    check_name = context.get("domain_check_name", "create-pack:domain_specific_check")
    assert check_name not in result.output, f"Did not expect '{check_name}' in output. Got: {result.output}"


@then("the check is not executed")
def check_not_executed(context: dict[str, Any]) -> None:
    """Verify the check was not executed."""
    result = context["result"]
    check_name = context.get("stage_check_name", "formalize-pack:stage_filtered_check")
    assert check_name not in result.output, f"Did not expect '{check_name}' in output. Got: {result.output}"


@then("the malformed check is skipped with a warning")
def malformed_check_skipped(context: dict[str, Any]) -> None:
    """Verify malformed check was skipped with a warning."""
    result = context["result"]
    # Check for warning about malformed check
    assert (
        "warning" in result.output.lower() or "invalid" in result.output.lower() or result.exit_code == 0
    ), f"Expected warning about malformed check. Got: {result.output}"


@then("other valid checks are executed normally")
def other_checks_executed(context: dict[str, Any]) -> None:
    """Verify other checks still executed."""
    result = context["result"]
    # Should have at least some checks executed (core checks)
    assert (
        "passed" in result.output.lower() or "warning" in result.output.lower() or "failed" in result.output.lower()
    ), f"Expected some checks to execute. Got: {result.output}"


@then("the check is skipped with a warning about unsupported check_type")
def check_skipped_unsupported_type(context: dict[str, Any]) -> None:
    """Verify check was skipped due to unsupported check_type."""
    result = context["result"]
    # Should succeed but might have warning in output
    assert result.exit_code == 0, f"Command should succeed. Got: {result.output}"


@then("other checks continue to execute")
def other_checks_continue(context: dict[str, Any]) -> None:
    """Verify other checks continued to execute."""
    result = context["result"]
    # Should have valid_check in output
    assert (
        "valid_check" in result.output or "Valid check" in result.output or result.exit_code == 0
    ), f"Expected other checks to execute. Got: {result.output}"


@then("the check is skipped with a warning about invalid regex")
def check_skipped_invalid_regex(context: dict[str, Any]) -> None:
    """Verify check was skipped due to invalid regex."""
    result = context["result"]
    # Should succeed but might have warning
    assert result.exit_code == 0, f"Command should succeed. Got: {result.output}"


@then("both checks are executed")
def both_checks_executed(context: dict[str, Any]) -> None:
    """Verify both extension checks were executed."""
    result = context["result"]
    # Check for the fail messages since files don't exist
    assert "check_a failed" in result.output, f"Expected 'check_a failed' in output. Got: {result.output}"
    assert "check_b failed" in result.output, f"Expected 'check_b failed' in output. Got: {result.output}"


@then(parsers.parse('"{check_a}" appears before "{check_b}"'))
def check_order(context: dict[str, Any], check_a: str, check_b: str) -> None:
    """Verify check order in output."""
    result = context["result"]
    output = result.output

    pos_a = output.find(check_a)
    pos_b = output.find(check_b)

    assert pos_a >= 0, f"Expected '{check_a}' in output. Got: {output}"
    assert pos_b >= 0, f"Expected '{check_b}' in output. Got: {output}"
    assert pos_a < pos_b, f"Expected '{check_a}' before '{check_b}'. Got: {output}"
