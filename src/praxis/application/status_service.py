"""Get project status information."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from praxis.application.validate_service import validate
from praxis.domain.domains import ARTIFACT_PATHS
from praxis.domain.models import PraxisConfig, ValidationResult
from praxis.domain.stages import REQUIRES_ARTIFACT, Stage
from praxis.infrastructure.yaml_loader import load_praxis_config


@dataclass
class StageHistoryEntry:
    """A single stage change in history."""

    stage: str
    commit_hash: str
    commit_date: str
    commit_message: str


@dataclass
class ProjectStatus:
    """Complete project status information."""

    # Basic info
    project_name: str
    config: PraxisConfig | None

    # Stage info
    stage_index: int  # 1-based index
    stage_count: int  # Total stages (9)
    next_stage: Stage | None
    next_stage_requirements: list[str]

    # Artifact info
    artifact_path: str | None
    artifact_exists: bool

    # Validation
    validation: ValidationResult

    # History
    stage_history: list[StageHistoryEntry]

    # Errors
    errors: list[str]


def get_stage_history(project_root: Path, limit: int = 10) -> list[StageHistoryEntry]:
    """Get history of stage changes from git log.

    Args:
        project_root: Project directory.
        limit: Maximum number of entries to return.

    Returns:
        List of stage history entries, most recent first.
    """
    history: list[StageHistoryEntry] = []

    try:
        # Get git log for praxis.yaml changes
        result = subprocess.run(
            [
                "git", "log",
                f"-{limit}",
                "--format=%H|%ad|%s",
                "--date=short",
                "--follow",
                "--",
                "praxis.yaml",
            ],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            return history

        for line in result.stdout.strip().split("\n"):
            if not line:
                continue

            parts = line.split("|", 2)
            if len(parts) != 3:
                continue

            commit_hash, commit_date, commit_message = parts

            # Get the stage value at this commit
            stage_result = subprocess.run(
                ["git", "show", f"{commit_hash}:praxis.yaml"],
                cwd=project_root,
                capture_output=True,
                text=True,
                check=False,
            )

            if stage_result.returncode == 0:
                import yaml
                try:
                    data = yaml.safe_load(stage_result.stdout)
                    if data and "stage" in data:
                        history.append(
                            StageHistoryEntry(
                                stage=data["stage"],
                                commit_hash=commit_hash[:7],
                                commit_date=commit_date,
                                commit_message=commit_message[:50],
                            )
                        )
                except yaml.YAMLError:
                    pass

    except subprocess.SubprocessError:
        pass

    return history


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


def get_status(path: Path) -> ProjectStatus:
    """Get complete project status.

    Args:
        path: Project directory.

    Returns:
        ProjectStatus with all status information.
    """
    errors: list[str] = []
    project_root = path.resolve()
    project_name = project_root.name

    # Load config
    load_result = load_praxis_config(project_root)

    if not load_result.valid or load_result.config is None:
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
            stage_history=[],
            errors=[i.message for i in load_result.issues],
        )

    config = load_result.config
    stages = list(Stage)
    stage_index = stages.index(config.stage) + 1  # 1-based

    # Next stage
    next_stage = get_next_stage(config.stage)

    # Artifact info
    artifact_path = ARTIFACT_PATHS.get(config.domain)
    artifact_exists = False
    if artifact_path:
        artifact_exists = (project_root / artifact_path).exists()

    # Requirements
    requirements = get_next_stage_requirements(
        config.stage, next_stage, config, project_root
    )

    # Validation
    validation = validate(project_root)

    # History
    history = get_stage_history(project_root)

    return ProjectStatus(
        project_name=project_name,
        config=config,
        stage_index=stage_index,
        stage_count=len(Stage),
        next_stage=next_stage,
        next_stage_requirements=requirements,
        artifact_path=artifact_path,
        artifact_exists=artifact_exists,
        validation=validation,
        stage_history=history,
        errors=errors,
    )
