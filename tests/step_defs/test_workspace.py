"""Step definitions for workspace management BDD tests."""

from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from praxis.application.workspace_service import (
    get_workspace_info,
    init_workspace,
    require_praxis_home,
)
from praxis.domain.workspace import WorkspaceInfo, WorkspaceInitResult

scenarios("../features/workspace.feature")


@pytest.fixture
def context() -> dict[str, Any]:
    """Shared context for step definitions."""
    return {}


@pytest.fixture
def temp_workspace(context: dict[str, Any]) -> Path:
    """Create a temporary workspace directory."""
    temp_dir = Path(tempfile.mkdtemp(prefix="praxis_test_"))
    context["temp_workspace"] = temp_dir
    yield temp_dir
    # Cleanup
    if temp_dir.exists():
        shutil.rmtree(temp_dir)


@given("PRAXIS_HOME is set to a temp directory")
def praxis_home_set_to_temp(temp_workspace: Path, context: dict[str, Any]) -> None:
    """Set PRAXIS_HOME to temp directory."""
    context["original_praxis_home"] = os.environ.get("PRAXIS_HOME")
    os.environ["PRAXIS_HOME"] = str(temp_workspace)
    context["praxis_home"] = temp_workspace


@given("the temp workspace directory exists")
def temp_workspace_exists(temp_workspace: Path) -> None:
    """Ensure temp workspace directory exists."""
    temp_workspace.mkdir(parents=True, exist_ok=True)


@given("a valid workspace exists at PRAXIS_HOME")
def valid_workspace_exists(temp_workspace: Path, context: dict[str, Any]) -> None:
    """Create a valid workspace structure."""
    # Create directories
    (temp_workspace / "extensions").mkdir(exist_ok=True)
    (temp_workspace / "examples").mkdir(exist_ok=True)
    (temp_workspace / "projects").mkdir(exist_ok=True)

    # Create config file
    config_content = """workspace:
  projects_path: ./projects
installed_extensions: []
installed_examples: []
defaults:
  privacy: personal
  environment: Home
"""
    (temp_workspace / "workspace-config.yaml").write_text(config_content)


@given("PRAXIS_HOME is not set")
def praxis_home_not_set(context: dict[str, Any]) -> None:
    """Unset PRAXIS_HOME."""
    context["original_praxis_home"] = os.environ.get("PRAXIS_HOME")
    if "PRAXIS_HOME" in os.environ:
        del os.environ["PRAXIS_HOME"]


@when("I call init_workspace")
def call_init_workspace(temp_workspace: Path, context: dict[str, Any]) -> None:
    """Call init_workspace."""
    result = init_workspace(temp_workspace)
    context["init_result"] = result


@when("I call get_workspace_info")
def call_get_workspace_info(temp_workspace: Path, context: dict[str, Any]) -> None:
    """Call get_workspace_info."""
    info = get_workspace_info(temp_workspace)
    context["workspace_info"] = info


@when("I call require_praxis_home")
def call_require_praxis_home(context: dict[str, Any]) -> None:
    """Call require_praxis_home and capture exception."""
    try:
        require_praxis_home()
        context["exception"] = None
    except ValueError as e:
        context["exception"] = e


@then("the init result should be successful")
def init_result_successful(context: dict[str, Any]) -> None:
    """Check init result is successful."""
    result: WorkspaceInitResult = context["init_result"]
    assert result.success, f"Init failed with errors: {result.errors}"


@then(parsers.parse('the directory "{dirname}" should exist in workspace'))
def directory_exists_in_workspace(
    dirname: str, temp_workspace: Path, context: dict[str, Any]
) -> None:
    """Check directory exists in workspace."""
    dir_path = temp_workspace / dirname
    assert dir_path.exists(), f"Directory {dirname} does not exist"
    assert dir_path.is_dir(), f"{dirname} is not a directory"


@then(parsers.parse('the file "{filename}" should exist in workspace'))
def file_exists_in_workspace(
    filename: str, temp_workspace: Path, context: dict[str, Any]
) -> None:
    """Check file exists in workspace."""
    file_path = temp_workspace / filename
    assert file_path.exists(), f"File {filename} does not exist"
    assert file_path.is_file(), f"{filename} is not a file"


@then("the workspace info should contain the config")
def workspace_info_has_config(context: dict[str, Any]) -> None:
    """Check workspace info has config."""
    info: WorkspaceInfo = context["workspace_info"]
    assert info.config is not None


@then("the workspace info should have extensions_path")
def workspace_info_has_extensions_path(context: dict[str, Any]) -> None:
    """Check workspace info has extensions_path."""
    info: WorkspaceInfo = context["workspace_info"]
    assert info.extensions_path is not None


@then("the workspace info should have examples_path")
def workspace_info_has_examples_path(context: dict[str, Any]) -> None:
    """Check workspace info has examples_path."""
    info: WorkspaceInfo = context["workspace_info"]
    assert info.examples_path is not None


@then("the workspace info should have projects_path")
def workspace_info_has_projects_path(context: dict[str, Any]) -> None:
    """Check workspace info has projects_path."""
    info: WorkspaceInfo = context["workspace_info"]
    assert info.projects_path is not None


@then(parsers.parse('a ValueError should be raised with message containing "{text}"'))
def valueerror_raised_with_message(text: str, context: dict[str, Any]) -> None:
    """Check ValueError was raised with message."""
    exc = context.get("exception")
    assert exc is not None, "No exception was raised"
    assert isinstance(exc, ValueError), f"Expected ValueError, got {type(exc)}"
    assert text in str(exc), f"Expected '{text}' in error message: {exc}"


@pytest.fixture(autouse=True)
def restore_praxis_home(context: dict[str, Any]) -> None:
    """Restore PRAXIS_HOME after each test."""
    yield
    original = context.get("original_praxis_home")
    if original is not None:
        os.environ["PRAXIS_HOME"] = original
    elif "PRAXIS_HOME" in os.environ:
        del os.environ["PRAXIS_HOME"]
