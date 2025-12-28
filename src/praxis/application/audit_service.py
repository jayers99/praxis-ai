"""Run audit checks against a project."""

from __future__ import annotations

from pathlib import Path

from praxis.domain.audit_checks import CHECKS_BY_DOMAIN
from praxis.domain.models import AuditCheck, AuditResult
from praxis.infrastructure.yaml_loader import load_praxis_config


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
