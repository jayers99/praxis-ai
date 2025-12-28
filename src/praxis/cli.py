"""Praxis CLI - thin Typer layer delegating to application services."""

from __future__ import annotations

from pathlib import Path

import click
import typer

from praxis import __version__
from praxis.application.audit_service import audit_project
from praxis.application.init_service import init_project
from praxis.application.stage_service import transition_stage
from praxis.application.status_service import get_status
from praxis.application.validate_service import validate
from praxis.domain.domains import Domain
from praxis.domain.models import AuditCheck
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
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output JSON format.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-error output.",
    ),
) -> None:
    """Initialize a new Praxis project."""
    # Interactive prompts if flags not provided (disabled in json/quiet mode)
    if json_output or quiet:
        if domain is None or privacy is None:
            error_msg = "--domain and --privacy required with --json or --quiet"
            if json_output:
                typer.echo('{"success": false, "errors": ["' + error_msg + '"]}')
            else:
                typer.echo(f"✗ {error_msg}", err=True)
            raise typer.Exit(1)
    else:
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

    if json_output:
        typer.echo(result.model_dump_json(indent=2))
        raise typer.Exit(0 if result.success else 1)

    if result.success:
        if not quiet:
            typer.echo("✓ Praxis project initialized")
            for f in result.files_created:
                typer.echo(f"  Created: {f}")
        raise typer.Exit(0)
    else:
        for err in result.errors:
            typer.echo(f"✗ {err}", err=True)
        raise typer.Exit(1)


@app.command(name="stage")
def stage_cmd(
    new_stage: str = typer.Argument(..., help="Target stage to transition to."),
    path: Path = typer.Argument(
        Path("."),
        help="Project directory.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output JSON format.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-error output.",
    ),
) -> None:
    """Transition project to a new lifecycle stage."""
    result = transition_stage(path, new_stage)

    # Handle warnings that need confirmation (auto-fail in json/quiet mode)
    if result.needs_confirmation:
        if json_output or quiet:
            # In automation mode, don't prompt - just fail
            if json_output:
                typer.echo(result.model_dump_json(indent=2))
            raise typer.Exit(1)
        typer.echo(f"⚠ {result.warning_message}", err=True)
        if not typer.confirm("Continue anyway?"):
            typer.echo("Aborted.")
            raise typer.Exit(0)
        # Re-run with force
        result = transition_stage(path, new_stage, force=True)

    if json_output:
        typer.echo(result.model_dump_json(indent=2))
        raise typer.Exit(0 if result.success else 1)

    # Print issues (warnings and errors go to stderr)
    for issue in result.issues:
        icon = "✗" if issue.severity == "error" else "⚠"
        typer.echo(f"{icon} {issue.message}", err=True)

    if result.success:
        if not quiet:
            typer.echo(f"✓ Stage updated to '{new_stage}'")
        raise typer.Exit(0)
    else:
        typer.echo("✗ Failed to update stage", err=True)
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
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output JSON format.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-error output.",
    ),
) -> None:
    """Validate a praxis.yaml configuration."""
    result = validate(path)

    if json_output:
        typer.echo(result.model_dump_json(indent=2))
        has_failures = len(result.errors) > 0
        has_warnings = len(result.warnings) > 0
        if has_failures or (strict and has_warnings):
            raise typer.Exit(1)
        raise typer.Exit(0)

    # Print issues (warnings and errors go to stderr)
    for issue in result.issues:
        icon = "\u2717" if issue.severity == "error" else "\u26a0"
        severity = issue.severity.upper()
        typer.echo(f"{icon} [{severity}] {issue.message}", err=True)

    # Print summary
    if result.valid and not result.warnings:
        if not quiet:
            typer.echo("\u2713 praxis.yaml is valid")
        raise typer.Exit(0)

    if result.valid and result.warnings:
        if strict:
            typer.echo(
                f"\u2717 Validation failed: {len(result.warnings)} warning(s)",
                err=True,
            )
            raise typer.Exit(1)
        if not quiet:
            typer.echo(
                f"\u2713 praxis.yaml is valid ({len(result.warnings)} warning(s))"
            )
        raise typer.Exit(0)

    # Has errors
    typer.echo(f"\u2717 Validation failed: {len(result.errors)} error(s)", err=True)
    raise typer.Exit(1)


@app.command(name="status")
def status_cmd(
    path: Path = typer.Argument(
        Path("."),
        help="Project directory.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output JSON format.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-error output.",
    ),
) -> None:
    """Show project status including stage, validation, and history."""
    status = get_status(path)

    if json_output:
        typer.echo(status.model_dump_json(indent=2))
        raise typer.Exit(0 if status.config else 1)

    # Handle config load errors
    if status.config is None:
        typer.echo(f"Project: {status.project_name}", err=True)
        for err in status.errors:
            typer.echo(f"\u2717 {err}", err=True)
        raise typer.Exit(1)

    if quiet:
        raise typer.Exit(0)

    config = status.config

    # Current state
    typer.echo(f"Project: {status.project_name}")
    typer.echo(f"  Domain:  {config.domain.value}")
    stage_progress = f"{status.stage_index}/{status.stage_count}"
    typer.echo(f"  Stage:   {config.stage.value} ({stage_progress})")
    typer.echo(f"  Privacy: {config.privacy_level.value}")
    typer.echo(f"  Env:     {config.environment}")

    # Next stage
    typer.echo("")
    if status.next_stage:
        typer.echo(f"Next Stage: {status.next_stage.value}")
        for req in status.next_stage_requirements:
            typer.echo(f"  - {req}")
    else:
        typer.echo("Next Stage: (none - at final stage)")

    # Artifact status
    typer.echo("")
    if status.artifact_path:
        icon = "\u2713" if status.artifact_exists else "\u2717"
        typer.echo(f"Artifact: {icon} {status.artifact_path}")
    else:
        typer.echo("Artifact: (none required for this domain)")

    # Validation
    typer.echo("")
    if status.validation.valid and not status.validation.warnings:
        typer.echo("Validation: \u2713 Valid")
    elif status.validation.valid and status.validation.warnings:
        warn_count = len(status.validation.warnings)
        typer.echo(f"Validation: \u2713 Valid ({warn_count} warning(s))")
        for issue in status.validation.warnings:
            typer.echo(f"  \u26a0 {issue.message}")
    else:
        err_count = len(status.validation.errors)
        typer.echo(f"Validation: \u2717 Invalid ({err_count} error(s))")
        for issue in status.validation.errors:
            typer.echo(f"  \u2717 {issue.message}", err=True)

    # Stage history
    typer.echo("")
    if status.stage_history:
        typer.echo("Stage History:")
        for entry in status.stage_history[:5]:  # Show last 5
            line = f"  {entry.commit_date} {entry.stage:10} {entry.commit_hash}"
            typer.echo(f"{line} {entry.commit_message}")
    else:
        typer.echo("Stage History: (no history found)")

    raise typer.Exit(0)


@app.command(name="audit")
def audit_cmd(
    path: Path = typer.Argument(
        Path("."),
        help="Project directory.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output JSON format.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-error output.",
    ),
    strict: bool = typer.Option(
        False,
        "--strict",
        "-s",
        help="Treat warnings as failures (exit 1).",
    ),
) -> None:
    """Check project against domain best practices."""
    result = audit_project(path)

    # Exit code determination
    has_failures = len(result.failed) > 0
    has_warnings = len(result.warnings) > 0
    exit_code = 1 if has_failures or (strict and has_warnings) else 0

    if json_output:
        typer.echo(result.model_dump_json(indent=2))
        raise typer.Exit(exit_code)

    if quiet:
        raise typer.Exit(exit_code)

    typer.echo(f"\nAuditing: {result.project_name} (domain: {result.domain})\n")

    # Group by category
    by_category: dict[str, list[AuditCheck]] = {}
    for check in result.checks:
        by_category.setdefault(check.category, []).append(check)

    icons = {"passed": "\u2713", "warning": "\u26a0", "failed": "\u2717"}
    for category, checks in by_category.items():
        typer.echo(f"{category.title()}:")
        for check in checks:
            typer.echo(f"  {icons[check.status]} {check.message}")
        typer.echo("")

    # Summary
    p, w, f = len(result.passed), len(result.warnings), len(result.failed)
    typer.echo(f"Summary: {p} passed, {w} warning(s), {f} failed")

    raise typer.Exit(exit_code)


if __name__ == "__main__":
    app()
