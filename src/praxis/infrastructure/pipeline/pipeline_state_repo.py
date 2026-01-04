"""Pipeline state persistence operations."""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from praxis.domain.pipeline.models import (
    AgentOutput,
    PipelineConfig,
    PipelineState,
    StageExecution,
)
from praxis.domain.pipeline.risk_tiers import RiskTier
from praxis.domain.pipeline.stages import PipelineStage

PIPELINE_YAML = "pipeline.yaml"
PIPELINE_RUNS_DIR = "pipeline-runs"


def load_pipeline_state(project_root: Path) -> PipelineState | None:
    """Load pipeline state from pipeline.yaml if it exists.

    Args:
        project_root: Project directory containing pipeline.yaml.

    Returns:
        PipelineState if file exists and is valid, None otherwise.
    """
    yaml_path = project_root / PIPELINE_YAML

    if not yaml_path.exists():
        return None

    try:
        with yaml_path.open() as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError:
        return None

    if data is None:
        return None

    return _deserialize_pipeline_state(data, project_root)


def save_pipeline_state(project_root: Path, state: PipelineState) -> None:
    """Persist pipeline state to pipeline.yaml.

    Creates a backup before writing if the file exists.

    Args:
        project_root: Project directory for pipeline.yaml.
        state: Pipeline state to persist.
    """
    yaml_path = project_root / PIPELINE_YAML
    backup_path = project_root / f"{PIPELINE_YAML}.backup"

    # Create backup if file exists
    if yaml_path.exists():
        shutil.copy2(yaml_path, backup_path)

    data = _serialize_pipeline_state(state)

    with yaml_path.open("w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def create_pipeline_run_directory(project_root: Path, pipeline_id: str) -> Path:
    """Create the pipeline-runs/{id}/ directory structure.

    Args:
        project_root: Project directory.
        pipeline_id: Unique pipeline identifier.

    Returns:
        Path to the created pipeline run directory.
    """
    run_dir = project_root / PIPELINE_RUNS_DIR / pipeline_id

    # Create main directory
    run_dir.mkdir(parents=True, exist_ok=True)

    # Create CCR critiques subdirectory
    (run_dir / "ccr-critiques").mkdir(exist_ok=True)

    # Create SAD responses subdirectory
    (run_dir / "sad-responses").mkdir(exist_ok=True)

    return run_dir


def get_stage_output_path(
    project_root: Path,
    pipeline_id: str,
    stage: PipelineStage,
) -> Path:
    """Return the canonical path for a stage's output file.

    Args:
        project_root: Project directory.
        pipeline_id: Pipeline identifier.
        stage: Pipeline stage.

    Returns:
        Path where the stage output should be written.
    """
    run_dir = project_root / PIPELINE_RUNS_DIR / pipeline_id

    stage_files = {
        PipelineStage.RTC: "rtc-output.md",
        PipelineStage.IDAS: "idas-output.md",
        PipelineStage.SAD: "sad-dispatch.md",
        PipelineStage.CCR: "ccr-consolidated.md",
        PipelineStage.ASR: "asr-synthesis.md",
        PipelineStage.HVA: "hva-decision.md",
    }

    return run_dir / stage_files[stage]


def get_ccr_critique_path(
    project_root: Path,
    pipeline_id: str,
    agent_type: str,
) -> Path:
    """Return the path for a CCR challenger's critique file.

    Args:
        project_root: Project directory.
        pipeline_id: Pipeline identifier.
        agent_type: Type of challenger agent (e.g., "architect", "security").

    Returns:
        Path where the critique should be written.
    """
    run_dir = project_root / PIPELINE_RUNS_DIR / pipeline_id
    return run_dir / "ccr-critiques" / f"{agent_type}-critique.md"


def get_sad_response_path(
    project_root: Path,
    pipeline_id: str,
    specialist_type: str,
) -> Path:
    """Return the path for a SAD specialist's response file.

    Args:
        project_root: Project directory.
        pipeline_id: Pipeline identifier.
        specialist_type: Type of specialist agent.

    Returns:
        Path where the response should be written.
    """
    run_dir = project_root / PIPELINE_RUNS_DIR / pipeline_id
    return run_dir / "sad-responses" / f"{specialist_type}-response.md"


def _serialize_pipeline_state(state: PipelineState) -> dict[str, Any]:
    """Convert PipelineState to YAML-serializable dict."""
    config = state.config

    data: dict[str, Any] = {
        "pipeline_id": config.pipeline_id,
        "risk_tier": config.risk_tier.value,
        "current_stage": config.current_stage.value,
        "started_at": config.started_at.isoformat(),
        "source_corpus_path": str(config.source_corpus_path),
        "stages": {},
    }

    # Add optional rerun fields if present
    if config.prior_run_id:
        data["prior_run_id"] = config.prior_run_id
    if config.rerun_reason:
        data["rerun_reason"] = config.rerun_reason
    if config.search_query:
        data["search_query"] = config.search_query

    for stage, execution in state.stages.items():
        stage_data: dict[str, Any] = {
            "status": execution.status,
        }
        if execution.started_at:
            stage_data["started_at"] = execution.started_at.isoformat()
        if execution.completed_at:
            stage_data["completed_at"] = execution.completed_at.isoformat()
        if execution.output_path:
            stage_data["output_path"] = str(execution.output_path)
        if execution.agent_outputs:
            stage_data["agent_outputs"] = [
                {
                    "agent_type": ao.agent_type,
                    "output_path": str(ao.output_path),
                    "timestamp": ao.timestamp.isoformat(),
                }
                for ao in execution.agent_outputs
            ]

        data["stages"][stage.value] = stage_data

    return data


def _deserialize_pipeline_state(
    data: dict[str, Any],
    project_root: Path,
) -> PipelineState:
    """Convert YAML dict to PipelineState."""
    config = PipelineConfig(
        pipeline_id=data["pipeline_id"],
        risk_tier=RiskTier(data["risk_tier"]),
        current_stage=PipelineStage(data["current_stage"]),
        started_at=datetime.fromisoformat(data["started_at"]),
        source_corpus_path=Path(data["source_corpus_path"]),
        prior_run_id=data.get("prior_run_id"),
        rerun_reason=data.get("rerun_reason"),
        search_query=data.get("search_query"),
    )

    stages: dict[PipelineStage, StageExecution] = {}

    for stage_value, stage_data in data.get("stages", {}).items():
        stage = PipelineStage(stage_value)

        agent_outputs = []
        for ao_data in stage_data.get("agent_outputs", []):
            agent_outputs.append(
                AgentOutput(
                    agent_type=ao_data["agent_type"],
                    output_path=Path(ao_data["output_path"]),
                    timestamp=datetime.fromisoformat(ao_data["timestamp"]),
                )
            )

        execution = StageExecution(
            stage=stage,
            status=stage_data["status"],
            started_at=(
                datetime.fromisoformat(stage_data["started_at"])
                if "started_at" in stage_data
                else None
            ),
            completed_at=(
                datetime.fromisoformat(stage_data["completed_at"])
                if "completed_at" in stage_data
                else None
            ),
            output_path=(
                Path(stage_data["output_path"])
                if "output_path" in stage_data
                else None
            ),
            agent_outputs=agent_outputs,
        )
        stages[stage] = execution

    return PipelineState(config=config, stages=stages)
