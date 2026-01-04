"""Run audit checks against a project."""

from __future__ import annotations

import os
import re
from collections.abc import Callable
from pathlib import Path

from praxis.domain.audit_checks import CHECKS_BY_DOMAIN, CheckDefinition
from praxis.domain.domains import Domain
from praxis.domain.models import AuditCheck, AuditResult, PraxisConfig
from praxis.domain.stages import Stage
from praxis.domain.workspace import AuditCheckContribution
from praxis.infrastructure.audit_contribution_runners import (
    run_dir_exists_check,
    run_file_contains_check,
    run_file_exists_check,
)
from praxis.infrastructure.manifest_loader import discover_extension_manifests
from praxis.infrastructure.yaml_loader import load_praxis_config


def _check_applies(check: CheckDefinition, config: PraxisConfig) -> bool:
    """Determine if a check applies to the current project context.

    Args:
        check: The check definition to evaluate.
        config: The project's praxis configuration.

    Returns:
        True if the check should be run, False if it should be skipped.
    """
    # Check min_stage filter: skip check if current stage is before min_stage
    if check.min_stage is not None and config.stage < check.min_stage:
        return False

    # Check subtypes filter: skip check if project subtype not in allowed subtypes
    if check.subtypes is not None:
        # If project has no subtype, skip subtype-specific checks
        if config.subtype is None:
            return False
        # If project subtype not in the check's subtypes list, skip
        if config.subtype not in check.subtypes:
            return False

    return True


def _create_check_function(
    check_contrib: AuditCheckContribution,
) -> tuple[Callable[[Path], bool], list[str]]:
    """Create a check function from an audit check contribution.

    Args:
        check_contrib: The audit check contribution.

    Returns:
        Tuple of (check_function, warnings_list).
        If check type is unsupported or has errors, returns (lambda: False, [warning]).
    """
    warnings: list[str] = []
    check_type = check_contrib.check_type

    if check_type == "file_exists":
        return lambda p: run_file_exists_check(p, check_contrib.path), warnings

    elif check_type == "dir_exists":
        return lambda p: run_dir_exists_check(p, check_contrib.path), warnings

    elif check_type == "file_contains":
        if not check_contrib.pattern:
            warnings.append(
                f"Check '{check_contrib.name}': file_contains requires 'pattern' field"
            )
            return lambda p: False, warnings

        # Validate regex pattern
        try:
            re.compile(check_contrib.pattern)
        except re.error as e:
            warnings.append(
                f"Check '{check_contrib.name}': invalid regex pattern: {e}"
            )
            # Return a function that will fail gracefully
            return lambda p: False, warnings

        return (
            lambda p: run_file_contains_check(
                p, check_contrib.path, check_contrib.pattern or ""
            ),
            warnings,
        )

    else:
        warnings.append(
            f"Check '{check_contrib.name}': unsupported check_type '{check_type}'"
        )
        return lambda p: False, warnings


def register_extension_checks() -> list[str]:
    """Register extension-contributed audit checks.

    Discovers installed extensions and converts their audit contributions
    into CheckDefinition objects that are merged into CHECKS_BY_DOMAIN.

    Returns:
        List of warning messages from processing extensions.
    """
    warnings: list[str] = []

    # Get workspace extensions path from PRAXIS_HOME
    praxis_home = os.environ.get("PRAXIS_HOME")
    if not praxis_home:
        return warnings  # No workspace, no extensions

    workspace_path = Path(praxis_home)
    extensions_path = workspace_path / "extensions"

    if not extensions_path.exists():
        return warnings  # No extensions directory

    # Load workspace config to get installed extensions
    from praxis.infrastructure.workspace_config_repo import load_workspace_config

    try:
        workspace_config = load_workspace_config(workspace_path)
        # Sort extensions for deterministic check ordering
        installed_extensions = sorted(workspace_config.installed_extensions)
    except (FileNotFoundError, ValueError):
        return warnings  # No valid workspace config

    # Discover and load extension manifests
    manifest_results = discover_extension_manifests(
        extensions_path, installed_extensions
    )

    # Process each manifest and register audit checks
    for manifest_result in manifest_results:
        if not manifest_result.success or not manifest_result.manifest:
            if manifest_result.error:
                error_msg = manifest_result.error
                warnings.append(
                    f"Extension '{manifest_result.extension_name}': {error_msg}"
                )
            continue

        # Add manifest loading warnings
        if manifest_result.warning:
            warn_msg = manifest_result.warning
            warnings.append(
                f"Extension '{manifest_result.extension_name}': {warn_msg}"
            )

        manifest = manifest_result.manifest
        extension_name = manifest.name

        # Process audit contributions
        for audit_contrib in manifest.contributions.audits:
            # Parse domain
            try:
                domain = Domain(audit_contrib.domain)
            except ValueError:
                domain_name = audit_contrib.domain
                warnings.append(
                    f"Extension '{extension_name}': invalid domain '{domain_name}'"
                )
                continue

            # Process each check in this audit contribution
            for check_contrib in audit_contrib.checks:
                # Create check function
                check_fn, check_warnings = _create_check_function(check_contrib)
                if check_warnings:
                    for w in check_warnings:
                        warnings.append(f"Extension '{extension_name}': {w}")
                    continue  # Skip this check if there were errors

                # Parse min_stage if specified
                min_stage = None
                if check_contrib.min_stage:
                    try:
                        min_stage = Stage(check_contrib.min_stage)
                    except ValueError:
                        stage_name = check_contrib.min_stage
                        warnings.append(
                            f"Extension '{extension_name}': "
                            f"check '{check_contrib.name}': "
                            f"invalid min_stage '{stage_name}'"
                        )
                        continue

                # Parse subtypes (inherit from audit contribution)
                subtypes = (
                    audit_contrib.subtypes if audit_contrib.subtypes else None
                )

                # Create CheckDefinition with prefixed name for provenance
                check_def = CheckDefinition(
                    name=f"{extension_name}:{check_contrib.name}",
                    category=check_contrib.category,
                    check_fn=check_fn,
                    pass_message=check_contrib.pass_message,
                    fail_message=check_contrib.fail_message,
                    severity="warning"
                    if check_contrib.severity == "warning"
                    else "failed",
                    min_stage=min_stage,
                    subtypes=subtypes,
                )

                # Add to CHECKS_BY_DOMAIN
                if domain not in CHECKS_BY_DOMAIN:
                    CHECKS_BY_DOMAIN[domain] = []
                CHECKS_BY_DOMAIN[domain].append(check_def)

    return warnings


def audit_project(path: Path) -> AuditResult:
    """Run audit checks against a project.

    Args:
        path: Project directory.

    Returns:
        AuditResult with all check results.
    """
    project_root = path.resolve()

    # Load config to get domain
    load_result = load_praxis_config(project_root)
    if not load_result.valid or not load_result.config:
        return AuditResult(
            project_name=project_root.name,
            domain="unknown",
            checks=[
                AuditCheck(
                    name="config_valid",
                    category="setup",
                    status="failed",
                    message="Invalid or missing praxis.yaml",
                )
            ],
        )

    config = load_result.config

    # Register extension checks (lazy loading)
    extension_warnings = register_extension_checks()

    check_defs = CHECKS_BY_DOMAIN.get(config.domain, [])

    results: list[AuditCheck] = []

    # Add any extension loading warnings as info checks
    for warning in extension_warnings:
        results.append(
            AuditCheck(
                name="extension_loading",
                category="setup",
                status="warning",
                message=f"Extension loading: {warning}",
            )
        )

    for check in check_defs:
        # Skip checks that don't apply to current stage/subtype
        if not _check_applies(check, config):
            continue

        try:
            passed = check.check_fn(project_root)
        except Exception:
            # If check fails to run, treat as failed
            passed = False

        results.append(
            AuditCheck(
                name=check.name,
                category=check.category,
                status="passed" if passed else check.severity,
                message=check.pass_message if passed else check.fail_message,
            )
        )

    return AuditResult(
        project_name=project_root.name,
        domain=config.domain.value,
        checks=results,
    )
