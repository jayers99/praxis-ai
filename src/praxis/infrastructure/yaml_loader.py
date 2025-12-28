"""Load and parse praxis.yaml files."""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import ValidationError

from praxis.domain.models import PraxisConfig, ValidationIssue, ValidationResult
from praxis.infrastructure.env_resolver import resolve_environment


def load_praxis_config(path: Path) -> ValidationResult:
    """Load and validate a praxis.yaml file.

    Args:
        path: Path to praxis.yaml file or project directory.

    Returns:
        ValidationResult with parsed config or validation issues.
    """
    # Resolve to praxis.yaml if path is a directory
    if path.is_dir():
        yaml_path = path / "praxis.yaml"
    else:
        yaml_path = path

    # Check file exists
    if not yaml_path.exists():
        return ValidationResult(
            valid=False,
            issues=[
                ValidationIssue(
                    rule="file_not_found",
                    severity="error",
                    message=f"praxis.yaml not found at '{yaml_path}'",
                )
            ],
        )

    # Parse YAML
    try:
        with yaml_path.open() as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return ValidationResult(
            valid=False,
            issues=[
                ValidationIssue(
                    rule="yaml_parse_error",
                    severity="error",
                    message=f"Failed to parse YAML: {e}",
                )
            ],
        )

    if data is None:
        return ValidationResult(
            valid=False,
            issues=[
                ValidationIssue(
                    rule="empty_config",
                    severity="error",
                    message="praxis.yaml is empty",
                )
            ],
        )

    # Apply environment override
    if "environment" in data:
        data["environment"] = resolve_environment(data["environment"])
    else:
        # Default to Home, but allow PRAXIS_ENV override
        data["environment"] = resolve_environment("Home")

    # Validate with Pydantic
    try:
        config = PraxisConfig.model_validate(data)
        return ValidationResult(valid=True, config=config)
    except ValidationError as e:
        issues = []
        for error in e.errors():
            field = ".".join(str(loc) for loc in error["loc"])
            issues.append(
                ValidationIssue(
                    rule="schema_validation",
                    severity="error",
                    message=f"Invalid {field}: {error['msg']}",
                )
            )
        return ValidationResult(valid=False, issues=issues)
