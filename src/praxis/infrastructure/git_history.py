"""Git-based history detection for regression and privacy changes."""

from __future__ import annotations

import subprocess
from pathlib import Path

import yaml
from pydantic import ValidationError

from praxis.domain.models import PraxisConfig, ValidationIssue
from praxis.domain.stages import ALLOWED_REGRESSIONS


def get_previous_config(project_root: Path) -> PraxisConfig | None:
    """Load praxis.yaml from the previous commit (HEAD).

    Args:
        project_root: Path to the project root directory.

    Returns:
        The previous PraxisConfig if available, None otherwise.
    """
    try:
        result = subprocess.run(
            ["git", "show", "HEAD:praxis.yaml"],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            # File didn't exist in previous commit or not a git repo
            return None

        data = yaml.safe_load(result.stdout)
        if data is None:
            return None

        return PraxisConfig.model_validate(data)
    except (subprocess.SubprocessError, yaml.YAMLError, ValidationError):
        return None


def check_regression(
    current: PraxisConfig,
    previous: PraxisConfig | None,
) -> ValidationIssue | None:
    """Check if the stage transition is a valid regression.

    Args:
        current: The current praxis.yaml configuration.
        previous: The previous praxis.yaml configuration (from HEAD).

    Returns:
        A ValidationIssue warning if regression is invalid, None otherwise.
    """
    if previous is None:
        return None

    # Not a regression if moving forward or staying same
    if current.stage >= previous.stage:
        return None

    # Check if this regression is allowed
    allowed = ALLOWED_REGRESSIONS.get(previous.stage, frozenset())
    if current.stage in allowed:
        return None

    allowed_str = ", ".join(s.value for s in allowed) if allowed else "none"
    return ValidationIssue(
        rule="invalid_regression",
        severity="warning",
        message=(
            f"Regression from '{previous.stage.value}' to '{current.stage.value}' "
            f"is not in allowed regression table. "
            f"Allowed targets from {previous.stage.value}: {allowed_str}"
        ),
    )


def check_privacy_downgrade(
    current: PraxisConfig,
    previous: PraxisConfig | None,
) -> ValidationIssue | None:
    """Check if privacy level was downgraded (made less restrictive).

    Args:
        current: The current praxis.yaml configuration.
        previous: The previous praxis.yaml configuration (from HEAD).

    Returns:
        A ValidationIssue warning if privacy was downgraded, None otherwise.
    """
    if previous is None:
        return None

    # Downgrade = current is less restrictive than previous
    if current.privacy_level < previous.privacy_level:
        return ValidationIssue(
            rule="privacy_downgrade",
            severity="warning",
            message=(
                f"Privacy level downgraded from '{previous.privacy_level.value}' "
                f"to '{current.privacy_level.value}'. "
                f"This makes the project less restrictive."
            ),
        )

    return None
