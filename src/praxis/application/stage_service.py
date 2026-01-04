"""Transition a project to a new lifecycle stage."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path

from praxis.domain.domains import ARTIFACT_PATHS
from praxis.domain.models import (
    PraxisConfig,
    StageHistoryEntry,
    StageResult,
    ValidationIssue,
)
from praxis.domain.stages import ALLOWED_REGRESSIONS, REQUIRES_ARTIFACT, Stage
from praxis.infrastructure.claude_md_updater import update_claude_md_stage
from praxis.infrastructure.yaml_loader import load_praxis_config
from praxis.infrastructure.yaml_writer import update_praxis_yaml


def is_crossing_formalize(current: Stage, target: Stage) -> bool:
    """Check if a regression crosses the Formalize boundary.

    Crossing occurs when moving from post-Formalize (Commit+) to
    pre-Formalize (Shape-).

    Args:
        current: Current stage.
        target: Target stage.

    Returns:
        True if regression crosses Formalize boundary.
    """
    # Pre-Formalize stages
    pre_formalize = {Stage.CAPTURE, Stage.SENSE, Stage.EXPLORE, Stage.SHAPE}
    # Post-Formalize stages (same as REQUIRES_ARTIFACT)
    post_formalize = REQUIRES_ARTIFACT

    # Crossing happens when:
    # 1. We're regressing (target < current)
    # 2. Current is post-Formalize
    # 3. Target is pre-Formalize
    return (
        target < current
        and current in post_formalize
        and target in pre_formalize
    )


def find_active_contract(config: PraxisConfig) -> str | None:
    """Find the most recent active contract ID from history.

    Searches history for the most recent Formalize transition that
    has a contract_id.

    Args:
        config: Current project configuration.

    Returns:
        Contract ID string if found, None otherwise.
    """
    # Search history in reverse (most recent first)
    for entry in reversed(config.history):
        if entry.to_stage == Stage.FORMALIZE.value and entry.contract_id:
            return entry.contract_id
    return None


def transition_stage(
    path: Path,
    new_stage_str: str,
    force: bool = False,
    reason: str | None = None,
) -> StageResult:
    """Transition a project to a new lifecycle stage.

    Args:
        path: Project directory.
        new_stage_str: Target stage name.
        force: If True, proceed with invalid regressions.
        reason: Rationale for non-standard regressions.

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
            # This is a non-standard regression
            # Check if crossing Formalize boundary
            crossing = is_crossing_formalize(current_config.stage, new_stage)
            contract_id = None
            if crossing:
                contract_id = find_active_contract(current_config)

            # Build enhanced warning message
            warning_parts = [
                f"Regression from '{current_config.stage.value}' to "
                f"'{new_stage.value}' is not standard."
            ]

            if crossing:
                warning_parts.append("This crosses the Formalize boundary.")
                if contract_id:
                    warning_parts.append(f"This will void {contract_id}.")

            warning_parts.append(
                f"Allowed: {', '.join(s.value for s in allowed) or 'none'}."
            )
            warning_parts.append("Provide --reason to document rationale.")

            warning_message = " ".join(warning_parts)

            # If reason is provided, proceed automatically
            if reason is not None:
                force = True
            if not force:
                return StageResult(
                    success=False,
                    needs_confirmation=True,
                    warning_message=warning_message,
                    crossing_formalize=crossing,
                    voided_contract_id=contract_id,
                )
            # Force mode requires reason for auditability
            if reason is None:
                return StageResult(
                    success=False,
                    issues=[
                        ValidationIssue(
                            rule="regression_reason_required",
                            severity="error",
                            message=(
                                "Non-standard regression requires --reason flag "
                                "to document rationale"
                            ),
                        )
                    ],
                )
            # If force and reason provided, add warning but continue
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

    # 6. Create history entry
    timestamp = datetime.now(timezone.utc).isoformat()

    # Generate contract ID for Formalize transitions
    contract_id = None
    if new_stage == Stage.FORMALIZE:
        # Format: contract-YYYYMMDD-HHMMSS
        dt = datetime.now(timezone.utc)
        contract_id = dt.strftime("contract-%Y%m%d-%H%M%S")

    # Create new history entry
    new_entry = StageHistoryEntry(
        timestamp=timestamp,
        from_stage=current_config.stage.value,
        to_stage=new_stage.value,
        contract_id=contract_id,
        reason=reason,
    )

    # Append to existing history
    updated_history = current_config.history + [new_entry]

    # 7. Update praxis.yaml with new stage and history
    success, error = update_praxis_yaml(
        project_root, stage=new_stage, history=updated_history
    )
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

    # 8. Update CLAUDE.md (best effort, don't fail if it doesn't work)
    update_claude_md_stage(project_root, new_stage)

    # 9. Render stage doc template for the new stage (best effort)
    try:
        from praxis.application.templates import render_stage_templates

        template_result = render_stage_templates(
            project_root=project_root,
            domain=current_config.domain,
            subtype=None,
            stages=[new_stage],
            force=False,
        )

        if not template_result.success:
            for err in template_result.errors:
                issues.append(
                    ValidationIssue(
                        rule="template_render_error",
                        severity="warning",
                        message=f"Template render warning: {err}",
                    )
                )
    except (FileNotFoundError, ValueError, OSError) as e:
        issues.append(
            ValidationIssue(
                rule="template_render_error",
                severity="warning",
                message=f"Template render warning: {e}",
            )
        )
    except Exception as e:
        logging.getLogger(__name__).exception(
            "Unexpected error during template rendering"
        )
        issues.append(
            ValidationIssue(
                rule="template_render_error",
                severity="warning",
                message=f"Template render warning: {e}",
            )
        )

    return StageResult(success=True, issues=issues)
