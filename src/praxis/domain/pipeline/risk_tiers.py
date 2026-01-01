"""Risk tier definitions for the Praxis Knowledge Distillation Pipeline."""

from __future__ import annotations

from enum import IntEnum

from praxis.domain.pipeline.stages import PipelineStage


class RiskTier(IntEnum):
    """
    Risk tiers govern validation depth, not decision authority.

    Higher tiers require more pipeline stages for thorough validation.
    """

    TIER_0 = 0  # Disposable / Personal Notes
    TIER_1 = 1  # Informational Knowledge
    TIER_2 = 2  # Strategic Knowledge
    TIER_3 = 3  # Foundational / Long-Lived Knowledge

    @property
    def description(self) -> str:
        """Return human-readable description of the tier."""
        descriptions = {
            RiskTier.TIER_0: "Disposable / Personal Notes",
            RiskTier.TIER_1: "Informational Knowledge",
            RiskTier.TIER_2: "Strategic Knowledge",
            RiskTier.TIER_3: "Foundational / Long-Lived Knowledge",
        }
        return descriptions[self]


# Required stages per risk tier (from handoff document)
# Skipping stages without explicit tier justification is a pipeline violation.
REQUIRED_STAGES: dict[RiskTier, list[PipelineStage]] = {
    # Tier 0: Lightweight Distillation
    RiskTier.TIER_0: [
        PipelineStage.RTC,
        PipelineStage.IDAS,
    ],
    # Tier 1: Standard Knowledge Entry (skip CCR)
    RiskTier.TIER_1: [
        PipelineStage.RTC,
        PipelineStage.IDAS,
        PipelineStage.SAD,
        PipelineStage.ASR,
    ],
    # Tier 2: Strategic Knowledge (full except HVA)
    RiskTier.TIER_2: [
        PipelineStage.RTC,
        PipelineStage.IDAS,
        PipelineStage.SAD,
        PipelineStage.CCR,
        PipelineStage.ASR,
    ],
    # Tier 3: Foundational Knowledge (all stages mandatory)
    RiskTier.TIER_3: [
        PipelineStage.RTC,
        PipelineStage.IDAS,
        PipelineStage.SAD,
        PipelineStage.CCR,
        PipelineStage.ASR,
        PipelineStage.HVA,
    ],
}


def is_stage_required(tier: RiskTier, stage: PipelineStage) -> bool:
    """Check if a stage is required for the given risk tier."""
    return stage in REQUIRED_STAGES[tier]


def get_next_required_stage(
    tier: RiskTier,
    current_stage: PipelineStage | None,
) -> PipelineStage | None:
    """
    Get the next required stage for the tier after the current stage.

    Returns None if all required stages are complete.
    """
    required = REQUIRED_STAGES[tier]
    if current_stage is None:
        return required[0] if required else None

    try:
        idx = required.index(current_stage)
        if idx + 1 < len(required):
            return required[idx + 1]
        return None
    except ValueError:
        # Current stage not in required list, return first required stage after it
        for stage in required:
            if stage > current_stage:
                return stage
        return None
