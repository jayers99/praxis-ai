"""Pipeline orchestration services for init and status."""

from __future__ import annotations

import uuid
from datetime import datetime
from pathlib import Path

from praxis.domain.pipeline.models import (
    PipelineConfig,
    PipelineInitResult,
    PipelineState,
    PipelineStatus,
    StageExecution,
    StageProgress,
)
from praxis.domain.pipeline.risk_tiers import (
    REQUIRED_STAGES,
    RiskTier,
    get_next_required_stage,
    is_stage_required,
)
from praxis.domain.pipeline.stages import PipelineStage
from praxis.infrastructure.pipeline.pipeline_state_repo import (
    create_pipeline_run_directory,
    get_stage_output_path,
    load_pipeline_state,
    save_pipeline_state,
)
from praxis.infrastructure.yaml_loader import load_praxis_config


def init_pipeline(
    project_root: Path,
    risk_tier: int,
    source_corpus_path: Path,
    force: bool = False,
) -> PipelineInitResult:
    """Initialize a new knowledge distillation pipeline.

    Args:
        project_root: Project directory containing praxis.yaml.
        risk_tier: Risk tier (0-3) determining required stages.
        source_corpus_path: Path to the source corpus for RTC stage.
        force: If True, replace existing active pipeline.

    Returns:
        PipelineInitResult with pipeline_id and required stages.
    """
    errors: list[str] = []

    # Validate project has praxis.yaml
    praxis_result = load_praxis_config(project_root)
    if not praxis_result.valid:
        errors.append("Project must have a valid praxis.yaml")
        for issue in praxis_result.issues:
            errors.append(f"  - {issue.message}")
        return PipelineInitResult(success=False, errors=errors)

    # Validate risk tier
    try:
        tier = RiskTier(risk_tier)
    except ValueError:
        valid_tiers = ", ".join(str(t.value) for t in RiskTier)
        errors.append(f"Invalid risk tier: {risk_tier}. Valid options: {valid_tiers}")
        return PipelineInitResult(success=False, errors=errors)

    # Validate source corpus exists
    if not source_corpus_path.exists():
        errors.append(f"Source corpus not found: {source_corpus_path}")
        return PipelineInitResult(success=False, errors=errors)

    # Check for existing active pipeline
    existing_state = load_pipeline_state(project_root)
    if existing_state is not None and not force:
        errors.append(
            f"Active pipeline exists: {existing_state.config.pipeline_id}. "
            "Use --force to replace."
        )
        return PipelineInitResult(success=False, errors=errors)

    # Generate pipeline ID
    pipeline_id = str(uuid.uuid4())[:8]

    # Create pipeline config
    config = PipelineConfig(
        pipeline_id=pipeline_id,
        risk_tier=tier,
        current_stage=PipelineStage.RTC,
        started_at=datetime.now(),
        source_corpus_path=source_corpus_path.resolve(),
    )

    # Initialize stage executions for all required stages
    stages: dict[PipelineStage, StageExecution] = {}
    required_stages = REQUIRED_STAGES[tier]
    for stage in PipelineStage:
        if stage in required_stages:
            stages[stage] = StageExecution(
                stage=stage,
                status="pending",
            )

    state = PipelineState(config=config, stages=stages)

    # Create pipeline run directory
    create_pipeline_run_directory(project_root, pipeline_id)

    # Save pipeline state
    save_pipeline_state(project_root, state)

    return PipelineInitResult(
        success=True,
        pipeline_id=pipeline_id,
        risk_tier=tier,
        required_stages=required_stages,
    )


def get_pipeline_status(project_root: Path) -> PipelineStatus:
    """Get current pipeline status.

    Args:
        project_root: Project directory.

    Returns:
        PipelineStatus with progress information.
    """
    errors: list[str] = []

    # Load pipeline state
    state = load_pipeline_state(project_root)
    if state is None:
        return PipelineStatus(
            errors=["No active pipeline. Use 'praxis pipeline init' to start one."],
        )

    config = state.config
    tier = config.risk_tier

    # Build stage progress
    stage_progress: list[StageProgress] = []
    all_required_complete = True

    for stage in PipelineStage:
        required = is_stage_required(tier, stage)
        if stage in state.stages:
            status = state.stages[stage].status
            output_path = get_stage_output_path(
                project_root, config.pipeline_id, stage
            )
            output_exists = output_path.exists()
        else:
            status = "skipped" if not required else "pending"
            output_exists = False

        if required and status != "completed":
            all_required_complete = False

        stage_progress.append(
            StageProgress(
                stage=stage,
                required=required,
                status=status,
                output_exists=output_exists,
            )
        )

    # Determine next stage
    completed_stages = state.get_completed_stages()
    last_completed = completed_stages[-1] if completed_stages else None
    next_stage = get_next_required_stage(tier, last_completed)

    # Check if awaiting HVA
    awaiting_hva = (
        is_stage_required(tier, PipelineStage.HVA)
        and state.is_stage_completed(PipelineStage.ASR)
        and not state.is_stage_completed(PipelineStage.HVA)
    )

    return PipelineStatus(
        pipeline_id=config.pipeline_id,
        risk_tier=tier,
        current_stage=config.current_stage,
        stage_progress=stage_progress,
        next_stage=next_stage,
        is_complete=all_required_complete,
        awaiting_hva=awaiting_hva,
        errors=errors,
    )


def advance_pipeline_stage(
    project_root: Path,
    to_stage: PipelineStage,
) -> tuple[bool, str | None]:
    """Advance the pipeline to a new current stage.

    Args:
        project_root: Project directory.
        to_stage: Stage to advance to.

    Returns:
        Tuple of (success, error_message).
    """
    state = load_pipeline_state(project_root)
    if state is None:
        return False, "No active pipeline"

    # Update current stage
    state.config.current_stage = to_stage

    save_pipeline_state(project_root, state)
    return True, None


def mark_stage_started(
    project_root: Path,
    stage: PipelineStage,
) -> tuple[bool, str | None]:
    """Mark a stage as in_progress.

    Args:
        project_root: Project directory.
        stage: Stage to mark as started.

    Returns:
        Tuple of (success, error_message).
    """
    state = load_pipeline_state(project_root)
    if state is None:
        return False, "No active pipeline"

    if stage not in state.stages:
        state.stages[stage] = StageExecution(
            stage=stage,
            status="in_progress",
            started_at=datetime.now(),
        )
    else:
        state.stages[stage].status = "in_progress"
        state.stages[stage].started_at = datetime.now()

    save_pipeline_state(project_root, state)
    return True, None


def mark_stage_completed(
    project_root: Path,
    stage: PipelineStage,
    output_path: Path | None = None,
) -> tuple[bool, str | None]:
    """Mark a stage as completed.

    Args:
        project_root: Project directory.
        stage: Stage to mark as completed.
        output_path: Optional path to stage output file.

    Returns:
        Tuple of (success, error_message).
    """
    state = load_pipeline_state(project_root)
    if state is None:
        return False, "No active pipeline"

    if stage not in state.stages:
        state.stages[stage] = StageExecution(
            stage=stage,
            status="completed",
            completed_at=datetime.now(),
            output_path=output_path,
        )
    else:
        state.stages[stage].status = "completed"
        state.stages[stage].completed_at = datetime.now()
        if output_path:
            state.stages[stage].output_path = output_path

    # Advance current stage if needed
    next_stage = stage.next_stage()
    if next_stage:
        state.config.current_stage = next_stage

    save_pipeline_state(project_root, state)
    return True, None
