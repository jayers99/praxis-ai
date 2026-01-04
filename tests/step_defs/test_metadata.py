"""Step definitions for metadata.feature."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pytest_bdd import given, parsers, scenarios, then, when
from typer.testing import CliRunner

from praxis.cli import app

scenarios("../features/metadata.feature")


# Reuse common step definitions from other tests


@given("an empty directory")
def empty_directory(tmp_path: Path, context: dict[str, Any]) -> None:
    """Use the pytest tmp_path as an empty parent directory."""
    context["parent_dir"] = tmp_path
    context["project_root"] = tmp_path


@when(
    parsers.parse(
        'I run praxis new "{name}" with domain "{domain}" and privacy "{privacy}"'
    )
)
def run_new_with_flags(
    cli_runner: CliRunner,
    context: dict[str, Any],
    name: str,
    domain: str,
    privacy: str,
) -> None:
    """Run praxis new command."""
    parent_dir = context.get("parent_dir", context.get("project_root"))
    result = cli_runner.invoke(
        app,
        [
            "new",
            name,
            "--domain",
            domain,
            "--privacy",
            privacy,
            "--path",
            str(parent_dir),
            "--quiet",
        ],
    )
    context["result"] = result
    context["project_root"] = parent_dir / name


@when("I run praxis status")
def run_status(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run praxis status command."""
    project_root: Path = context["project_root"]
    result = cli_runner.invoke(app, ["status", str(project_root)])
    context["result"] = result


@when("I run praxis validate")
def run_validate(cli_runner: CliRunner, context: dict[str, Any]) -> None:
    """Run praxis validate command."""
    project_root: Path = context["project_root"]
    result = cli_runner.invoke(app, ["validate", str(project_root)])
    context["result"] = result


@then(parsers.parse('praxis.yaml should contain name "{expected_name}"'))
def check_praxis_yaml_name(context: dict[str, Any], expected_name: str) -> None:
    """Verify praxis.yaml contains the expected name."""
    project_root: Path = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"
    assert praxis_yaml.exists(), "praxis.yaml should exist"
    content = yaml.safe_load(praxis_yaml.read_text())
    actual_name = content.get("name", "")
    assert actual_name == expected_name, (
        f"Expected name '{expected_name}', got '{actual_name}'"
    )


@then(parsers.parse('praxis.yaml should contain slug "{expected_slug}"'))
def check_praxis_yaml_slug(context: dict[str, Any], expected_slug: str) -> None:
    """Verify praxis.yaml contains the expected slug."""
    project_root: Path = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"
    assert praxis_yaml.exists(), "praxis.yaml should exist"
    content = yaml.safe_load(praxis_yaml.read_text())
    actual_slug = content.get("slug", "")
    assert actual_slug == expected_slug, (
        f"Expected slug '{expected_slug}', got '{actual_slug}'"
    )


@then(parsers.parse('praxis.yaml should contain description "{expected_desc}"'))
def check_praxis_yaml_description(context: dict[str, Any], expected_desc: str) -> None:
    """Verify praxis.yaml contains the expected description."""
    project_root: Path = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"
    assert praxis_yaml.exists(), "praxis.yaml should exist"
    content = yaml.safe_load(praxis_yaml.read_text())
    actual_desc = content.get("description", "")
    assert actual_desc == expected_desc, (
        f"Expected description '{expected_desc}', got '{actual_desc}'"
    )


@then("praxis.yaml should have empty description")
def check_praxis_yaml_empty_description(context: dict[str, Any]) -> None:
    """Verify praxis.yaml has an empty description."""
    project_root: Path = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"
    assert praxis_yaml.exists(), "praxis.yaml should exist"
    content = yaml.safe_load(praxis_yaml.read_text())
    desc = content.get("description", None)
    assert desc == "", f"Expected empty description, got '{desc}'"


@then("praxis.yaml should contain empty tags")
def check_praxis_yaml_empty_tags(context: dict[str, Any]) -> None:
    """Verify praxis.yaml contains an empty tags list."""
    project_root: Path = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"
    assert praxis_yaml.exists(), "praxis.yaml should exist"
    content = yaml.safe_load(praxis_yaml.read_text())
    tags = content.get("tags", None)
    assert tags == [], f"Expected empty tags list, got {tags}"


@given(
    parsers.parse('a project with name "{name}" and slug "{slug}"')
)
def project_with_name_and_slug(
    tmp_path: Path, context: dict[str, Any], name: str, slug: str
) -> None:
    """Create a project with specific name and slug."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        f"""domain: code
stage: capture
privacy_level: personal
environment: Home
name: {name}
slug: {slug}
description: ''
tags: []
"""
    )


@given(
    parsers.parse('a project directory "{dirname}" with no metadata fields')
)
def project_directory_no_metadata(
    tmp_path: Path, context: dict[str, Any], dirname: str
) -> None:
    """Create a project directory with legacy praxis.yaml (no metadata fields)."""
    # Create the subdirectory with the specified name
    project_dir = tmp_path / dirname
    project_dir.mkdir()
    context["project_root"] = project_dir

    praxis_yaml = project_dir / "praxis.yaml"
    praxis_yaml.write_text(
        """domain: code
stage: capture
privacy_level: personal
environment: Home
"""
    )


@then(parsers.parse('slug should be auto-generated as "{expected_slug}"'))
def check_auto_generated_slug(context: dict[str, Any], expected_slug: str) -> None:
    """Verify slug was auto-generated correctly (in memory, not persisted)."""
    # The slug is auto-generated during load but not written back
    # We verify this by checking the output or re-loading the config
    from praxis.infrastructure.yaml_loader import load_praxis_config

    project_root: Path = context["project_root"]
    result = load_praxis_config(project_root)
    assert result.valid, "Config should be valid"
    assert result.config is not None, "Config should be loaded"
    actual_slug = result.config.slug
    assert actual_slug == expected_slug, (
        f"Expected auto-generated slug '{expected_slug}', got '{actual_slug}'"
    )


@then(parsers.parse('name should be auto-generated as "{expected_name}"'))
def check_auto_generated_name(context: dict[str, Any], expected_name: str) -> None:
    """Verify name was auto-generated correctly (in memory, not persisted)."""
    from praxis.infrastructure.yaml_loader import load_praxis_config

    project_root: Path = context["project_root"]
    result = load_praxis_config(project_root)
    assert result.valid, "Config should be valid"
    assert result.config is not None, "Config should be loaded"
    actual_name = result.config.name
    assert actual_name == expected_name, (
        f"Expected auto-generated name '{expected_name}', got '{actual_name}'"
    )


@given(parsers.parse('a praxis.yaml with slug "{slug}"'))
def praxis_yaml_with_slug(
    tmp_path: Path, context: dict[str, Any], slug: str
) -> None:
    """Create a praxis.yaml with a specific slug."""
    context["project_root"] = tmp_path
    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        f"""domain: code
stage: capture
privacy_level: personal
environment: Home
slug: {slug}
"""
    )


@given(
    parsers.parse('a project with description "{description}" and tags "{tags}"')
)
def project_with_description_and_tags(
    tmp_path: Path, context: dict[str, Any], description: str, tags: str
) -> None:
    """Create a project with specific description and tags."""
    context["project_root"] = tmp_path
    # Handle empty tags string
    if tags.strip():
        tags_list = [tag.strip() for tag in tags.split(",")]
    else:
        tags_list = []
    tags_yaml = yaml.dump(tags_list, default_flow_style=True).strip()

    praxis_yaml = tmp_path / "praxis.yaml"
    praxis_yaml.write_text(
        f"""domain: code
stage: capture
privacy_level: personal
environment: Home
name: My Project
slug: my-project
description: {description}
tags: {tags_yaml}
"""
    )


@given(parsers.parse('a directory named "{dirname}"'))
def directory_named(tmp_path: Path, context: dict[str, Any], dirname: str) -> None:
    """Create a directory with a specific name."""
    project_dir = tmp_path / dirname
    project_dir.mkdir()
    context["project_root"] = project_dir


@when('I run praxis init with domain "code" and privacy "personal"')
def run_init_with_domain_privacy(
    cli_runner: CliRunner, context: dict[str, Any]
) -> None:
    """Run praxis init command."""
    project_root: Path = context["project_root"]
    result = cli_runner.invoke(
        app,
        [
            "init",
            str(project_root),
            "--domain",
            "code",
            "--privacy",
            "personal",
            "--quiet",
        ],
    )
    context["result"] = result
