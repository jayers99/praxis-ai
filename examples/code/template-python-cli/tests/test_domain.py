"""Domain layer unit tests."""

from template_python_cli.domain.greeting import create_greeting


def test_create_greeting_default() -> None:
    """Test greeting creation with default name."""
    result = create_greeting("World")
    assert result == "Hello, World!"


def test_create_greeting_custom() -> None:
    """Test greeting creation with custom name."""
    result = create_greeting("Praxis")
    assert result == "Hello, Praxis!"
