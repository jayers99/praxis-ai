"""Pydantic models for the Praxis Knowledge Distillation Pipeline."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from praxis.domain.pipeline.risk_tiers import RiskTier
from praxis.domain.pipeline.stages import PipelineStage


class AgentOutput(BaseModel):
    """Output from a single agent invocation."""

    agent_type: str  # e.g., "architect", "security", "operations"
    output_path: Path
    timestamp: datetime


class StageExecution(BaseModel):
    """Execution state for a single pipeline stage."""

    stage: PipelineStage
    status: Literal["pending", "in_progress", "completed", "skipped"]
    started_at: datetime | None = None
    completed_at: datetime | None = None
    output_path: Path | None = None
    agent_outputs: list[AgentOutput] = Field(default_factory=list)


class PipelineConfig(BaseModel):
    """Configuration for a pipeline run."""

    pipeline_id: str
    risk_tier: RiskTier
    current_stage: PipelineStage
    started_at: datetime
    source_corpus_path: Path  # RTC input location
    prior_run_id: str | None = None  # Reference to prior pipeline run (for reruns)
    rerun_reason: str | None = None  # Reason for rerun (changed assumptions, etc.)
    search_query: str | None = None  # Query used for library precheck


class PipelineState(BaseModel):
    """Complete state of a pipeline run."""

    config: PipelineConfig
    stages: dict[PipelineStage, StageExecution] = Field(default_factory=dict)

    def get_stage_status(self, stage: PipelineStage) -> str:
        """Get the status of a specific stage."""
        if stage in self.stages:
            return self.stages[stage].status
        return "pending"

    def is_stage_completed(self, stage: PipelineStage) -> bool:
        """Check if a stage is completed."""
        return self.get_stage_status(stage) == "completed"

    def get_completed_stages(self) -> list[PipelineStage]:
        """Return list of completed stages in order."""
        completed = []
        for stage in PipelineStage:
            if self.is_stage_completed(stage):
                completed.append(stage)
        return completed


class PipelineStageResult(BaseModel):
    """Result of executing a single pipeline stage."""

    success: bool
    stage: PipelineStage
    output_path: Path | None = None
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    next_stage: PipelineStage | None = None


class PipelineInitResult(BaseModel):
    """Result of initializing a new pipeline."""

    success: bool
    pipeline_id: str | None = None
    risk_tier: RiskTier | None = None
    required_stages: list[PipelineStage] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    precheck_matches: list[dict[str, str | float]] = Field(
        default_factory=list
    )  # Library precheck results


class StageProgress(BaseModel):
    """Progress information for a single stage."""

    stage: PipelineStage
    required: bool
    status: str
    output_exists: bool


class PipelineStatus(BaseModel):
    """Current status of a pipeline."""

    pipeline_id: str | None = None
    risk_tier: RiskTier | None = None
    current_stage: PipelineStage | None = None
    stage_progress: list[StageProgress] = Field(default_factory=list)
    next_stage: PipelineStage | None = None
    is_complete: bool = False
    awaiting_hva: bool = False
    errors: list[str] = Field(default_factory=list)


class HVADecision(BaseModel):
    """Human Validation & Acceptance decision."""

    decision: Literal["accept", "refine", "reject"]
    rationale: str
    refine_to_stage: PipelineStage | None = None  # If decision is "refine"
    decided_at: datetime
