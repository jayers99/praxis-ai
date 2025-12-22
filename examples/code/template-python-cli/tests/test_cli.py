"""CLI integration tests."""

from typer.testing import CliRunner

from template_python_cli.cli import app

runner = CliRunner()


def test_help_shows_commands() -> None:
    """Test that --help shows available commands."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "helloworld" in result.output


def test_helloworld_default() -> None:
    """Test helloworld with default name."""
    result = runner.invoke(app, ["helloworld"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.output


def test_helloworld_custom_name() -> None:
    """Test helloworld with custom name."""
    result = runner.invoke(app, ["helloworld", "Praxis"])
    assert result.exit_code == 0
    assert "Hello, Praxis!" in result.output
