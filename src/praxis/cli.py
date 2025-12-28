"""Praxis CLI - thin Typer layer delegating to application services."""

from __future__ import annotations

from pathlib import Path

import click
import typer

from praxis import __version__
from praxis.application.init_service import init_project
from praxis.application.validate_service import validate
from praxis.domain.domains import Domain
from praxis.domain.privacy import PrivacyLevel

app = typer.Typer(
    name="praxis",
    help="Policy-driven AI workflow governance.",
    no_args_is_help=True,
    add_completion=False,
)


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        typer.echo(f"praxis {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
) -> None:
    """Praxis CLI - Policy-driven AI workflow governance."""


@app.command(name="init")
def init_cmd(
    path: Path = typer.Argument(
        Path("."),
        help="Project directory to initialize.",
    ),
    domain: str | None = typer.Option(
        None,
        "--domain",
        "-d",
        help="Project domain (code, create, write, observe, learn).",
    ),
    privacy: str | None = typer.Option(
        None,
        "--privacy",
        "-p",
        help="Privacy level (public, personal, confidential, restricted).",
    ),
    environment: str = typer.Option(
        "Home",
        "--env",
        "-e",
        help="Environment (Home, Work).",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite existing files.",
    ),
) -> None:
    """Initialize a new Praxis project."""
    # Interactive prompts if flags not provided
    if domain is None:
        domain_choices = [d.value for d in Domain]
        domain = typer.prompt(
            "Domain",
            default="code",
            show_choices=True,
            type=click.Choice(domain_choices),
        )
    if privacy is None:
        privacy_choices = [p.value for p in PrivacyLevel]
        privacy = typer.prompt(
            "Privacy level",
            default="personal",
            show_choices=True,
            type=click.Choice(privacy_choices),
        )

    result = init_project(path, domain, privacy, environment, force)

    if result.success:
        typer.echo("✓ Praxis project initialized")
        for f in result.files_created:
            typer.echo(f"  Created: {f}")
        raise typer.Exit(0)
    else:
        for err in result.errors:
            typer.echo(f"✗ {err}")
        raise typer.Exit(1)


@app.command(name="validate")
def validate_cmd(
    path: Path = typer.Argument(
        Path("."),
        help="Path to project root or praxis.yaml file.",
        exists=True,
    ),
    strict: bool = typer.Option(
        False,
        "--strict",
        "-s",
        help="Treat warnings as errors (exit 1).",
    ),
) -> None:
    """Validate a praxis.yaml configuration."""
    result = validate(path)

    # Print issues
    for issue in result.issues:
        icon = "\u2717" if issue.severity == "error" else "\u26a0"
        severity = issue.severity.upper()
        typer.echo(f"{icon} [{severity}] {issue.message}")

    # Print summary
    if result.valid and not result.warnings:
        typer.echo("\u2713 praxis.yaml is valid")
        raise typer.Exit(0)

    if result.valid and result.warnings:
        if strict:
            typer.echo(f"\u2717 Validation failed: {len(result.warnings)} warning(s)")
            raise typer.Exit(1)
        typer.echo(
            f"\u2713 praxis.yaml is valid ({len(result.warnings)} warning(s))"
        )
        raise typer.Exit(0)

    # Has errors
    typer.echo(f"\u2717 Validation failed: {len(result.errors)} error(s)")
    raise typer.Exit(1)


if __name__ == "__main__":
    app()
