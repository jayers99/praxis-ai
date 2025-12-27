"""CLI integration tests."""

from typer.testing import CliRunner

from template_python_cli.cli import app


def test_help_shows_commands(cli_runner: CliRunner) -> None:
    """Test that --help shows available commands."""
    result = cli_runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "helloworld" in result.output


def test_helloworld_default(cli_runner: CliRunner) -> None:
    """Test helloworld with default name."""
    result = cli_runner.invoke(app, ["helloworld"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.output


def test_helloworld_custom_name(cli_runner: CliRunner) -> None:
    """Test helloworld with custom name."""
    result = cli_runner.invoke(app, ["helloworld", "Praxis"])
    assert result.exit_code == 0
    assert "Hello, Praxis!" in result.output
