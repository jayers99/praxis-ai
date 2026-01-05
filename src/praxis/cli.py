"""Praxis CLI - thin Typer layer delegating to application services."""

from __future__ import annotations

from pathlib import Path

import click
import typer

from praxis import __version__
from praxis.application.audit_service import audit_project
from praxis.application.context_service import get_context
from praxis.application.extension_service import (
    add_example,
    add_extension,
    list_examples,
    list_extensions,
    remove_extension,
    update_all_extensions,
)
from praxis.application.init_service import init_project
from praxis.application.next_steps_service import format_next_steps_human
from praxis.application.opinions_service import (
    format_json_output,
    format_list_output,
    format_prompt_output,
    get_opinions_tree,
    resolve_opinions,
)
from praxis.application.stage_service import transition_stage
from praxis.application.status_service import get_status
from praxis.application.validate_service import validate
from praxis.application.workspace_service import (
    get_praxis_home,
    get_workspace_info,
    init_workspace,
    require_praxis_home,
)
from praxis.domain.domains import Domain
from praxis.domain.models import AuditCheck, CoverageCheckResult, ToolCheckResult
from praxis.domain.privacy import PrivacyLevel
from praxis.domain.subtypes import SubtypeValidationError, validate_subtype_for_domain
from praxis.infrastructure.stage_templates.template_paths import validate_subtype
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
    rich_markup_mode=None,  # Disable Rich formatting boxes
)

# Sub-apps for command groups (inherit rich_markup_mode from parent)
workspace_app = typer.Typer(help="Workspace management commands.")
extensions_app = typer.Typer(help="Extension management commands.")
examples_app = typer.Typer(help="Example management commands.")
templates_app = typer.Typer(help="Template rendering commands.")
opinions_app = typer.Typer(help="Opinions resolution and export.")
guide_app = typer.Typer(help="In-terminal documentation guides.")
research_app = typer.Typer(help="Research session management commands.")
library_app = typer.Typer(help="Research library query and maintenance commands.")
domain_app = typer.Typer(help="Domain creation and management commands.")

app.add_typer(workspace_app, name="workspace")
app.add_typer(extensions_app, name="extensions")
app.add_typer(examples_app, name="examples")
app.add_typer(templates_app, name="templates")
app.add_typer(opinions_app, name="opinions")
app.add_typer(guide_app, name="guide")
app.add_typer(research_app, name="research")
app.add_typer(library_app, name="library")
app.add_typer(domain_app, name="domain")


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


@app.command(name="help")
def help_cmd(ctx: typer.Context) -> None:
    """Show this help message."""
    typer.echo(ctx.parent.get_help())


@app.command(name="doctor")
def doctor_cmd(
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON.",
    ),
) -> None:
    """Check Praxis installation and configuration.

    Verifies:
    - Python version (requires 3.10+)
    - PRAXIS_HOME environment variable
    - Workspace structure and configuration
    - CLI accessibility

    Exit codes:
    - 0: All checks passed
    - 1: Critical errors found (missing required components)
    - 2: Warnings found (optional components missing)
    """
    import json as json_module
    import os
    import sys

    checks = []
    has_errors = False
    has_warnings = False

    # Check Python version
    py_version = sys.version_info
    if py_version >= (3, 10):
        checks.append({
            "status": "pass",
            "check": "Python version",
            "value": f"{py_version.major}.{py_version.minor}.{py_version.micro}",
            "message": None,
        })
    else:
        checks.append({
            "status": "error",
            "check": "Python version",
            "value": f"{py_version.major}.{py_version.minor}.{py_version.micro}",
            "message": "Python 3.10+ required",
        })
        has_errors = True

    # Check PRAXIS_HOME
    praxis_home_env = os.environ.get("PRAXIS_HOME")
    if praxis_home_env:
        checks.append({
            "status": "pass",
            "check": "PRAXIS_HOME",
            "value": praxis_home_env,
            "message": None,
        })
    else:
        checks.append({
            "status": "warning",
            "check": "PRAXIS_HOME",
            "value": "not set",
            "message": "Workspace features disabled",
        })
        has_warnings = True

    # Check workspace structure
    workspace_path = get_praxis_home()
    if workspace_path and workspace_path.exists():
        workspace_config = workspace_path / "workspace-config.yaml"
        if workspace_config.exists():
            checks.append({
                "status": "pass",
                "check": "Workspace",
                "value": str(workspace_path),
                "message": "Configured",
            })

            # Check subdirectories
            expected_dirs = ["extensions", "examples", "projects"]
            for dirname in expected_dirs:
                dir_path = workspace_path / dirname
                if dir_path.exists():
                    checks.append({
                        "status": "pass",
                        "check": f"  {dirname}/",
                        "value": "exists",
                        "message": None,
                    })
                else:
                    checks.append({
                        "status": "warning",
                        "check": f"  {dirname}/",
                        "value": "missing",
                        "message": "Expected directory not found",
                    })
                    has_warnings = True
        else:
            checks.append({
                "status": "warning",
                "check": "Workspace",
                "value": str(workspace_path),
                "message": (
                    "Directory exists but not initialized "
                    "(run 'praxis workspace init')"
                ),
            })
            has_warnings = True
    elif praxis_home_env:
        checks.append({
            "status": "error",
            "check": "Workspace",
            "value": praxis_home_env,
            "message": "Directory not found",
        })
        has_errors = True

    # Check Praxis package version
    checks.append({
        "status": "pass",
        "check": "Praxis version",
        "value": __version__,
        "message": None,
    })

    # JSON output
    if json_output:
        output = {
            "success": not has_errors,
            "has_warnings": has_warnings,
            "checks": checks,
        }
        typer.echo(json_module.dumps(output, indent=2))
        if has_errors:
            raise typer.Exit(1)
        if has_warnings:
            raise typer.Exit(2)
        raise typer.Exit(0)

    # Human-readable output
    typer.echo("Praxis Health Check\n")

    for check in checks:
        if check["status"] == "pass":
            icon = "✓"
        elif check["status"] == "warning":
            icon = "⚠"
        else:  # error
            icon = "✗"

        check_name = check["check"]
        value = check["value"]
        message = check["message"]

        if message:
            typer.echo(f"  {icon} {check_name:25} {value} ({message})")
        else:
            typer.echo(f"  {icon} {check_name:25} {value}")

    # Summary and recommendations
    typer.echo("")
    if has_errors:
        typer.echo("✗ Critical errors found\n", err=True)
        typer.echo("Recommended fixes:", err=True)

        if py_version < (3, 10):
            typer.echo("  - Install Python 3.10 or higher", err=True)

        if praxis_home_env and workspace_path and not workspace_path.exists():
            typer.echo("  - Create workspace: praxis workspace init", err=True)

        raise typer.Exit(1)

    if has_warnings:
        typer.echo("⚠ Some optional components missing\n")
        typer.echo("Recommendations:")

        if not praxis_home_env:
            typer.echo("  - Set PRAXIS_HOME environment variable:")
            typer.echo('    export PRAXIS_HOME="$HOME/praxis-workspace"')
            typer.echo("  - Initialize workspace:")
            typer.echo("    praxis workspace init")

        if workspace_path and workspace_path.exists():
            workspace_config = workspace_path / "workspace-config.yaml"
            if not workspace_config.exists():
                typer.echo("  - Initialize workspace:")
                typer.echo("    praxis workspace init")

        raise typer.Exit(2)

    typer.echo("✓ All checks passed")
    raise typer.Exit(0)


@templates_app.command("render")
def templates_render_cmd(
    path: Path = typer.Argument(
        Path("."),
        help="Project directory.",
    ),
    domain: str | None = typer.Option(
        None,
        "--domain",
        "-d",
        help=(
            "Project domain (code, create, write, observe, learn). "
            "Defaults to praxis.yaml."
        ),
    ),
    subtype: str | None = typer.Option(
        None,
        "--subtype",
        help="Optional subtype (e.g., api-backend).",
    ),
    stages: list[str] = typer.Option(
        [],
        "--stage",
        help=(
            "Only render these stages (can be provided multiple times). "
            "Defaults to all stages."
        ),
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite existing files.",
    ),
    template_root: list[Path] = typer.Option(
        [],
        "--template-root",
        help="Additional template root to search (can be provided multiple times).",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-error output.",
    ),
) -> None:
    """Render lifecycle stage docs and domain artifacts into a project."""
    import os

    from praxis.application.templates import render_stage_templates
    from praxis.domain.domains import Domain
    from praxis.domain.stages import Stage
    from praxis.infrastructure.manifest_loader import discover_extension_manifests
    from praxis.infrastructure.workspace_config_repo import load_workspace_config
    from praxis.infrastructure.yaml_loader import load_praxis_config

    project_root = path.resolve()

    domain_value: str | None = domain
    subtype_value: str | None = subtype
    load_result = load_praxis_config(project_root)

    # Load domain and subtype from praxis.yaml if not provided
    if load_result.valid and load_result.config is not None:
        if domain_value is None:
            domain_value = load_result.config.domain.value
        if subtype_value is None:
            subtype_value = load_result.config.subtype

    if domain_value is None:
        typer.echo(
            "Error: --domain is required (or provide a valid praxis.yaml)",
            err=True,
        )
        raise typer.Exit(1)

    try:
        domain_enum = Domain(domain_value)
    except ValueError:
        valid_domains = ", ".join(d.value for d in Domain)
        typer.echo(
            f"Error: invalid domain '{domain_value}'. Valid: {valid_domains}",
            err=True,
        )
        raise typer.Exit(1)

    stage_enums: list[Stage] | None = None
    if stages:
        stage_enums = []
        for stage_str in stages:
            try:
                stage_enums.append(Stage(stage_str))
            except ValueError:
                valid_stages = ", ".join(s.value for s in Stage)
                typer.echo(
                    f"Error: invalid stage '{stage_str}'. Valid: {valid_stages}",
                    err=True,
                )
                raise typer.Exit(1)

    # Load extension manifests if workspace exists
    extension_manifests = None
    praxis_home = os.environ.get("PRAXIS_HOME")
    if praxis_home:
        workspace_path = Path(praxis_home)
        if workspace_path.exists():
            try:
                config = load_workspace_config(workspace_path)
                extensions_path = workspace_path / "extensions"
                if extensions_path.exists() and config.installed_extensions:
                    manifest_results = discover_extension_manifests(
                        extensions_path, config.installed_extensions
                    )
                    # Filter to successful manifests with template contributions
                    extension_manifests = []
                    for manifest_result in manifest_results:
                        if manifest_result.success and manifest_result.manifest:
                            ext_path = extensions_path / manifest_result.extension_name
                            extension_manifests.append(
                                (ext_path, manifest_result.manifest)
                            )
                            # Log warnings if any
                            if manifest_result.warning:
                                typer.echo(
                                    f"Warning: {manifest_result.warning}", err=True
                                )
            except Exception:
                # Silently ignore workspace loading errors
                pass

    result = render_stage_templates(
        project_root=project_root,
        domain=domain_enum,
        subtype=subtype_value,
        stages=stage_enums,
        force=force,
        extra_template_roots=template_root,
        extension_manifests=extension_manifests,
    )

    if json_output:
        typer.echo(result.model_dump_json(indent=2))
        raise typer.Exit(0 if result.success else 1)

    if quiet:
        raise typer.Exit(0 if result.success else 1)

    if result.success:
        typer.echo("✓ Templates rendered")
    else:
        typer.echo("✗ Templates rendered with errors", err=True)

    # Show detailed file-by-file status
    for rendered in result.rendered:
        if rendered.destination.is_relative_to(project_root):
            rel_path = rendered.destination.relative_to(project_root)
        else:
            rel_path = rendered.destination

        if rendered.status == "created":
            typer.echo(f"  Created {rel_path}")
        elif rendered.status == "skipped":
            typer.echo(f"  Skipping {rel_path} — file already exists")
        elif rendered.status == "overwritten":
            typer.echo(f"  Overwritten {rel_path}")
        elif rendered.status == "error" and rendered.error:
            typer.echo(f"  Error: {rendered.error}", err=True)

    for info_msg in result.info:
        typer.echo(f"ℹ {info_msg}")

    for err in result.errors:
        typer.echo(f"Error: {err}", err=True)

    raise typer.Exit(0 if result.success else 1)


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
    lifecycle_mode: str = typer.Option(
        "full",
        "--lifecycle-mode",
        "-m",
        help=(
            "Lifecycle mode: 'full' (all 9 stages) or 'fast' "
            "(simplified 4-stage track)."
        ),
    ),
    template: str | None = typer.Option(
        None,
        "--template",
        "-t",
        help="Project template (e.g., python-cli).",
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

    result = init_project(
        path,
        domain,
        privacy,
        environment,
        subtype=None,
        template=template,
        lifecycle_mode=lifecycle_mode,
        force=force,
    )

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


@app.command(name="new")
def new_cmd(
    name: str = typer.Argument(
        ...,
        help="Project name (directory will be created under the chosen location).",
    ),
    domain: str | None = typer.Option(
        None,
        "--domain",
        "-d",
        help="Project domain (code, create, write, observe, learn).",
    ),
    subtype: str | None = typer.Option(
        None,
        "--subtype",
        help="Optional subtype (e.g., cli, api, library).",
    ),
    privacy: str | None = typer.Option(
        None,
        "--privacy",
        "-p",
        help=(
            "Privacy level (public, public-trusted, personal, "
            "confidential, restricted)."
        ),
    ),
    environment: str | None = typer.Option(
        None,
        "--env",
        "-e",
        help="Environment (Home, Work). Defaults to workspace config when available.",
    ),
    lifecycle_mode: str = typer.Option(
        "full",
        "--lifecycle-mode",
        "-m",
        help=(
            "Lifecycle mode: 'full' (all 9 stages) or 'fast' "
            "(simplified 4-stage track)."
        ),
    ),
    path: Path | None = typer.Option(
        None,
        "--path",
        help=(
            "Parent directory where the project directory will be created. "
            "Defaults to $PRAXIS_HOME/projects/<domain> when available, "
            "otherwise current directory."
        ),
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help=(
            "Overwrite existing managed files (praxis.yaml, CLAUDE.md, "
            "docs/capture.md)."
        ),
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON (automation-friendly; no prompts).",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-error output (no prompts).",
    ),
) -> None:
    """Create a new project directory and initialize Praxis governance files."""
    import json

    if "/" in name or "\\" in name:
        typer.echo("✗ Project name must not contain path separators", err=True)
        raise typer.Exit(1)

    workspace_path = get_praxis_home()
    workspace_info = None
    if workspace_path is not None:
        try:
            workspace_info = get_workspace_info(workspace_path)
        except Exception:
            workspace_info = None

    # Interactive prompts if flags not provided (disabled in json/quiet mode)
    if json_output or quiet:
        if domain is None or privacy is None:
            error_msg = "--domain and --privacy required with --json or --quiet"
            if json_output:
                typer.echo(
                    json.dumps(
                        {
                            "success": False,
                            "errors": [error_msg],
                        },
                        indent=2,
                    )
                )
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

        if subtype is None:
            subtype_answer = typer.prompt(
                "Subtype (optional)",
                default="",
                show_default=False,
            )
            subtype = subtype_answer.strip() or None

        if privacy is None:
            privacy_default = (
                workspace_info.config.defaults.privacy.value
                if workspace_info is not None
                else "personal"
            )
            privacy_choices = [p.value for p in PrivacyLevel]
            privacy = typer.prompt(
                "Privacy level",
                default=privacy_default,
                show_choices=True,
                type=click.Choice(privacy_choices),
            )

        if environment is None:
            env_default = (
                workspace_info.config.defaults.environment
                if workspace_info is not None
                else "Home"
            )
            environment = typer.prompt(
                "Environment",
                default=env_default,
                show_choices=True,
                type=click.Choice(["Home", "Work"]),
            )

    assert domain is not None
    assert privacy is not None

    # Validate subtype format early (matches template validation rules)
    if subtype is not None:
        try:
            validate_subtype(subtype)
        except ValueError as e:
            error_msg = str(e)
            if json_output:
                typer.echo(
                    json.dumps(
                        {
                            "success": False,
                            "errors": [error_msg],
                        },
                        indent=2,
                    )
                )
            else:
                typer.echo(f"✗ {error_msg}", err=True)
            raise typer.Exit(1)

        # Also validate subtype is valid for this domain
        try:
            domain_enum = Domain(domain)
            validate_subtype_for_domain(subtype, domain_enum)
        except SubtypeValidationError as e:
            error_msg = str(e)
            if json_output:
                typer.echo(
                    json.dumps(
                        {
                            "success": False,
                            "errors": [error_msg],
                        },
                        indent=2,
                    )
                )
            else:
                typer.echo(f"✗ {error_msg}", err=True)
            raise typer.Exit(1)

    # Apply workspace defaults in automation mode (if not provided)
    if environment is None:
        environment = (
            workspace_info.config.defaults.environment
            if workspace_info is not None
            else "Home"
        )

    # Resolve parent directory
    if path is not None:
        parent_dir = path.expanduser()
    else:
        if workspace_info is not None:
            default_parent = workspace_info.projects_path / domain
        elif workspace_path is not None:
            default_parent = workspace_path / "projects" / domain
        elif json_output or quiet:
            # Keep exit code 3 consistent with workspace-related commands
            error_msg = "PRAXIS_HOME not set and --path not provided"
            if json_output:
                typer.echo(
                    json.dumps(
                        {
                            "success": False,
                            "errors": [error_msg],
                        },
                        indent=2,
                    )
                )
            else:
                typer.echo(f"✗ {error_msg}", err=True)
            raise typer.Exit(3)
        else:
            default_parent = Path(".")

        if json_output or quiet:
            # Automation modes must not prompt.
            parent_dir = default_parent
        else:
            # Interactive mode always confirms the destination to avoid surprising
            # users when workspace defaults are present.
            parent_str = typer.prompt(
                "Location (parent directory)",
                default=str(default_parent),
            )
            parent_dir = Path(parent_str).expanduser()

    project_root = (parent_dir / name).resolve()
    if project_root.exists() and not project_root.is_dir():
        typer.echo(f"✗ Target exists and is not a directory: {project_root}", err=True)
        raise typer.Exit(1)

    result = init_project(
        project_root,
        domain,
        privacy,
        environment,
        subtype=subtype,
        lifecycle_mode=lifecycle_mode,
        force=force,
    )

    if json_output:
        typer.echo(
            json.dumps(
                {
                    "success": result.success,
                    "project_root": str(project_root),
                    "options": {
                        "domain": domain,
                        "subtype": subtype,
                        "privacy_level": privacy,
                        "environment": environment,
                        "force": force,
                    },
                    "files_created": result.files_created,
                    "errors": result.errors,
                },
                indent=2,
            )
        )
        raise typer.Exit(0 if result.success else 1)

    if result.success:
        if not quiet:
            typer.echo("✓ Praxis project created")
            typer.echo(f"  Path: {project_root}")
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
    reason: str | None = typer.Option(
        None,
        "--reason",
        "-r",
        help="Rationale for non-standard regressions.",
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
    result = transition_stage(path, new_stage, reason=reason)

    # Handle warnings that need confirmation (auto-fail in json/quiet mode)
    if result.needs_confirmation:
        if json_output or quiet:
            # In automation mode, don't prompt - just fail
            if json_output:
                typer.echo(result.model_dump_json(indent=2))
            raise typer.Exit(1)

        # Display enhanced warning with impact details
        typer.echo(f"⚠ {result.warning_message}", err=True)

        if result.crossing_formalize:
            typer.echo(
                "  ⚠ This regression crosses the Formalize boundary",
                err=True,
            )
            if result.voided_contract_id:
                typer.echo(
                    f"  ⚠ This will void: {result.voided_contract_id}",
                    err=True,
                )

        if not typer.confirm("Continue anyway?"):
            typer.echo("Aborted.")
            raise typer.Exit(0)
        # Prompt for reason if not provided
        if reason is None:
            reason = typer.prompt("Reason for regression")
        # Re-run with force and reason
        result = transition_stage(path, new_stage, force=True, reason=reason)

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
        output["version"] = "1.0"
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
    if not quiet:
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
    if not quiet:
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
        if not quiet:
            failed_items = [t.tool for t in tool_failures]
            if has_coverage_failure:
                failed_items.append("coverage")
            msg = f"\u2717 Tool checks failed: {', '.join(failed_items)}"
            typer.echo(msg, err=True)
        raise typer.Exit(1)

    if result.valid and has_warnings:
        if strict:
            if not quiet:
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
    if not quiet:
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
    """Show project status including stage, validation, and next steps.

    Displays 1-3 actionable next steps based on domain and stage.

    Step Types:
      + create  ~ edit  ▶ run  ? review  ! fix
    """
    status = get_status(path)

    if json_output:
        typer.echo(status.model_dump_json(indent=2))
        raise typer.Exit(0 if status.config else 1)

    # Handle config load errors
    if status.config is None:
        typer.echo(f"Project: {status.project_name}", err=True)
        for err in status.errors:
            typer.echo(f"\u2717 {err}", err=True)
        # Still show next steps for fixing errors
        if status.next_steps:
            typer.echo("")
            typer.echo(format_next_steps_human(status.next_steps))
        raise typer.Exit(1)

    if quiet:
        raise typer.Exit(0)

    config = status.config

    # Current state
    typer.echo(f"Project: {status.project_name}")
    if config.slug:
        typer.echo(f"  Slug:    {config.slug}")
    if config.description:
        typer.echo(f"  Desc:    {config.description}")
    typer.echo(f"  Domain:  {config.domain.value}")
    stage_progress = f"{status.stage_index}/{status.stage_count}"
    typer.echo(f"  Stage:   {config.stage.value} ({stage_progress})")
    typer.echo(f"  Privacy: {config.privacy_level.value}")
    typer.echo(f"  Env:     {config.environment}")
    typer.echo(f"  Mode:    {config.lifecycle_mode}")
    if config.tags:
        tags_str = ", ".join(config.tags)
        typer.echo(f"  Tags:    {tags_str}")

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

    # Checklist references
    typer.echo("")
    if status.checklist_path:
        typer.echo(f"Checklist: {status.checklist_path}")
        # Check if addendum exists (framework repo root relative)
        if status.checklist_addendum_path:
            # Try to find the framework root (where core/ is)
            # We're in a user project, so we need to check if the addendum exists
            # in the praxis framework installation
            import importlib.util
            praxis_spec = importlib.util.find_spec("praxis")
            if praxis_spec and praxis_spec.origin:
                framework_root = Path(praxis_spec.origin).parent.parent.parent
                addendum_full = framework_root / status.checklist_addendum_path
                if addendum_full.exists():
                    typer.echo(f"           {status.checklist_addendum_path}")

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

    # Next steps guidance
    typer.echo("")
    typer.echo(format_next_steps_human(status.next_steps))

    # Stage history
    typer.echo("")
    if status.stage_history:
        typer.echo("Stage History:")
        for entry in status.stage_history[:5]:  # Show last 5
            # Format timestamp (just date part)
            if "T" in entry.timestamp:
                timestamp_date = entry.timestamp.split("T")[0]
            else:
                timestamp_date = entry.timestamp
            transition = f"{entry.from_stage} → {entry.to_stage}"
            line = f"  {timestamp_date} {transition:25}"
            if entry.contract_id:
                line += f" [{entry.contract_id}]"
            if entry.reason:
                line += f" ({entry.reason})"
            typer.echo(line)
    else:
        typer.echo("Stage History: (no history found)")

    raise typer.Exit(0)


@app.command(name="context")
def context_cmd(
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
    """Generate deterministic AI context bundle for the project.

    Produces a reproducible context bundle containing:
    - Project configuration (domain, stage, privacy, environment)
    - Resolved opinions for current domain and stage
    - Formalize artifact excerpt (if applicable)

    Use --json for machine-readable output with stable schema.
    """
    bundle = get_context(path.resolve())

    # Handle errors
    if bundle.errors:
        if json_output:
            typer.echo(bundle.model_dump_json(indent=2))
        else:
            for error in bundle.errors:
                typer.echo(f"✗ {error}", err=True)
        raise typer.Exit(1)

    # JSON output
    if json_output:
        typer.echo(bundle.model_dump_json(indent=2))
        raise typer.Exit(0)

    # Quiet mode
    if quiet:
        raise typer.Exit(0)

    # Human-readable output
    typer.echo(f"Project: {bundle.project_name}")
    typer.echo(f"  Domain:  {bundle.domain}")
    typer.echo(f"  Stage:   {bundle.stage}")
    typer.echo(f"  Privacy: {bundle.privacy_level}")
    typer.echo(f"  Env:     {bundle.environment}")
    if bundle.subtype:
        typer.echo(f"  Subtype: {bundle.subtype}")

    typer.echo("")
    typer.echo("Opinions:")
    if bundle.opinions:
        for opinion_path in bundle.opinions:
            typer.echo(f"  - {opinion_path}")
    else:
        typer.echo("  (no opinions found)")

    typer.echo("")
    typer.echo("Formalize Artifact:")
    if bundle.formalize_artifact.get("path"):
        artifact_path = bundle.formalize_artifact["path"]
        typer.echo(f"  Path: {artifact_path}")
        if bundle.formalize_artifact.get("excerpt"):
            typer.echo("  Excerpt: (first 100 lines)")
        else:
            typer.echo("  Status: not found")
    else:
        typer.echo("  (none required for this stage)")

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
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-error output.",
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

    if quiet:
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


# ============================================================================
# Pipeline Commands
# ============================================================================

pipeline_app = typer.Typer(help="Knowledge distillation pipeline commands.")
app.add_typer(pipeline_app, name="pipeline")


@pipeline_app.command("init")
def pipeline_init_cmd(
    path: Path = typer.Argument(
        Path("."),
        help="Project directory.",
    ),
    tier: int = typer.Option(
        2,
        "--tier",
        "-t",
        help="Risk tier (0-3). Higher tiers require more stages.",
    ),
    corpus: Path = typer.Option(
        ...,
        "--corpus",
        "-c",
        help="Path to source corpus for RTC stage.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Replace existing active pipeline.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON.",
    ),
) -> None:
    """Initialize a new knowledge distillation pipeline."""
    from praxis.application.pipeline import init_pipeline

    result = init_pipeline(
        project_root=path.resolve(),
        risk_tier=tier,
        source_corpus_path=corpus.resolve(),
        force=force,
    )

    if json_output:
        typer.echo(result.model_dump_json(indent=2))
    else:
        if result.success:
            typer.echo(f"Pipeline initialized: {result.pipeline_id}")
            typer.echo(f"Risk tier: {result.risk_tier.value}")
            stages = ", ".join(s.value for s in result.required_stages)
            typer.echo(f"Required stages: {stages}")
        else:
            for error in result.errors:
                typer.echo(f"Error: {error}", err=True)
            raise typer.Exit(1)


@pipeline_app.command("status")
def pipeline_status_cmd(
    path: Path = typer.Argument(
        Path("."),
        help="Project directory.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-error output.",
    ),
) -> None:
    """Show current pipeline status and progress."""
    from praxis.application.pipeline import get_pipeline_status

    status = get_pipeline_status(path.resolve())

    if json_output:
        typer.echo(status.model_dump_json(indent=2))
        raise typer.Exit(0 if not status.errors else 1)

    if status.errors:
        for error in status.errors:
            typer.echo(f"Error: {error}", err=True)
        raise typer.Exit(1)

    if quiet:
        raise typer.Exit(0)

    typer.echo(f"Pipeline: {status.pipeline_id}")
    typer.echo(f"Risk tier: {status.risk_tier.value}")
    typer.echo(f"Current stage: {status.current_stage.value}")
    typer.echo("")
    typer.echo("Stage Progress:")
    for progress in status.stage_progress:
        marker = "✓" if progress.status == "completed" else "○"
        req = "(required)" if progress.required else "(optional)"
        typer.echo(f"  {marker} {progress.stage.value}: {progress.status} {req}")

    if status.next_stage:
        typer.echo(f"\nNext: {status.next_stage.value}")
    elif status.is_complete:
        typer.echo("\n✓ Pipeline complete")
    elif status.awaiting_hva:
        typer.echo("\n⏳ Awaiting HVA decision")


@pipeline_app.command("run")
def pipeline_run_cmd(
    path: Path = typer.Argument(
        Path("."),
        help="Project directory.",
    ),
    stage: str = typer.Option(
        None,
        "--stage",
        "-s",
        help="Specific stage to run (rtc, idas, sad, ccr, asr).",
    ),
    all_stages: bool = typer.Option(
        False,
        "--all",
        "-a",
        help="Run all remaining stages.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON.",
    ),
) -> None:
    """Execute pipeline stage(s)."""
    from praxis.application.pipeline import (
        execute_asr,
        execute_ccr,
        execute_idas,
        execute_rtc,
        execute_sad,
        get_pipeline_status,
    )

    executors = {
        "rtc": execute_rtc,
        "idas": execute_idas,
        "sad": execute_sad,
        "ccr": execute_ccr,
        "asr": execute_asr,
    }

    project_root = path.resolve()

    if stage:
        if stage not in executors:
            typer.echo(f"Invalid stage: {stage}", err=True)
            raise typer.Exit(1)

        result = executors[stage](project_root)

        if json_output:
            typer.echo(result.model_dump_json(indent=2))
        else:
            if result.success:
                typer.echo(f"✓ {stage.upper()} completed")
                if result.output_path:
                    typer.echo(f"  Output: {result.output_path}")
                for warning in result.warnings:
                    typer.echo(f"  ⚠ {warning}")
            else:
                for error in result.errors:
                    typer.echo(f"Error: {error}", err=True)
                raise typer.Exit(1)

    elif all_stages:
        status = get_pipeline_status(project_root)
        if status.errors:
            for error in status.errors:
                typer.echo(f"Error: {error}", err=True)
            raise typer.Exit(1)

        # Run stages in order until HVA
        stage_order = ["rtc", "idas", "sad", "ccr", "asr"]
        for stage_name in stage_order:
            # Check if stage is required and not completed
            progress = next(
                (p for p in status.stage_progress if p.stage.value == stage_name),
                None,
            )
            if progress and progress.required and progress.status != "completed":
                typer.echo(f"Running {stage_name.upper()}...")
                result = executors[stage_name](project_root)
                if not result.success:
                    for error in result.errors:
                        typer.echo(f"Error: {error}", err=True)
                    raise typer.Exit(1)
                typer.echo(f"✓ {stage_name.upper()} completed")

        typer.echo("\n✓ All stages completed. Ready for HVA decision.")

    else:
        typer.echo("Specify --stage or --all", err=True)
        raise typer.Exit(1)


@pipeline_app.command("accept")
def pipeline_accept_cmd(
    path: Path = typer.Argument(
        Path("."),
        help="Project directory.",
    ),
    rationale: str = typer.Option(
        ...,
        "--rationale",
        "-r",
        help="Rationale for accepting the pipeline.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON.",
    ),
) -> None:
    """Accept pipeline output (HVA stage)."""
    from praxis.application.pipeline import execute_hva

    result = execute_hva(path.resolve(), "accept", rationale)

    if json_output:
        typer.echo(result.model_dump_json(indent=2))
    else:
        if result.success:
            typer.echo("✓ Pipeline accepted")
            typer.echo("  Ready for research-library ingestion.")
        else:
            for error in result.errors:
                typer.echo(f"Error: {error}", err=True)
            raise typer.Exit(1)


@pipeline_app.command("reject")
def pipeline_reject_cmd(
    path: Path = typer.Argument(
        Path("."),
        help="Project directory.",
    ),
    rationale: str = typer.Option(
        ...,
        "--rationale",
        "-r",
        help="Rationale for rejecting the pipeline.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON.",
    ),
) -> None:
    """Reject pipeline output (HVA stage)."""
    from praxis.application.pipeline import execute_hva

    result = execute_hva(path.resolve(), "reject", rationale)

    if json_output:
        typer.echo(result.model_dump_json(indent=2))
    else:
        if result.success:
            typer.echo("✗ Pipeline rejected")
            typer.echo("  See rationale in HVA decision file.")
        else:
            for error in result.errors:
                typer.echo(f"Error: {error}", err=True)
            raise typer.Exit(1)


@pipeline_app.command("refine")
def pipeline_refine_cmd(
    path: Path = typer.Argument(
        Path("."),
        help="Project directory.",
    ),
    to_stage: str = typer.Option(
        ...,
        "--to",
        "-t",
        help="Stage to return to (rtc, idas, sad, ccr, asr).",
    ),
    rationale: str = typer.Option(
        ...,
        "--rationale",
        "-r",
        help="Rationale for requesting refinement.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON.",
    ),
) -> None:
    """Return pipeline to earlier stage for refinement (HVA stage)."""
    from praxis.application.pipeline import execute_hva

    result = execute_hva(path.resolve(), "refine", rationale, to_stage)

    if json_output:
        typer.echo(result.model_dump_json(indent=2))
    else:
        if result.success:
            typer.echo(f"↩ Pipeline returned to {to_stage}")
            typer.echo("  Address issues and re-run from that stage.")
        else:
            for error in result.errors:
                typer.echo(f"Error: {error}", err=True)
            raise typer.Exit(1)


# -----------------------------------------------------------------------------
# Opinions commands
# -----------------------------------------------------------------------------


@opinions_app.callback(invoke_without_command=True)
def opinions_cmd(
    ctx: typer.Context,
    path: Path = typer.Argument(
        Path("."),
        help="Project directory.",
    ),
    domain: str | None = typer.Option(
        None,
        "--domain",
        "-d",
        help="Domain (code, create, write, learn, observe). Overrides praxis.yaml.",
    ),
    stage: str | None = typer.Option(
        None,
        "--stage",
        "-s",
        help="Lifecycle stage. Overrides praxis.yaml.",
    ),
    subtype: str | None = typer.Option(
        None,
        "--subtype",
        "-t",
        help="Subtype (e.g., cli, library). Overrides praxis.yaml.",
    ),
    prompt: bool = typer.Option(
        False,
        "--prompt",
        "-p",
        help="Output as AI-ready prompt context.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON.",
    ),
    list_all: bool = typer.Option(
        False,
        "--list",
        "-l",
        help="List all available opinion files.",
    ),
    redact: bool = typer.Option(
        False,
        "--redact",
        help="Apply pattern-based redaction to sensitive content (defense-in-depth).",
    ),
) -> None:
    """Resolve and display applicable opinions for a project.

    By default, reads domain/stage/subtype from praxis.yaml in the project
    directory. Use --domain, --stage, --subtype to override or query without
    a praxis.yaml file.

    Examples:
        praxis opinions                    # Show resolved opinions
        praxis opinions --prompt           # AI-ready context
        praxis opinions --json             # Machine-readable
        praxis opinions --list             # All available files
        praxis opinions --domain code --stage capture
    """
    import json as json_module

    from praxis.infrastructure.yaml_loader import load_praxis_config

    # Handle --list separately (doesn't need domain/stage)
    if list_all:
        tree, warning = get_opinions_tree(start_path=path.resolve())
        if tree is None:
            typer.echo(f"Warning: {warning}", err=True)
            raise typer.Exit(0)
        typer.echo(format_list_output(tree))
        return

    # If subcommand was invoked, let it handle
    if ctx.invoked_subcommand is not None:
        return

    # Load from praxis.yaml if flags not provided
    resolved_domain = domain
    resolved_stage = stage
    resolved_subtype = subtype
    privacy_level: str | None = None

    if resolved_domain is None:
        # Try to load from praxis.yaml
        yaml_path = path.resolve() / "praxis.yaml"
        if yaml_path.exists():
            result = load_praxis_config(yaml_path)
            if result.valid and result.config:
                resolved_domain = result.config.domain.value
                resolved_stage = resolved_stage or result.config.stage.value
                resolved_subtype = resolved_subtype or result.config.subtype
                privacy_level = result.config.privacy_level.value
        else:
            typer.echo(
                "Error: No praxis.yaml found and --domain not specified.",
                err=True,
            )
            raise typer.Exit(1)

    if resolved_domain is None:
        typer.echo(
            "Error: Could not determine domain. Use --domain or create praxis.yaml.",
            err=True,
        )
        raise typer.Exit(1)

    # Resolve opinions
    resolved = resolve_opinions(
        domain=resolved_domain,
        stage=resolved_stage,
        subtype=resolved_subtype,
        start_path=path.resolve(),
    )

    # Output warnings
    for warning in resolved.warnings:
        typer.echo(f"Warning: {warning}", err=True)

    # Privacy warnings (only for --prompt)
    if prompt and privacy_level:
        from praxis.domain.privacy import PrivacyLevel
        from praxis.domain.privacy_guard import PrivacyGuard

        try:
            privacy_enum = PrivacyLevel(privacy_level)
            if PrivacyGuard.should_warn(privacy_enum):
                constraint = PrivacyGuard.get_constraint(privacy_enum)
                if constraint.warning_text:
                    typer.echo(constraint.warning_text, err=True)
        except (ValueError, KeyError):
            pass  # Invalid privacy level, skip warning

    # Format output
    if json_output:
        typer.echo(json_module.dumps(format_json_output(resolved), indent=2))
    elif prompt:
        output, redaction_warnings = format_prompt_output(
            resolved, privacy_level=privacy_level, redact=redact
        )
        if redaction_warnings:
            patterns_str = ", ".join(set(redaction_warnings))
            typer.echo(
                f"ℹ️  Redaction applied: {patterns_str}",
                err=True,
            )
        typer.echo(output)
    else:
        # Default: show provenance list
        typer.echo(f"Applicable opinions for {resolved.domain}", nl=False)
        if resolved.stage:
            typer.echo(f" × {resolved.stage}", nl=False)
        if resolved.subtype:
            typer.echo(f" ({resolved.subtype})", nl=False)
        typer.echo(":")
        typer.echo()

        if not resolved.existing_files:
            typer.echo("  (no opinion files found)")
        else:
            for i, f in enumerate(resolved.existing_files, 1):
                status = ""
                if f.frontmatter:
                    status = f" [{f.frontmatter.status.value}]"
                typer.echo(f"  {i}. {f.path}{status}")

        typer.echo()
        typer.echo(f"Total: {len(resolved.existing_files)} files")


@guide_app.command("lifecycle")
def guide_lifecycle_cmd() -> None:
    """Show lifecycle stages and Formalize hinge concept."""
    from praxis.application.guide_service import get_lifecycle_guide

    try:
        guide_text = get_lifecycle_guide()
        typer.echo(guide_text)
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@guide_app.command("privacy")
def guide_privacy_cmd() -> None:
    """Show privacy levels and behavioral constraints."""
    from praxis.application.guide_service import get_privacy_guide

    try:
        guide_text = get_privacy_guide()
        typer.echo(guide_text)
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


@guide_app.command("domain")
def guide_domain_cmd(
    domain: str = typer.Argument(
        ..., help="Domain name (code, create, write, learn, observe)"
    ),
) -> None:
    """Show domain-specific guidance and artifacts."""
    from praxis.application.guide_service import get_domain_guide

    try:
        guide_text = get_domain_guide(domain)
        typer.echo(guide_text)
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)
    except ValueError as e:
        typer.echo(f"Error: {e}", err=True)
        # List valid domains
        valid_domains = ["code", "create", "write", "learn", "observe"]
        typer.echo(f"\nValid domains: {', '.join(valid_domains)}", err=True)
        raise typer.Exit(1)


# =============================================================================
# Research Commands
# =============================================================================


@research_app.command("init")
def research_init_cmd(
    topic: str = typer.Option(
        ...,
        "--topic",
        "-t",
        help="Research topic to investigate.",
    ),
    corpus: Path = typer.Option(
        ...,
        "--corpus",
        "-c",
        help="Path to source corpus for RTC phase.",
    ),
    tier: int = typer.Option(
        2,
        "--tier",
        help="Risk tier (0-3). Higher tiers have stricter requirements.",
    ),
    path: Path = typer.Argument(
        Path("."),
        help="Working directory for the research session.",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Replace existing active session.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-error output.",
    ),
) -> None:
    """Initialize a new research session."""
    import json

    from praxis.application.research_service import init_research

    result = init_research(
        working_dir=path.resolve(),
        topic=topic,
        corpus_path=corpus.resolve(),
        tier=tier,
        force=force,
    )

    if json_output:
        data = {
            "success": result.success,
            "session_id": result.session_id,
            "phase": result.phase,
            "errors": result.errors,
        }
        typer.echo(json.dumps(data, indent=2))
        raise typer.Exit(0 if result.success else 1)

    if result.success:
        if not quiet:
            typer.echo("✓ Research session initialized")
            typer.echo(f"  Session ID: {result.session_id}")
            typer.echo(f"  Phase: {result.phase}")
        raise typer.Exit(0)
    else:
        for err in result.errors:
            typer.echo(f"✗ {err}", err=True)
        raise typer.Exit(1)


@research_app.command("status")
def research_status_cmd(
    path: Path = typer.Argument(
        Path("."),
        help="Working directory containing session.yaml.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-error output.",
    ),
) -> None:
    """Show current research session status and progress."""
    import json

    from praxis.application.research_service import get_research_status

    result = get_research_status(path.resolve())

    if json_output:
        data = {
            "success": result.success,
            "session_id": result.session_id,
            "topic": result.topic,
            "phase": result.phase,
            "phase_index": result.phase_index,
            "phase_count": result.phase_count,
            "tier": result.tier,
            "status": result.status,
            "corpus_path": result.corpus_path,
            "created_at": result.created_at,
            "updated_at": result.updated_at,
            "phase_history": result.phase_history,
            "artifact_path": result.artifact_path,
            "errors": result.errors,
        }
        typer.echo(json.dumps(data, indent=2))
        raise typer.Exit(0 if result.success else 1)

    if not result.success:
        for err in result.errors:
            typer.echo(f"✗ {err}", err=True)
        raise typer.Exit(1)

    if quiet:
        raise typer.Exit(0)

    typer.echo(f"Session: {result.session_id}")
    typer.echo(f"  Topic:  {result.topic}")
    typer.echo(f"  Phase:  {result.phase} ({result.phase_index}/{result.phase_count})")
    typer.echo(f"  Tier:   {result.tier}")
    typer.echo(f"  Status: {result.status}")
    typer.echo(f"  Corpus: {result.corpus_path}")

    if result.artifact_path:
        typer.echo(f"  Artifact: {result.artifact_path}")

    typer.echo("")
    typer.echo("Phase History:")
    for entry in result.phase_history:
        timestamp = entry.get("timestamp", "")[:10]  # Just date part
        phase = entry.get("phase", "")
        typer.echo(f"  {timestamp} → {phase}")

    raise typer.Exit(0)


@research_app.command("run")
def research_run_cmd(
    path: Path = typer.Argument(
        Path("."),
        help="Working directory containing session.yaml.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-error output.",
    ),
) -> None:
    """Advance to the next research phase."""
    import json

    from praxis.application.research_service import run_research_phase

    result = run_research_phase(path.resolve())

    if json_output:
        data = {
            "success": result.success,
            "previous_phase": result.previous_phase,
            "current_phase": result.current_phase,
            "errors": result.errors,
            "warnings": result.warnings,
        }
        typer.echo(json.dumps(data, indent=2))
        raise typer.Exit(0 if result.success else 1)

    if result.success:
        if not quiet:
            typer.echo(
                f"✓ Advanced from {result.previous_phase} to {result.current_phase}"
            )
            for warning in result.warnings:
                typer.echo(f"  ℹ {warning}")
        raise typer.Exit(0)
    else:
        for err in result.errors:
            typer.echo(f"✗ {err}", err=True)
        raise typer.Exit(1)


@research_app.command("approve")
def research_approve_cmd(
    rationale: str = typer.Option(
        ...,
        "--rationale",
        "-r",
        help="Rationale for approving the research.",
    ),
    path: Path = typer.Argument(
        Path("."),
        help="Working directory containing session.yaml.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-error output.",
    ),
) -> None:
    """Approve completed research for cataloging."""
    import json

    from praxis.application.research_service import approve_research

    result = approve_research(path.resolve(), rationale)

    if json_output:
        data = {
            "success": result.success,
            "session_id": result.session_id,
            "artifact_path": result.artifact_path,
            "cataloged": result.cataloged,
            "errors": result.errors,
        }
        typer.echo(json.dumps(data, indent=2))
        raise typer.Exit(0 if result.success else 1)

    if result.success:
        if not quiet:
            typer.echo("✓ Research approved")
            typer.echo(f"  Session: {result.session_id}")
            if result.artifact_path:
                typer.echo(f"  Artifact: {result.artifact_path}")
            if result.cataloged:
                typer.echo("  Status: Cataloged to research library")
            else:
                typer.echo("  Status: Ready for cataloging")
        raise typer.Exit(0)
    else:
        for err in result.errors:
            typer.echo(f"✗ {err}", err=True)
        raise typer.Exit(1)


@research_app.command("reject")
def research_reject_cmd(
    rationale: str = typer.Option(
        ...,
        "--rationale",
        "-r",
        help="Rationale for rejecting the research.",
    ),
    path: Path = typer.Argument(
        Path("."),
        help="Working directory containing session.yaml.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-error output.",
    ),
) -> None:
    """Reject research session and archive as draft."""
    import json

    from praxis.application.research_service import reject_research

    result = reject_research(path.resolve(), rationale)

    if json_output:
        data = {
            "success": result.success,
            "session_id": result.session_id,
            "archived": result.archived,
            "errors": result.errors,
        }
        typer.echo(json.dumps(data, indent=2))
        raise typer.Exit(0 if result.success else 1)

    if result.success:
        if not quiet:
            typer.echo("✗ Research rejected")
            typer.echo(f"  Session: {result.session_id}")
            if result.archived:
                typer.echo("  Status: Archived as draft")
        raise typer.Exit(0)
    else:
        for err in result.errors:
            typer.echo(f"✗ {err}", err=True)
        raise typer.Exit(1)


# =============================================================================
# Library Commands
# =============================================================================


@library_app.command("query")
def library_query_cmd(
    question: str = typer.Argument(
        ...,
        help="Natural language question to answer from the library.",
    ),
    library_path: Path | None = typer.Option(
        None,
        "--library-path",
        "-l",
        help="Path to research library (defaults to auto-detected).",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-error output.",
    ),
) -> None:
    """Query the research library with a natural language question."""
    import json

    from praxis.application.library_service import query_library_service

    result = query_library_service(question, library_path)

    if json_output:
        data = {
            "success": result.success,
            "query": result.query,
            "coverage_level": result.coverage_level,
            "coverage_reasoning": result.coverage_reasoning,
            "match_count": result.match_count,
            "summary": result.summary,
            "sources": result.sources,
            "gaps": result.gaps,
            "errors": result.errors,
        }
        typer.echo(json.dumps(data, indent=2))
        raise typer.Exit(0 if result.success else 1)

    if not result.success:
        for err in result.errors:
            typer.echo(f"✗ {err}", err=True)
        raise typer.Exit(1)

    if quiet:
        raise typer.Exit(0)

    typer.echo(f"Query: {result.query}")
    typer.echo("")
    typer.echo(f"Coverage: {result.coverage_level} ({result.match_count} matches)")
    typer.echo(f"  {result.coverage_reasoning}")
    typer.echo("")

    if result.sources:
        typer.echo("Sources:")
        for source in result.sources:
            typer.echo(f"  • [{source['title']}]({source['path']})")
            typer.echo(f"    Consensus: {source['consensus']}, Date: {source['date']}")

    if result.gaps:
        typer.echo("")
        typer.echo("Gaps (topics with limited coverage):")
        for gap in result.gaps:
            typer.echo(f"  • {gap}")

    raise typer.Exit(0)


@library_app.command("search")
def library_search_cmd(
    keyword: str = typer.Option(
        ...,
        "--keyword",
        "-k",
        help="Keyword to search for.",
    ),
    topic: str | None = typer.Option(
        None,
        "--topic",
        "-t",
        help="Optional topic to filter results.",
    ),
    library_path: Path | None = typer.Option(
        None,
        "--library-path",
        "-l",
        help="Path to research library (defaults to auto-detected).",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-error output.",
    ),
) -> None:
    """Search the research library by keyword."""
    import json

    from praxis.application.library_service import search_library_service

    result = search_library_service(keyword, topic, library_path)

    if json_output:
        data = {
            "success": result.success,
            "keyword": result.keyword,
            "topic": result.topic,
            "matches": result.matches,
            "errors": result.errors,
        }
        typer.echo(json.dumps(data, indent=2))
        raise typer.Exit(0 if result.success else 1)

    if not result.success:
        for err in result.errors:
            typer.echo(f"✗ {err}", err=True)
        raise typer.Exit(1)

    if quiet:
        raise typer.Exit(0)

    typer.echo(f"Search: {result.keyword}")
    if result.topic:
        typer.echo(f"  Topic filter: {result.topic}")
    typer.echo("")

    if not result.matches:
        typer.echo("No matching artifacts found.")
        raise typer.Exit(0)

    typer.echo(f"Found {len(result.matches)} match(es):")
    for match in result.matches:
        score = match.get("relevance_score", 0)
        typer.echo(f"  • {match['id']} (relevance: {score:.2f})")
        typer.echo(f"    {match['title']}")
        typer.echo(f"    Topic: {match['topic']}, Consensus: {match['consensus']}")

    raise typer.Exit(0)


@library_app.command("cite")
def library_cite_cmd(
    artifact_id: str = typer.Argument(
        ...,
        help="Artifact ID to cite.",
    ),
    library_path: Path | None = typer.Option(
        None,
        "--library-path",
        "-l",
        help="Path to research library (defaults to auto-detected).",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-error output.",
    ),
) -> None:
    """Get a formatted citation for an artifact."""
    import json

    from praxis.application.library_service import cite_artifact

    result = cite_artifact(artifact_id, library_path)

    if json_output:
        data = {
            "success": result.success,
            "artifact_id": result.artifact_id,
            "citation": result.citation,
            "formatted": result.formatted,
            "errors": result.errors,
        }
        typer.echo(json.dumps(data, indent=2))
        raise typer.Exit(0 if result.success else 1)

    if not result.success:
        for err in result.errors:
            typer.echo(f"✗ {err}", err=True)
        raise typer.Exit(1)

    if quiet:
        raise typer.Exit(0)

    typer.echo(result.formatted)
    raise typer.Exit(0)


@library_app.command("check-orphans")
def library_check_orphans_cmd(
    library_path: Path | None = typer.Option(
        None,
        "--library-path",
        "-l",
        help="Path to research library (defaults to auto-detected).",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-error output.",
    ),
) -> None:
    """Check for orphaned artifacts not listed in CATALOG.md."""
    import json

    from praxis.application.library_service import check_orphans

    result = check_orphans(library_path)

    if json_output:
        data = {
            "success": result.success,
            "orphans": result.orphans,
            "count": result.count,
            "errors": result.errors,
        }
        typer.echo(json.dumps(data, indent=2))
        raise typer.Exit(0 if result.success else 1)

    if not result.success:
        for err in result.errors:
            typer.echo(f"✗ {err}", err=True)
        raise typer.Exit(1)

    if quiet:
        raise typer.Exit(0)

    if result.count == 0:
        typer.echo("✓ No orphaned artifacts found")
    else:
        typer.echo(f"Found {result.count} orphaned artifact(s):")
        for orphan in result.orphans:
            typer.echo(f"  • {orphan}")

    raise typer.Exit(0)


@library_app.command("check-stale")
def library_check_stale_cmd(
    days: int = typer.Option(
        180,
        "--days",
        "-d",
        help="Number of days before an artifact is considered stale.",
    ),
    library_path: Path | None = typer.Option(
        None,
        "--library-path",
        "-l",
        help="Path to research library (defaults to auto-detected).",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-error output.",
    ),
) -> None:
    """Check for stale artifacts older than threshold."""
    import json

    from praxis.application.library_service import check_stale

    result = check_stale(days, library_path)

    if json_output:
        data = {
            "success": result.success,
            "stale_artifacts": result.stale_artifacts,
            "count": result.count,
            "threshold_days": result.threshold_days,
            "errors": result.errors,
        }
        typer.echo(json.dumps(data, indent=2))
        raise typer.Exit(0 if result.success else 1)

    if not result.success:
        for err in result.errors:
            typer.echo(f"✗ {err}", err=True)
        raise typer.Exit(1)

    if quiet:
        raise typer.Exit(0)

    if result.count == 0:
        typer.echo(f"✓ No stale artifacts found (threshold: {days} days)")
    else:
        typer.echo(f"Found {result.count} stale artifact(s) (older than {days} days):")
        for artifact in result.stale_artifacts:
            typer.echo(f"  • {artifact['id']} ({artifact['date']})")
            typer.echo(f"    {artifact['title']}")

    raise typer.Exit(0)


@library_app.command("reindex")
def library_reindex_cmd(
    library_path: Path | None = typer.Option(
        None,
        "--library-path",
        "-l",
        help="Path to research library (defaults to auto-detected).",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-error output.",
    ),
) -> None:
    """Rebuild CATALOG.md from all artifacts in the library."""
    import json

    from praxis.application.library_service import reindex_library_service

    result = reindex_library_service(library_path)

    if json_output:
        data = {
            "success": result.success,
            "implemented": result.implemented,
            "errors": result.errors,
        }
        typer.echo(json.dumps(data, indent=2))
        raise typer.Exit(0 if result.success else 1)

    if not result.success:
        for err in result.errors:
            typer.echo(f"✗ {err}", err=True)
        raise typer.Exit(1)

    if quiet:
        raise typer.Exit(0)

    if result.implemented:
        typer.echo("✓ Library reindexed successfully")
    else:
        typer.echo("ℹ Reindex is not yet implemented")
        typer.echo("  Use incremental cataloging via 'praxis research approve'")

    raise typer.Exit(0)


# =============================================================================
# Domain Commands
# =============================================================================


@domain_app.command("create")
def domain_create_cmd(
    workspace: Path | None = typer.Option(
        None,
        "--workspace",
        "-w",
        help="Workspace path (defaults to PRAXIS_HOME).",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON.",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress non-error output.",
    ),
) -> None:
    """Create a new custom domain through guided Q&A.

    This command provides a guided journey to define a new domain:
    1. Select from predefined templates or create custom
    2. Configure domain characteristics and AI permissions
    3. Define subtypes and formalize artifacts
    4. Generate domain specification file

    The new domain becomes available for use in future projects.
    """
    import json

    from praxis.application.domain_creation_service import create_domain_guided

    # Domain creation requires interactive mode
    if json_output or quiet:
        typer.echo(
            json.dumps(
                {
                    "success": False,
                    "errors": ["Domain creation requires interactive mode"],
                },
                indent=2,
            )
            if json_output
            else "✗ Domain creation requires interactive mode",
            err=True,
        )
        raise typer.Exit(1)

    result = create_domain_guided(workspace_path=workspace, interactive=True)

    if result.success:
        typer.echo("✓ Domain created successfully")
        typer.echo(f"  Name: {result.domain_name}")
        typer.echo(f"  Specification: {result.spec_path}")
        for f in result.files_created:
            typer.echo(f"  Created: {f}")
        if result.warnings:
            for warning in result.warnings:
                typer.echo(f"  ⚠ {warning}")
        raise typer.Exit(0)
    else:
        for err in result.errors:
            typer.echo(f"✗ {err}", err=True)
        raise typer.Exit(1)


@domain_app.command("list")
def domain_list_cmd(
    workspace: Path | None = typer.Option(
        None,
        "--workspace",
        "-w",
        help="Workspace path (defaults to PRAXIS_HOME).",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON.",
    ),
    include_builtin: bool = typer.Option(
        True,
        "--include-builtin/--no-builtin",
        help="Include built-in domains in listing.",
    ),
) -> None:
    """List available domains (built-in and custom)."""
    import json

    from praxis.application.domain_creation_service import list_custom_domains
    from praxis.domain.domains import Domain

    custom_domains = list_custom_domains(workspace_path=workspace)

    if json_output:
        output = {
            "builtin": [d.value for d in Domain] if include_builtin else [],
            "custom": [
                {
                    "name": d.name,
                    "display_name": d.display_name,
                    "description": d.description,
                    "subtypes": d.subtypes,
                }
                for d in custom_domains
            ],
        }
        typer.echo(json.dumps(output, indent=2))
        raise typer.Exit(0)

    if include_builtin:
        typer.echo("Built-in Domains:")
        for domain in Domain:
            typer.echo(f"  • {domain.value}")
        typer.echo("")

    if custom_domains:
        typer.echo("Custom Domains:")
        for domain in custom_domains:
            typer.echo(f"  • {domain.name} - {domain.description}")
    else:
        typer.echo("Custom Domains: (none)")

    raise typer.Exit(0)


@domain_app.command("show")
def domain_show_cmd(
    name: str = typer.Argument(..., help="Domain name to show details for."),
    workspace: Path | None = typer.Option(
        None,
        "--workspace",
        "-w",
        help="Workspace path (defaults to PRAXIS_HOME).",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Output as JSON.",
    ),
) -> None:
    """Show details of a custom domain."""
    import json

    from praxis.application.domain_creation_service import load_domain_specification

    spec = load_domain_specification(name, workspace_path=workspace)

    if spec is None:
        error_msg = f"Domain '{name}' not found"
        if json_output:
            typer.echo(json.dumps({"success": False, "error": error_msg}, indent=2))
        else:
            typer.echo(f"✗ {error_msg}", err=True)
        raise typer.Exit(1)

    if json_output:
        typer.echo(spec.model_dump_json(indent=2, exclude_none=True))
        raise typer.Exit(0)

    typer.echo(f"Domain: {spec.display_name} ({spec.name})")
    typer.echo(f"  Description: {spec.description}")
    typer.echo(f"  Version: {spec.version}")
    if spec.author:
        typer.echo(f"  Author: {spec.author}")
    if spec.created_at:
        typer.echo(f"  Created: {spec.created_at}")

    typer.echo("")
    if spec.formalize_artifact_name:
        typer.echo(f"Formalize Artifact: {spec.formalize_artifact_name}")
        typer.echo(f"  Path: {spec.formalize_artifact_path}")
    else:
        typer.echo("Formalize Artifact: (none)")

    typer.echo("")
    typer.echo(f"Default Privacy: {spec.default_privacy}")

    typer.echo("")
    typer.echo("AI Permissions:")
    if spec.ai_permissions:
        for op, perm in spec.ai_permissions.items():
            typer.echo(f"  {op:12} → {perm}")
    else:
        typer.echo("  (using defaults)")

    typer.echo("")
    if spec.subtypes:
        typer.echo(f"Subtypes: {', '.join(spec.subtypes)}")
    else:
        typer.echo("Subtypes: (none)")

    raise typer.Exit(0)


if __name__ == "__main__":
    app()
