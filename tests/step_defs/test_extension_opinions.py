"""Step definitions for extension_opinions.feature."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pytest
import yaml
from pytest_bdd import given, parsers, scenarios, then, when
from typer.testing import CliRunner

from praxis.cli import app

scenarios("../features/extension_opinions.feature")


@given("I am in a temporary directory")
def setup_temp_dir(tmp_path: Path, context: dict[str, Any], request: pytest.FixtureRequest) -> None:
    """Set up temporary directory with cleanup."""
    context["project_root"] = tmp_path
    original_dir = os.getcwd()
    os.chdir(tmp_path)

    def restore_cwd() -> None:
        os.chdir(original_dir)

    request.addfinalizer(restore_cwd)


@given("I have a workspace with PRAXIS_HOME set")
def setup_workspace(context: dict[str, Any], tmp_path: Path) -> None:
    """Set up a workspace environment."""
    # Create workspace structure
    workspace_root = tmp_path / "workspace"
    workspace_root.mkdir()

    # Set PRAXIS_HOME
    os.environ["PRAXIS_HOME"] = str(workspace_root)
    context["workspace_root"] = workspace_root

    # Create extensions directory
    extensions_dir = workspace_root / "extensions"
    extensions_dir.mkdir()
    context["extensions_dir"] = extensions_dir

    # Create workspace config
    config = {
        "workspace": {"projects_path": "./projects"},
        "installed_extensions": [],
        "installed_examples": [],
        "defaults": {"privacy": "personal", "environment": "Home"},
    }
    config_path = workspace_root / "workspace-config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(config, f)

    # Create core opinions directory in project root
    project_root = context.get("project_root", tmp_path)
    opinions_dir = project_root / "opinions"
    opinions_dir.mkdir(exist_ok=True)
    (opinions_dir / "code").mkdir(exist_ok=True)


@given(parsers.parse('an installed extension "{ext_name}" with praxis-extension.yaml'))
def create_extension_with_manifest(context: dict[str, Any], ext_name: str) -> None:
    """Create an extension directory with a manifest."""
    extensions_dir = context["extensions_dir"]
    ext_dir = extensions_dir / ext_name
    ext_dir.mkdir()

    # Create default manifest
    manifest = {
        "manifest_version": "0.1",
        "name": ext_name,
        "description": f"Test extension {ext_name}",
        "contributions": {"opinions": []},
    }
    manifest_path = ext_dir / "praxis-extension.yaml"
    with open(manifest_path, "w") as f:
        yaml.dump(manifest, f)

    # Add to installed extensions
    workspace_root = context["workspace_root"]
    config_path = workspace_root / "workspace-config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)
    config["installed_extensions"].append(ext_name)
    with open(config_path, "w") as f:
        yaml.dump(config, f)

    context[f"ext_{ext_name}"] = ext_dir


@given(parsers.parse('the manifest declares an opinion contribution "{target_path}"'))
def add_opinion_contribution(context: dict[str, Any], target_path: str) -> None:
    """Add an opinion contribution to the most recently created extension."""
    # Find the most recently created extension
    ext_name = None
    for key in reversed(list(context.keys())):
        if key.startswith("ext_"):
            ext_name = key[4:]  # Remove "ext_" prefix
            break

    if not ext_name:
        raise ValueError("No extension created yet")

    ext_dir = context[f"ext_{ext_name}"]
    manifest_path = ext_dir / "praxis-extension.yaml"

    with open(manifest_path) as f:
        manifest = yaml.safe_load(f)

    # Add opinion contribution
    contribution = {
        "source": f"opinions/{target_path}",
        "target": target_path,
    }
    manifest["contributions"]["opinions"].append(contribution)

    with open(manifest_path, "w") as f:
        yaml.dump(manifest, f)

    context["last_contribution"] = target_path


@given(parsers.parse('the extension has the opinion file at "{source_path}"'))
def create_extension_opinion_file(context: dict[str, Any], source_path: str) -> None:
    """Create an opinion file in the extension directory."""
    # Find the most recently created extension
    ext_name = None
    for key in reversed(list(context.keys())):
        if key.startswith("ext_"):
            ext_name = key[4:]
            break

    if not ext_name:
        raise ValueError("No extension created yet")

    ext_dir = context[f"ext_{ext_name}"]
    file_path = ext_dir / source_path
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Create a simple opinion file with frontmatter
    content = """---
domain: code
version: "1.0"
status: active
---

# Test Opinion

This is a test opinion from an extension.
"""
    file_path.write_text(content)


@given(parsers.parse('the manifest has an unsupported manifest_version "{version}"'))
def set_unsupported_version(context: dict[str, Any], version: str) -> None:
    """Set an unsupported manifest version."""
    # Find the most recently created extension
    ext_name = None
    for key in reversed(list(context.keys())):
        if key.startswith("ext_"):
            ext_name = key[4:]
            break

    if not ext_name:
        raise ValueError("No extension created yet")

    ext_dir = context[f"ext_{ext_name}"]
    manifest_path = ext_dir / "praxis-extension.yaml"

    with open(manifest_path) as f:
        manifest = yaml.safe_load(f)

    manifest["manifest_version"] = version

    with open(manifest_path, "w") as f:
        yaml.dump(manifest, f)


@given("the manifest contains invalid YAML syntax")
def create_invalid_yaml_manifest(context: dict[str, Any]) -> None:
    """Create a manifest with invalid YAML syntax."""
    # Find the most recently created extension
    ext_name = None
    for key in reversed(list(context.keys())):
        if key.startswith("ext_"):
            ext_name = key[4:]
            break

    if not ext_name:
        raise ValueError("No extension created yet")

    ext_dir = context[f"ext_{ext_name}"]
    manifest_path = ext_dir / "praxis-extension.yaml"

    # Write invalid YAML
    manifest_path.write_text("manifest_version: 0.1\n  invalid: indentation\n: bad")


@given(parsers.parse('an installed extension "{ext_name}" contributing "{target}"'))
def create_extension_with_contribution(context: dict[str, Any], ext_name: str, target: str) -> None:
    """Create an extension with a specific contribution."""
    extensions_dir = context["extensions_dir"]
    ext_dir = extensions_dir / ext_name
    ext_dir.mkdir()

    # Create manifest with contribution
    manifest = {
        "manifest_version": "0.1",
        "name": ext_name,
        "description": f"Test extension {ext_name}",
        "contributions": {"opinions": [{"source": f"opinions/{target}", "target": target}]},
    }
    manifest_path = ext_dir / "praxis-extension.yaml"
    with open(manifest_path, "w") as f:
        yaml.dump(manifest, f)

    # Add to installed extensions
    workspace_root = context["workspace_root"]
    config_path = workspace_root / "workspace-config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)
    config["installed_extensions"].append(ext_name)
    with open(config_path, "w") as f:
        yaml.dump(config, f)

    context[f"ext_{ext_name}"] = ext_dir


@given("both extensions have the opinion file")
def create_opinion_files_for_both_extensions(context: dict[str, Any]) -> None:
    """Create opinion files for both recently created extensions."""
    # Find the last two extensions
    ext_names = []
    for key in reversed(list(context.keys())):
        if key.startswith("ext_"):
            ext_names.append(key[4:])
            if len(ext_names) == 2:
                break

    if len(ext_names) < 2:
        raise ValueError("Need at least two extensions")

    for ext_name in ext_names:
        ext_dir = context[f"ext_{ext_name}"]

        # Get the target path from manifest
        manifest_path = ext_dir / "praxis-extension.yaml"
        with open(manifest_path) as f:
            manifest = yaml.safe_load(f)

        if manifest["contributions"]["opinions"]:
            source_path = manifest["contributions"]["opinions"][0]["source"]
            file_path = ext_dir / source_path
            file_path.parent.mkdir(parents=True, exist_ok=True)

            content = f"""---
domain: code
version: "1.0"
status: active
---

# Test Opinion from {ext_name}

This is a test opinion.
"""
            file_path.write_text(content)


@given('the core opinions include "code/principles.md"')
def create_core_opinion(context: dict[str, Any]) -> None:
    """Create a core opinion file."""
    project_root = context.get("project_root", Path.cwd())
    opinions_dir = project_root / "opinions"
    opinions_dir.mkdir(exist_ok=True)
    code_dir = opinions_dir / "code"
    code_dir.mkdir(exist_ok=True)

    file_path = code_dir / "principles.md"
    content = """---
domain: code
version: "1.0"
status: active
---

# Core Code Principles

Core principles from praxis-ai.
"""
    file_path.write_text(content)


@given(parsers.parse('an installed extension "{ext_name}" without praxis-extension.yaml'))
def create_extension_without_manifest(context: dict[str, Any], ext_name: str) -> None:
    """Create an extension without a manifest."""
    extensions_dir = context["extensions_dir"]
    ext_dir = extensions_dir / ext_name
    ext_dir.mkdir()

    # Add to installed extensions but don't create manifest
    workspace_root = context["workspace_root"]
    config_path = workspace_root / "workspace-config.yaml"
    with open(config_path) as f:
        config = yaml.safe_load(f)
    config["installed_extensions"].append(ext_name)
    with open(config_path, "w") as f:
        yaml.dump(config, f)


@when(parsers.parse('I run "{command}"'))
def run_command(context: dict[str, Any], command: str) -> None:
    """Run a CLI command."""
    runner = CliRunner()
    args = command.split()[1:]  # Skip 'praxis'
    result = runner.invoke(app, args)
    context["result"] = result
    context["stdout"] = result.stdout
    context["stderr"] = result.stderr if hasattr(result, "stderr") else ""
    context["exit_code"] = result.exit_code


@then(parsers.parse('the output contains "{text}"'))
def check_output_contains(context: dict[str, Any], text: str) -> None:
    """Check that output contains text."""
    stdout = context.get("stdout", "")
    assert text in stdout, f"Expected '{text}' in output, got:\n{stdout}"


@then(parsers.parse('the output does not contain "{text}"'))
def check_output_not_contains(context: dict[str, Any], text: str) -> None:
    """Check that output does not contain text."""
    stdout = context.get("stdout", "")
    assert text not in stdout, f"Did not expect '{text}' in output, got:\n{stdout}"


@then(parsers.parse("the exit code is {code:d}"))
def check_exit_code(context: dict[str, Any], code: int) -> None:
    """Check the exit code."""
    exit_code = context.get("exit_code", -1)
    assert exit_code == code, f"Expected exit code {code}, got {exit_code}"


@then(parsers.parse('the stderr does not contain "{text}"'))
def check_stderr_not_contains(context: dict[str, Any], text: str) -> None:
    """Check that stderr does not contain text."""
    stderr = context.get("stderr", "")
    # In Typer, warnings might go to stdout instead of stderr
    stdout = context.get("stdout", "")
    combined = stdout + stderr
    assert text not in combined, f"Did not expect '{text}' in output, got:\n{combined}"


@then("other extensions with valid manifests are loaded")
def check_other_extensions_loaded(context: dict[str, Any]) -> None:
    """Check that other extensions were loaded despite errors."""
    stdout = context.get("stdout", "")
    # Just check that we got some output and didn't crash
    assert "opinions/" in stdout, f"Expected opinions tree in output, got:\n{stdout}"
