"""Step definitions for extension management BDD tests."""

from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path
from typing import Any

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from praxis.application.extension_service import (
    add_example,
    add_extension,
    list_examples,
    list_extensions,
)
from praxis.domain.workspace import (
    ExampleAddResult,
    ExampleListResult,
    ExtensionAddResult,
    ExtensionListResult,
)

scenarios("../features/extensions.feature")


@pytest.fixture
def context() -> dict[str, Any]:
    """Shared context for step definitions."""
    return {}


@pytest.fixture
def temp_workspace(context: dict[str, Any]) -> Path:
    """Create a temporary workspace directory."""
    temp_dir = Path(tempfile.mkdtemp(prefix="praxis_ext_test_"))
    context["temp_workspace"] = temp_dir
    yield temp_dir
    # Cleanup
    if temp_dir.exists():
        shutil.rmtree(temp_dir)


@given("a valid workspace with praxis-ai at PRAXIS_HOME")
def valid_workspace_with_praxis_ai(
    temp_workspace: Path, context: dict[str, Any]
) -> None:
    """Create a valid workspace with praxis-ai directory and registries."""
    context["original_praxis_home"] = os.environ.get("PRAXIS_HOME")
    os.environ["PRAXIS_HOME"] = str(temp_workspace)
    context["praxis_home"] = temp_workspace

    # Create directories
    (temp_workspace / "extensions").mkdir(exist_ok=True)
    (temp_workspace / "examples").mkdir(exist_ok=True)
    (temp_workspace / "projects").mkdir(exist_ok=True)
    (temp_workspace / "praxis-ai").mkdir(exist_ok=True)

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

    # Create extensions.yaml registry
    extensions_content = """extensions:
  render-run:
    repo: https://github.com/jayers99/render-run.git
    domain: create
    description: Send prompts to AI image generation APIs

  template-python-cli:
    repo: https://github.com/jayers99/template-python-cli.git
    domain: code
    description: Scaffold new Python CLI projects
"""
    (temp_workspace / "praxis-ai" / "extensions.yaml").write_text(extensions_content)

    # Create examples.yaml registry
    examples_content = """examples:
  uat-praxis-code:
    repo: https://github.com/jayers99/uat-praxis-code.git
    domain: code
    description: Hello-world CLI project

  opinions-framework:
    repo: https://github.com/jayers99/opinions-framework.git
    domain: write
    description: Opinions framework research
"""
    (temp_workspace / "praxis-ai" / "examples.yaml").write_text(examples_content)


@when("I call list_extensions")
def call_list_extensions(temp_workspace: Path, context: dict[str, Any]) -> None:
    """Call list_extensions."""
    result = list_extensions(temp_workspace)
    context["extension_list_result"] = result


@when(parsers.parse('I call add_extension with name "{name}"'))
def call_add_extension(
    name: str, temp_workspace: Path, context: dict[str, Any]
) -> None:
    """Call add_extension with given name."""
    result = add_extension(temp_workspace, name)
    context["add_result"] = result


@when("I call list_examples")
def call_list_examples(temp_workspace: Path, context: dict[str, Any]) -> None:
    """Call list_examples."""
    result = list_examples(temp_workspace)
    context["example_list_result"] = result


@when(parsers.parse('I call add_example with name "{name}"'))
def call_add_example(name: str, temp_workspace: Path, context: dict[str, Any]) -> None:
    """Call add_example with given name."""
    result = add_example(temp_workspace, name)
    context["example_add_result"] = result


@then(parsers.parse('the extension list should contain "{name}"'))
def extension_list_contains(name: str, context: dict[str, Any]) -> None:
    """Check extension list contains name."""
    result: ExtensionListResult = context["extension_list_result"]
    names = [ext.name for ext in result.available]
    assert name in names, f"Extension '{name}' not found in {names}"


@then("the add result should be unsuccessful")
def add_result_unsuccessful(context: dict[str, Any]) -> None:
    """Check add result is unsuccessful."""
    result: ExtensionAddResult = context["add_result"]
    assert not result.success, "Expected add to fail but it succeeded"


@then(parsers.parse('the add result error should contain "{text}"'))
def add_result_error_contains(text: str, context: dict[str, Any]) -> None:
    """Check add result error contains text."""
    result: ExtensionAddResult = context["add_result"]
    assert result.error is not None, "Expected error message but got None"
    assert text in result.error.lower(), f"Expected '{text}' in error: {result.error}"


@then(parsers.parse('the example list should contain "{name}"'))
def example_list_contains(name: str, context: dict[str, Any]) -> None:
    """Check example list contains name."""
    result: ExampleListResult = context["example_list_result"]
    names = [ex.name for ex in result.available]
    assert name in names, f"Example '{name}' not found in {names}"


@then("the example add result should be unsuccessful")
def example_add_result_unsuccessful(context: dict[str, Any]) -> None:
    """Check example add result is unsuccessful."""
    result: ExampleAddResult = context["example_add_result"]
    assert not result.success, "Expected add to fail but it succeeded"


@then(parsers.parse('the example add result error should contain "{text}"'))
def example_add_result_error_contains(text: str, context: dict[str, Any]) -> None:
    """Check example add result error contains text."""
    result: ExampleAddResult = context["example_add_result"]
    assert result.error is not None, "Expected error message but got None"
    assert text in result.error.lower(), f"Expected '{text}' in error: {result.error}"


@pytest.fixture(autouse=True)
def restore_praxis_home(context: dict[str, Any]) -> None:
    """Restore PRAXIS_HOME after each test."""
    yield
    original = context.get("original_praxis_home")
    if original is not None:
        os.environ["PRAXIS_HOME"] = original
    elif "PRAXIS_HOME" in os.environ:
        del os.environ["PRAXIS_HOME"]
