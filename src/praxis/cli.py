"""Praxis CLI - thin Typer layer delegating to application services."""

from __future__ import annotations

from pathlib import Path

import click
import typer

from praxis import __version__
from praxis.application.audit_service import audit_project
from praxis.application.extension_service import (
    add_example,
    add_extension,
    list_examples,
    list_extensions,
    remove_extension,
    update_all_extensions,
)
from praxis.application.init_service import init_project
from praxis.application.stage_service import transition_stage
from praxis.application.status_service import get_status
from praxis.application.validate_service import validate
from praxis.application.workspace_service import (
    get_workspace_info,
    init_workspace,
    require_praxis_home,
)
from praxis.domain.domains import Domain
from praxis.domain.models import AuditCheck, CoverageCheckResult, ToolCheckResult
from praxis.domain.privacy import PrivacyLevel
from praxis.infrastructure.tool_runner import (
    run_coverage,
    run_mypy,
    run_pytest,
    run_ruff,
)

app = typer.Typer(
    name="praxis",
    help="Policy-driven AI workflow governance.",
    no_args_is_help=True,
    add_completion=False,
)

# Sub-apps for command groups
workspace_app = typer.Typer(help="Workspace management commands.")
extensions_app = typer.Typer(help="Extension management commands.")
examples_app = typer.Typer(help="Example management commands.")

app.add_typer(workspace_app, name="workspace")
app.add_typer(extensions_app, name="extensions")
app.add_typer(examples_app, name="examples")


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
    check_tests: bool = typer.Option(
        False,
        "--check-tests",
        help="Run pytest and fail if tests fail.",
    ),
    check_lint: bool = typer.Option(
        False,
        "--check-lint",
        help="Run ruff and fail if lint errors exist.",
    ),
    check_types: bool = typer.Option(
        False,
        "--check-types",
        help="Run mypy and fail if type errors exist.",
    ),
    check_all: bool = typer.Option(
        False,
        "--check-all",
        help="Run all checks (tests, lint, types, coverage if configured).",
    ),
    check_coverage: bool = typer.Option(
        False,
        "--check-coverage",
        help="Run coverage check (requires coverage_threshold in praxis.yaml).",
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

    # Resolve project root for tool checks
    project_root = path if path.is_dir() else path.parent

    # Run tool checks if requested
    tool_results: list[ToolCheckResult] = []
    run_tests = check_tests or check_all
    run_lint = check_lint or check_all
    run_types = check_types or check_all

    if run_tests:
        tr = run_pytest(project_root)
        tool_results.append(ToolCheckResult(
            tool=tr.tool, success=tr.success, output=tr.output, error=tr.error
        ))

    if run_lint:
        tr = run_ruff(project_root)
        tool_results.append(ToolCheckResult(
            tool=tr.tool, success=tr.success, output=tr.output, error=tr.error
        ))

    if run_types:
        tr = run_mypy(project_root)
        tool_results.append(ToolCheckResult(
            tool=tr.tool, success=tr.success, output=tr.output, error=tr.error
        ))

    # Run coverage check if requested and threshold is configured
    coverage_result: CoverageCheckResult | None = None
    should_check_coverage = check_coverage or check_all
    if should_check_coverage and result.config and result.config.coverage_threshold:
        cr = run_coverage(project_root, result.config.coverage_threshold)
        coverage_result = CoverageCheckResult(
            success=cr.success,
            coverage_percent=cr.coverage_percent,
            threshold=cr.threshold,
            error=cr.error,
        )
    elif check_coverage and (not result.config or not result.config.coverage_threshold):
        coverage_result = CoverageCheckResult(
            success=False,
            coverage_percent=None,
            threshold=0,
            error="coverage_threshold not set in praxis.yaml",
        )

    # Check if any tool checks failed
    tool_failures = [t for t in tool_results if not t.success]
    has_coverage_failure = coverage_result is not None and not coverage_result.success

    # Determine overall success
    has_errors = len(result.errors) > 0
    has_warnings = len(result.warnings) > 0
    has_tool_failures = len(tool_failures) > 0

    if json_output:
        # Build combined JSON output
        output = result.model_dump()
        output["tool_checks"] = [t.model_dump() for t in tool_results]
        if coverage_result:
            output["coverage_check"] = coverage_result.model_dump()
        import json

        typer.echo(json.dumps(output, indent=2))
        if has_errors or has_tool_failures or has_coverage_failure:
            raise typer.Exit(1)
        if strict and has_warnings:
            raise typer.Exit(1)
        raise typer.Exit(0)

    # Print validation issues (warnings and errors go to stderr)
    for issue in result.issues:
        icon = "\u2717" if issue.severity == "error" else "\u26a0"
        severity = issue.severity.upper()
        typer.echo(f"{icon} [{severity}] {issue.message}", err=True)

    # Print tool check results
    if (tool_results or coverage_result) and not quiet:
        typer.echo("")
        typer.echo("Tool Checks:")
        for tool_check in tool_results:
            icon = "\u2713" if tool_check.success else "\u2717"
            typer.echo(f"  {icon} {tool_check.tool}")
            if not tool_check.success and tool_check.error:
                # Show first line of error
                first_line = tool_check.error.strip().split("\n")[0]
                typer.echo(f"    {first_line}", err=True)

        # Print coverage result
        if coverage_result:
            icon = "\u2713" if coverage_result.success else "\u2717"
            if coverage_result.coverage_percent is not None:
                pct = coverage_result.coverage_percent
                threshold = coverage_result.threshold
                typer.echo(f"  {icon} coverage ({pct:.0f}% / {threshold}% threshold)")
            else:
                typer.echo(f"  {icon} coverage")
            if not coverage_result.success and coverage_result.error:
                typer.echo(f"    {coverage_result.error}", err=True)

    # Print summary
    typer.echo("")
    all_checks_pass = (
        result.valid
        and not has_warnings
        and not has_tool_failures
        and not has_coverage_failure
    )
    if all_checks_pass:
        if not quiet:
            typer.echo("\u2713 Validation passed")
        raise typer.Exit(0)

    if has_tool_failures or has_coverage_failure:
        failed_items = [t.tool for t in tool_failures]
        if has_coverage_failure:
            failed_items.append("coverage")
        typer.echo(f"\u2717 Tool checks failed: {', '.join(failed_items)}", err=True)
        raise typer.Exit(1)

    if result.valid and has_warnings:
        if strict:
            typer.echo(
                f"\u2717 Validation failed: {len(result.warnings)} warning(s)",
                err=True,
            )
            raise typer.Exit(1)
        if not quiet:
            typer.echo(
                f"\u2713 Validation passed ({len(result.warnings)} warning(s))"
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


# =============================================================================
# Workspace Commands
# =============================================================================


@workspace_app.command(name="init")
def workspace_init_cmd(
    path: Path | None = typer.Option(
        None,
        "--path",
        "-p",
        help="Workspace path (defaults to PRAXIS_HOME or prompts).",
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
    """Initialize a new Praxis workspace."""
    import os

    import questionary

    # Determine workspace path
    if path is None:
        praxis_home = os.environ.get("PRAXIS_HOME")
        if praxis_home:
            workspace_path = Path(praxis_home).expanduser()
        elif json_output or quiet:
            typer.echo(
                "Error: PRAXIS_HOME not set and --path not provided", err=True
            )
            raise typer.Exit(3)
        else:
            # Interactive prompt
            answer = questionary.path(
                "Where should the workspace be created?",
                default="~/praxis-workspace",
            ).ask()
            if answer is None:
                typer.echo("Aborted.")
                raise typer.Exit(0)
            workspace_path = Path(answer).expanduser()
    else:
        workspace_path = path.expanduser()

    result = init_workspace(workspace_path)

    if json_output:
        typer.echo(result.model_dump_json(indent=2))
        raise typer.Exit(0 if result.success else 1)

    if result.success:
        if not quiet:
            typer.echo(f"✓ Workspace initialized at {workspace_path}")
            for d in result.dirs_created:
                typer.echo(f"  Created: {d}/")
            for f in result.files_created:
                typer.echo(f"  Created: {f}")
            for w in result.warnings:
                typer.echo(f"  ⚠ {w}", err=True)
        raise typer.Exit(0)
    else:
        for err in result.errors:
            typer.echo(f"✗ {err}", err=True)
        raise typer.Exit(1)


@workspace_app.command(name="info")
def workspace_info_cmd(
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output JSON format.",
    ),
) -> None:
    """Show workspace information."""
    try:
        workspace_path = require_praxis_home()
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(3)

    try:
        info = get_workspace_info(workspace_path)
    except FileNotFoundError as e:
        typer.echo(f"✗ {e}", err=True)
        raise typer.Exit(1)

    if json_output:
        # Convert paths to strings for JSON
        data = {
            "path": str(info.path),
            "extensions_path": str(info.extensions_path),
            "examples_path": str(info.examples_path),
            "projects_path": str(info.projects_path),
            "praxis_ai_path": str(info.praxis_ai_path) if info.praxis_ai_path else None,
            "installed_extensions": info.config.installed_extensions,
            "installed_examples": info.config.installed_examples,
            "defaults": {
                "privacy": info.config.defaults.privacy.value,
                "environment": info.config.defaults.environment,
            },
        }
        import json

        typer.echo(json.dumps(data, indent=2))
        raise typer.Exit(0)

    typer.echo(f"Workspace: {info.path}")
    typer.echo(f"  Extensions: {info.extensions_path}")
    typer.echo(f"  Examples:   {info.examples_path}")
    typer.echo(f"  Projects:   {info.projects_path}")
    if info.praxis_ai_path:
        typer.echo(f"  Praxis AI:  {info.praxis_ai_path}")
    else:
        typer.echo("  Praxis AI:  (not found)")

    typer.echo("")
    typer.echo("Installed Extensions:")
    if info.config.installed_extensions:
        for ext in info.config.installed_extensions:
            typer.echo(f"  - {ext}")
    else:
        typer.echo("  (none)")

    typer.echo("")
    typer.echo("Installed Examples:")
    if info.config.installed_examples:
        for ex in info.config.installed_examples:
            typer.echo(f"  - {ex}")
    else:
        typer.echo("  (none)")

    raise typer.Exit(0)


# =============================================================================
# Extensions Commands
# =============================================================================


@extensions_app.command(name="list")
def extensions_list_cmd(
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output JSON format.",
    ),
) -> None:
    """List available and installed extensions."""
    try:
        workspace_path = require_praxis_home()
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(3)

    result = list_extensions(workspace_path)

    if json_output:
        data = {
            "available": [
                {
                    "name": ext.name,
                    "domain": ext.domain.value,
                    "description": ext.description,
                    "installed": ext.installed,
                }
                for ext in result.available
            ],
            "installed": result.installed,
        }
        import json

        typer.echo(json.dumps(data, indent=2))
        raise typer.Exit(0)

    typer.echo("Available Extensions:")
    if result.available:
        for ext in result.available:
            status = "[installed]" if ext.installed else ""
            typer.echo(f"  {ext.name:25} {status:12} {ext.description}")
    else:
        typer.echo("  (registry not found - is praxis-ai cloned?)")

    raise typer.Exit(0)


@extensions_app.command(name="add")
def extensions_add_cmd(
    names: list[str] = typer.Argument(
        None,
        help="Extension name(s) to add. If omitted, shows interactive picker.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output JSON format.",
    ),
) -> None:
    """Add extension(s) to the workspace."""
    import questionary

    try:
        workspace_path = require_praxis_home()
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(3)

    # If no names provided, show interactive picker
    if not names:
        if json_output:
            typer.echo("Error: extension name required with --json", err=True)
            raise typer.Exit(2)

        available = list_extensions(workspace_path)
        if not available.available:
            typer.echo("✗ No extensions available (registry not found)", err=True)
            raise typer.Exit(1)

        # Filter out already installed
        choices = [
            questionary.Choice(
                title=f"{ext.name} - {ext.description}",
                value=ext.name,
                disabled="already installed" if ext.installed else None,
            )
            for ext in available.available
        ]

        selected = questionary.checkbox(
            "Select extensions to install:",
            choices=choices,
        ).ask()

        if not selected:
            typer.echo("No extensions selected.")
            raise typer.Exit(0)

        names = selected

    # Add each extension
    results = []
    for name in names:
        result = add_extension(workspace_path, name)
        results.append(result)

        if not json_output:
            if result.success:
                typer.echo(f"✓ Installed {name}")
            else:
                typer.echo(f"✗ Failed to install {name}: {result.error}", err=True)

    if json_output:
        import json

        data = [
            {"name": r.name, "success": r.success, "error": r.error}
            for r in results
        ]
        typer.echo(json.dumps(data, indent=2))

    # Exit with error if any failed
    if any(not r.success for r in results):
        raise typer.Exit(4)
    raise typer.Exit(0)


@extensions_app.command(name="remove")
def extensions_remove_cmd(
    name: str = typer.Argument(..., help="Extension name to remove."),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output JSON format.",
    ),
) -> None:
    """Remove an extension from the workspace."""
    try:
        workspace_path = require_praxis_home()
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(3)

    result = remove_extension(workspace_path, name)

    if json_output:
        import json

        data = {"name": name, "success": result.success, "error": result.error}
        typer.echo(json.dumps(data, indent=2))
        raise typer.Exit(0 if result.success else 4)

    if result.success:
        typer.echo(f"✓ Removed {name}")
        raise typer.Exit(0)
    else:
        typer.echo(f"✗ Failed to remove {name}: {result.error}", err=True)
        raise typer.Exit(4)


@extensions_app.command(name="update")
def extensions_update_cmd(
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output JSON format.",
    ),
) -> None:
    """Update all installed extensions."""
    try:
        workspace_path = require_praxis_home()
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(3)

    results = update_all_extensions(workspace_path)

    if not results:
        if json_output:
            typer.echo("[]")
        else:
            typer.echo("No extensions installed.")
        raise typer.Exit(0)

    if json_output:
        import json

        data = [
            {"name": r.name, "success": r.success, "error": r.error}
            for r in results
        ]
        typer.echo(json.dumps(data, indent=2))
    else:
        for r in results:
            if r.success:
                typer.echo(f"✓ Updated {r.name}")
            else:
                typer.echo(f"✗ Failed to update {r.name}: {r.error}", err=True)

    if any(not r.success for r in results):
        raise typer.Exit(4)
    raise typer.Exit(0)


# =============================================================================
# Examples Commands
# =============================================================================


@examples_app.command(name="list")
def examples_list_cmd(
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output JSON format.",
    ),
) -> None:
    """List available and installed examples."""
    try:
        workspace_path = require_praxis_home()
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(3)

    result = list_examples(workspace_path)

    if json_output:
        data = {
            "available": [
                {
                    "name": ex.name,
                    "domain": ex.domain.value,
                    "description": ex.description,
                    "installed": ex.installed,
                }
                for ex in result.available
            ],
            "installed": result.installed,
        }
        import json

        typer.echo(json.dumps(data, indent=2))
        raise typer.Exit(0)

    typer.echo("Available Examples:")
    if result.available:
        for ex in result.available:
            status = "[installed]" if ex.installed else ""
            typer.echo(f"  {ex.name:25} {status:12} {ex.description}")
    else:
        typer.echo("  (registry not found - is praxis-ai cloned?)")

    raise typer.Exit(0)


@examples_app.command(name="add")
def examples_add_cmd(
    names: list[str] = typer.Argument(
        None,
        help="Example name(s) to add. If omitted, shows interactive picker.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output JSON format.",
    ),
) -> None:
    """Add example(s) to the workspace."""
    import questionary

    try:
        workspace_path = require_praxis_home()
    except ValueError as e:
        typer.echo(str(e), err=True)
        raise typer.Exit(3)

    # If no names provided, show interactive picker
    if not names:
        if json_output:
            typer.echo("Error: example name required with --json", err=True)
            raise typer.Exit(2)

        available = list_examples(workspace_path)
        if not available.available:
            typer.echo("✗ No examples available (registry not found)", err=True)
            raise typer.Exit(1)

        # Filter out already installed
        choices = [
            questionary.Choice(
                title=f"{ex.name} - {ex.description}",
                value=ex.name,
                disabled="already installed" if ex.installed else None,
            )
            for ex in available.available
        ]

        selected = questionary.checkbox(
            "Select examples to install:",
            choices=choices,
        ).ask()

        if not selected:
            typer.echo("No examples selected.")
            raise typer.Exit(0)

        names = selected

    # Add each example
    results = []
    for name in names:
        result = add_example(workspace_path, name)
        results.append(result)

        if not json_output:
            if result.success:
                typer.echo(f"✓ Installed {name}")
            else:
                typer.echo(f"✗ Failed to install {name}: {result.error}", err=True)

    if json_output:
        import json

        data = [
            {"name": r.name, "success": r.success, "error": r.error}
            for r in results
        ]
        typer.echo(json.dumps(data, indent=2))

    # Exit with error if any failed
    if any(not r.success for r in results):
        raise typer.Exit(4)
    raise typer.Exit(0)


if __name__ == "__main__":
    app()
