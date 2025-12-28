"""Check for required artifact existence on filesystem."""

from __future__ import annotations

from pathlib import Path

from praxis.domain.domains import ARTIFACT_PATHS
from praxis.domain.models import PraxisConfig, ValidationIssue
from praxis.domain.stages import REQUIRES_ARTIFACT


def check_artifact_exists(
    config: PraxisConfig,
    project_root: Path,
) -> ValidationIssue | None:
    """Check if the required formalization artifact exists.

    Args:
        config: The parsed praxis.yaml configuration.
        project_root: Path to the project root directory.

    Returns:
        A ValidationIssue if the artifact is missing, None otherwise.
    """
    # Only check for stages that require artifacts
    if config.stage not in REQUIRES_ARTIFACT:
        return None

    # Get the artifact path for this domain
    artifact_path = ARTIFACT_PATHS.get(config.domain)
    if artifact_path is None:
        # Observe domain has no required artifact
        return None

    full_path = project_root / artifact_path
    if not full_path.exists():
        return ValidationIssue(
            rule="missing_artifact",
            severity="error",
            message=(
                f"Stage '{config.stage.value}' requires formalization artifact "
                f"at '{artifact_path}', but file not found"
            ),
        )

    return None
