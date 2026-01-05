"""Step definitions for templates_init.feature."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pytest_bdd import given, parsers, scenarios, then, when
from typer.testing import CliRunner

from praxis.cli import app

scenarios("../features/templates_init.feature")


@given("an empty directory")
def empty_directory(tmp_path: Path, context: dict[str, Any]) -> None:
    """Use the pytest tmp_path as an empty project directory."""
    context["project_root"] = tmp_path


@when(parsers.parse('I run praxis init with domain "{domain}" and privacy "{privacy}"'))
def run_init_with_flags(
    cli_runner: CliRunner,
    context: dict[str, Any],
    domain: str,
    privacy: str,
) -> None:
    """Run praxis init with domain and privacy flags."""
    project_root = context["project_root"]
    result = cli_runner.invoke(
        app,
        ["init", str(project_root), "--domain", domain, "--privacy", privacy],
    )
    context["result"] = result


@when(
    parsers.parse(
        'I run praxis init with domain "{domain}", privacy "{privacy}", '
        'and template "{template}"'
    )
)
def run_init_with_template(
    cli_runner: CliRunner,
    context: dict[str, Any],
    domain: str,
    privacy: str,
    template: str,
) -> None:
    """Run praxis init with domain, privacy, and template flags."""
    project_root = context["project_root"]
    result = cli_runner.invoke(
        app,
        [
            "init",
            str(project_root),
            "--domain",
            domain,
            "--privacy",
            privacy,
            "--template",
            template,
        ],
    )
    context["result"] = result


@then(parsers.parse('praxis.yaml should exist with domain "{domain}"'))
def check_praxis_yaml_domain(context: dict[str, Any], domain: str) -> None:
    """Verify praxis.yaml exists with the expected domain."""
    project_root = context["project_root"]
    praxis_yaml = project_root / "praxis.yaml"
    assert praxis_yaml.exists(), "praxis.yaml should exist"
    content = yaml.safe_load(praxis_yaml.read_text())
    assert content["domain"] == domain, (
        f"Expected domain '{domain}', got '{content.get('domain')}'"
    )


@then("pyproject.toml should exist")
def check_pyproject_exists(context: dict[str, Any]) -> None:
    """Verify pyproject.toml exists."""
    project_root = context["project_root"]
    pyproject = project_root / "pyproject.toml"
    assert pyproject.exists(), "pyproject.toml should exist"


@then("pyproject.toml should not exist")
def check_pyproject_not_exists(context: dict[str, Any]) -> None:
    """Verify pyproject.toml does not exist."""
    project_root = context["project_root"]
    pyproject = project_root / "pyproject.toml"
    assert not pyproject.exists(), "pyproject.toml should not exist"


@then("the project should have hexagonal architecture structure")
def check_hexagonal_architecture(context: dict[str, Any]) -> None:
    """Verify project has hexagonal architecture directories."""
    project_root = context["project_root"]

    # Check for src/ directory with package
    src_dirs = list((project_root / "src").glob("*"))
    assert len(src_dirs) > 0, "src/ should contain a package directory"

    package_dir = src_dirs[0]
    assert (package_dir / "domain").is_dir(), "domain/ directory should exist"
    assert (package_dir / "application").is_dir(), "application/ directory should exist"
    assert (
        package_dir / "infrastructure"
    ).is_dir(), "infrastructure/ directory should exist"
    assert (package_dir / "cli.py").is_file(), "cli.py should exist"


@then("the project should have a sample hello command")
def check_hello_command(context: dict[str, Any]) -> None:
    """Verify project has a sample hello command."""
    project_root = context["project_root"]

    # Find package directory
    src_dirs = list((project_root / "src").glob("*"))
    package_dir = src_dirs[0]

    # Check cli.py contains hello command
    cli_py = package_dir / "cli.py"
    assert cli_py.is_file(), "cli.py should exist"
    cli_content = cli_py.read_text()
    assert "hello" in cli_content, "cli.py should contain hello command"

    # Check hello service exists
    hello_service = package_dir / "application" / "hello_service.py"
    assert hello_service.is_file(), "hello_service.py should exist"


@then("tests/features/hello.feature should exist")
def check_hello_feature(context: dict[str, Any]) -> None:
    """Verify hello.feature exists."""
    project_root = context["project_root"]
    hello_feature = project_root / "tests" / "features" / "hello.feature"
    assert hello_feature.exists(), "tests/features/hello.feature should exist"


@then("tests/step_defs/test_hello.py should exist")
def check_hello_steps(context: dict[str, Any]) -> None:
    """Verify test_hello.py step definitions exist."""
    project_root = context["project_root"]
    test_hello = project_root / "tests" / "step_defs" / "test_hello.py"
    assert test_hello.exists(), "tests/step_defs/test_hello.py should exist"


@then("tests/test_hello_service.py should exist")
def check_hello_service_test(context: dict[str, Any]) -> None:
    """Verify test_hello_service.py unit tests exist."""
    project_root = context["project_root"]
    test_hello_service = project_root / "tests" / "test_hello_service.py"
    assert test_hello_service.exists(), "tests/test_hello_service.py should exist"
