"""Transition a project to a new lifecycle stage."""

from __future__ import annotations

from pathlib import Path

from praxis.domain.domains import ARTIFACT_PATHS
from praxis.domain.models import StageResult, ValidationIssue
from praxis.domain.stages import ALLOWED_REGRESSIONS, REQUIRES_ARTIFACT, Stage
from praxis.infrastructure.claude_md_updater import update_claude_md_stage
from praxis.infrastructure.yaml_loader import load_praxis_config
from praxis.infrastructure.yaml_writer import update_praxis_yaml


def transition_stage(
    path: Path,
    new_stage_str: str,
    force: bool = False,
) -> StageResult:
    """Transition a project to a new lifecycle stage.

    Args:
        path: Project directory.
        new_stage_str: Target stage name.
        force: If True, proceed with invalid regressions.

    Returns:
        StageResult with success status, issues, and confirmation needs.
    """
    issues: list[ValidationIssue] = []

    # 1. Validate new stage is valid enum
    try:
        new_stage = Stage(new_stage_str)
    except ValueError:
        valid_stages = ", ".join(s.value for s in Stage)
        return StageResult(
            success=False,
            issues=[
                ValidationIssue(
                    rule="invalid_stage",
                    severity="error",
                    message=f"Invalid stage: '{new_stage_str}'. Valid: {valid_stages}",
                )
            ],
        )

    # 2. Load current config
    project_root = path.resolve()
    load_result = load_praxis_config(project_root)
    if not load_result.valid:
        return StageResult(success=False, issues=load_result.issues)

    current_config = load_result.config
    assert current_config is not None  # Guaranteed by load_result.valid

    # 3. Check if same stage (no-op)
    if new_stage == current_config.stage:
        return StageResult(
            success=True,
            issues=[
                ValidationIssue(
                    rule="same_stage",
                    severity="warning",
                    message=f"Already at stage '{new_stage.value}'",
                )
            ],
        )

    # 4. Check if this is a regression
    if new_stage < current_config.stage:
        allowed = ALLOWED_REGRESSIONS.get(current_config.stage, frozenset())
        if new_stage not in allowed:
            if not force:
                return StageResult(
                    success=False,
                    needs_confirmation=True,
                    warning_message=(
                        f"Regression from '{current_config.stage.value}' to "
                        f"'{new_stage.value}' is not standard. "
                        f"Allowed: {', '.join(s.value for s in allowed) or 'none'}"
                    ),
                )
            # If force, add warning but continue
            issues.append(
                ValidationIssue(
                    rule="stage_regression",
                    severity="warning",
                    message=f"Non-standard regression to '{new_stage.value}'",
                )
            )

    # 5. Check artifact requirement (warn only)
    if new_stage in REQUIRES_ARTIFACT:
        artifact_path = ARTIFACT_PATHS.get(current_config.domain)
        if artifact_path:
            full_path = project_root / artifact_path
            if not full_path.exists():
                issues.append(
                    ValidationIssue(
                        rule="artifact_missing",
                        severity="warning",
                        message=(
                            f"Stage '{new_stage.value}' typically requires "
                            f"'{artifact_path}'"
                        ),
                    )
                )

    # 6. Update praxis.yaml
    success, error = update_praxis_yaml(project_root, stage=new_stage)
    if not success:
        return StageResult(
            success=False,
            issues=[
                ValidationIssue(
                    rule="yaml_write_error",
                    severity="error",
                    message=error or "Failed to update praxis.yaml",
                )
            ],
        )

    # 7. Update CLAUDE.md (best effort, don't fail if it doesn't work)
    update_claude_md_stage(project_root, new_stage)

    return StageResult(success=True, issues=issues)
