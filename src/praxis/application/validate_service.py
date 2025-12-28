"""Validation service - orchestrates all validation rules."""

from __future__ import annotations

from pathlib import Path

from praxis.domain.models import ValidationResult
from praxis.infrastructure.artifact_checker import check_artifact_exists
from praxis.infrastructure.git_history import (
    check_privacy_downgrade,
    check_regression,
    get_previous_config,
)
from praxis.infrastructure.yaml_loader import load_praxis_config


def validate(path: Path) -> ValidationResult:
    """Validate a praxis.yaml configuration.

    Performs all validation checks:
    1. Schema validation (via Pydantic)
    2. Artifact existence check
    3. Regression detection (vs previous commit)
    4. Privacy downgrade detection (vs previous commit)

    Args:
        path: Path to praxis.yaml file or project directory.

    Returns:
        ValidationResult with all issues found.
    """
    # Resolve project root
    if path.is_dir():
        project_root = path
    else:
        project_root = path.parent

    # Step 1: Load and validate schema
    result = load_praxis_config(path)
    if not result.valid or result.config is None:
        return result

    config = result.config
    issues = list(result.issues)

    # Step 2: Check artifact existence
    artifact_issue = check_artifact_exists(config, project_root)
    if artifact_issue is not None:
        issues.append(artifact_issue)

    # Step 3: Get previous config for regression checks
    previous_config = get_previous_config(project_root)

    # Step 4: Check for invalid regression
    regression_issue = check_regression(config, previous_config)
    if regression_issue is not None:
        issues.append(regression_issue)

    # Step 5: Check for privacy downgrade
    privacy_issue = check_privacy_downgrade(config, previous_config)
    if privacy_issue is not None:
        issues.append(privacy_issue)

    # Determine overall validity (errors make it invalid, warnings don't)
    has_errors = any(issue.severity == "error" for issue in issues)

    return ValidationResult(
        valid=not has_errors,
        config=config,
        issues=issues,
    )
