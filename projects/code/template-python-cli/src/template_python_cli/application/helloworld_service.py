"""Helloworld use case - orchestrates the greeting."""

from template_python_cli.domain.greeting import create_greeting


def execute(name: str) -> str:
    """Execute the helloworld use case."""
    return create_greeting(name)
