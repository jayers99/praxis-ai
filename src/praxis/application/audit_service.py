"""Run audit checks against a project."""

from __future__ import annotations

from pathlib import Path

from praxis.domain.audit_checks import CHECKS_BY_DOMAIN, CheckDefinition
from praxis.domain.models import AuditCheck, AuditResult, PraxisConfig
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
    check_defs = CHECKS_BY_DOMAIN.get(config.domain, [])

    results: list[AuditCheck] = []
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
