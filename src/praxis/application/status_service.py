"""Get project status information."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from praxis.application.validate_service import validate
from praxis.domain.domains import ARTIFACT_PATHS
from praxis.domain.models import PraxisConfig, ValidationResult
from praxis.domain.next_steps import NextStep
from praxis.domain.stages import REQUIRES_ARTIFACT, Stage
from praxis.infrastructure.yaml_loader import load_praxis_config


class StageHistoryDisplay(BaseModel):
    """Stage history entry for display in status output."""

    timestamp: str
    from_stage: str
    to_stage: str
    contract_id: str | None = None
    reason: str | None = None


class ProjectStatus(BaseModel):
    """Complete project status information."""

    # Basic info
    project_name: str
    config: PraxisConfig | None = None

    # Stage info
    stage_index: int = 0  # 1-based index
    stage_count: int = 9  # Total stages
    next_stage: Stage | None = None
    next_stage_requirements: list[str] = Field(default_factory=list)

    # Artifact info
    artifact_path: str | None = None
    artifact_exists: bool = False

    # Checklist info
    checklist_path: str | None = None
    checklist_addendum_path: str | None = None

    # Validation
    validation: ValidationResult

    # Next steps guidance
    next_steps: list[NextStep] = Field(default_factory=list)

    # History
    stage_history: list[StageHistoryDisplay] = Field(default_factory=list)

    # Errors
    errors: list[str] = Field(default_factory=list)


def get_stage_history_from_config(
    config: PraxisConfig, limit: int = 10
) -> list[StageHistoryDisplay]:
    """Get stage history from praxis.yaml config.

    Args:
        config: Current praxis config.
        limit: Maximum number of entries to return.

    Returns:
        List of stage history entries, most recent first.
    """
    # Get last N entries in reverse order (most recent first)
    if not config.history:
        return []

    history_entries = config.history[-limit:][::-1]
    return [
        StageHistoryDisplay(
            timestamp=entry.timestamp,
            from_stage=entry.from_stage,
            to_stage=entry.to_stage,
            contract_id=entry.contract_id,
            reason=entry.reason,
        )
        for entry in history_entries
    ]


def get_next_stage(current: Stage) -> Stage | None:
    """Get the next stage in the lifecycle.

    Args:
        current: Current stage.

    Returns:
        Next stage, or None if at Close.
    """
    stages = list(Stage)
    current_index = stages.index(current)

    if current_index >= len(stages) - 1:
        return None  # Already at Close

    return stages[current_index + 1]


def get_next_stage_requirements(
    current_stage: Stage,
    next_stage: Stage | None,
    config: PraxisConfig,
    project_root: Path,
) -> list[str]:
    """Get requirements to advance to the next stage.

    Args:
        current_stage: Current stage.
        next_stage: Next stage (or None if at Close).
        config: Current project config.
        project_root: Project directory.

    Returns:
        List of requirement descriptions.
    """
    if next_stage is None:
        return ["Project is at final stage (close)."]

    requirements: list[str] = []

    # Check if next stage requires artifact
    if next_stage in REQUIRES_ARTIFACT:
        artifact_path = ARTIFACT_PATHS.get(config.domain)
        if artifact_path:
            full_path = project_root / artifact_path
            if not full_path.exists():
                requirements.append(f"Create {artifact_path}")

    # Stage-specific guidance
    if next_stage == Stage.FORMALIZE:
        requirements.append("Lock scope and create formalization artifact")
    elif next_stage == Stage.COMMIT:
        requirements.append("Verify readiness to build")
    elif next_stage == Stage.EXECUTE:
        requirements.append("Build the implementation")
    elif next_stage == Stage.SUSTAIN:
        requirements.append("Complete initial implementation")

    if not requirements:
        requirements.append("No blockers - ready to advance")

    return requirements


def resolve_checklist_paths(
    stage: Stage,
    domain: str,
) -> tuple[str | None, str | None]:
    """Resolve checklist paths for the current stage and domain.

    Args:
        stage: Current lifecycle stage.
        domain: Project domain.

    Returns:
        Tuple of (base_checklist_path, addendum_path).
        Both paths are relative to the project root.
        Returns None for addendum if no domain-specific checklist exists.
    """
    # Base checklist path
    base_path = f"core/checklists/{stage.value}.md"

    # Domain addendum path (if it exists)
    addendum_path = f"core/checklists/{stage.value}-{domain}.md"

    # We don't check file existence here - that happens in the CLI layer
    # This service just provides the canonical paths
    return (base_path, addendum_path)


def get_status(path: Path) -> ProjectStatus:
    """Get complete project status.

    Args:
        path: Project directory.

    Returns:
        ProjectStatus with all status information.
    """
    from praxis.application.next_steps_service import get_next_steps

    errors: list[str] = []
    project_root = path.resolve()

    # Load config first to get project name from config if available
    load_result = load_praxis_config(project_root)

    # Use config.name if present, otherwise fall back to directory name
    if load_result.valid and load_result.config and load_result.config.name:
        project_name = load_result.config.name
    else:
        project_name = project_root.name

    if not load_result.valid or load_result.config is None:
        # Generate next steps even for invalid config
        next_steps = get_next_steps(None, load_result, project_root)
        return ProjectStatus(
            project_name=project_name,
            config=None,
            stage_index=0,
            stage_count=len(Stage),
            next_stage=None,
            next_stage_requirements=[],
            artifact_path=None,
            artifact_exists=False,
            validation=load_result,
            next_steps=next_steps,
            stage_history=[],
            errors=[i.message for i in load_result.issues],
        )

    config = load_result.config
    stages = list(Stage)
    stage_index = stages.index(config.stage) + 1  # 1-based

    # Next stage
    next_stage = get_next_stage(config.stage)

    # Artifact info
    artifact_path_obj = ARTIFACT_PATHS.get(config.domain)
    artifact_path = str(artifact_path_obj) if artifact_path_obj else None
    artifact_exists = False
    if artifact_path_obj:
        artifact_exists = (project_root / artifact_path_obj).exists()

    # Checklist info
    checklist_base, checklist_addendum = resolve_checklist_paths(
        config.stage, config.domain.value
    )

    # Requirements
    requirements = get_next_stage_requirements(
        config.stage, next_stage, config, project_root
    )

    # Validation
    validation = validate(project_root)

    # Next steps guidance
    next_steps = get_next_steps(config, validation, project_root)

    # History from praxis.yaml
    history = get_stage_history_from_config(config)

    return ProjectStatus(
        project_name=project_name,
        config=config,
        stage_index=stage_index,
        stage_count=len(Stage),
        next_stage=next_stage,
        next_stage_requirements=requirements,
        artifact_path=artifact_path,
        artifact_exists=artifact_exists,
        checklist_path=checklist_base,
        checklist_addendum_path=checklist_addendum,
        validation=validation,
        next_steps=next_steps,
        stage_history=history,
        errors=errors,
    )
