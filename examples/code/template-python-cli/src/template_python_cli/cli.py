"""Thin CLI layer - delegates to application services."""

import typer

from template_python_cli.application import helloworld_service

app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.callback()
def callback() -> None:
    """Template Python CLI - A reusable project template."""
    pass


@app.command()
def helloworld(name: str = typer.Argument(default="World")) -> None:
    """Greet someone with a friendly hello."""
    result = helloworld_service.execute(name=name)
    typer.echo(result)
