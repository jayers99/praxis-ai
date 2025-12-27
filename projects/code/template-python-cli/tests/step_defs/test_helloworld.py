"""Step definitions for helloworld feature."""

from typing import Any

import pytest
from pytest_bdd import parsers, scenarios, then, when
from typer.testing import CliRunner

from template_python_cli.cli import app

scenarios("../features/helloworld.feature")

runner = CliRunner()


@pytest.fixture
def context() -> dict[str, Any]:
    """Shared context between steps."""
    return {}


@when("I run the helloworld command")
def run_helloworld_default(context: dict[str, Any]) -> None:
    """Run helloworld without arguments."""
    context["result"] = runner.invoke(app, ["helloworld"])


@when(parsers.parse('I run the helloworld command with name "{name}"'))
def run_helloworld_with_name(context: dict[str, Any], name: str) -> None:
    """Run helloworld with a name argument."""
    context["result"] = runner.invoke(app, ["helloworld", name])


@then(parsers.parse('I should see "{expected}"'))
def check_output(context: dict[str, Any], expected: str) -> None:
    """Verify the output contains expected text."""
    assert context["result"].exit_code == 0
    assert expected in context["result"].output
