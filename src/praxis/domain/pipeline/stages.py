"""Pipeline stage definitions for the Praxis Knowledge Distillation Pipeline."""

from __future__ import annotations

from enum import Enum


class PipelineStage(str, Enum):
    """
    PKDP stages in canonical order.

    RTC → IDAS → SAD → CCR → ASR → HVA

    Each stage progressively increases signal, clarity, and epistemic confidence.
    """

    RTC = "rtc"  # Raw Thought Capture
    IDAS = "idas"  # Inquiry-Driven Analytical Synthesis
    SAD = "sad"  # Specialist Agent Dispatch
    CCR = "ccr"  # Critical Challenge Review
    ASR = "asr"  # Adjudicated Synthesis & Resolution
    HVA = "hva"  # Human Validation & Acceptance

    def __lt__(self, other: object) -> bool:
        """Compare stages by pipeline order."""
        if not isinstance(other, PipelineStage):
            return NotImplemented
        order = list(PipelineStage)
        return order.index(self) < order.index(other)

    def __le__(self, other: object) -> bool:
        """Compare stages by pipeline order."""
        if not isinstance(other, PipelineStage):
            return NotImplemented
        return self == other or self < other

    def __gt__(self, other: object) -> bool:
        """Compare stages by pipeline order."""
        if not isinstance(other, PipelineStage):
            return NotImplemented
        order = list(PipelineStage)
        return order.index(self) > order.index(other)

    def __ge__(self, other: object) -> bool:
        """Compare stages by pipeline order."""
        if not isinstance(other, PipelineStage):
            return NotImplemented
        return self == other or self > other

    def next_stage(self) -> PipelineStage | None:
        """Return the next stage in the pipeline, or None if at HVA."""
        order = list(PipelineStage)
        idx = order.index(self)
        if idx + 1 < len(order):
            return order[idx + 1]
        return None

    def previous_stage(self) -> PipelineStage | None:
        """Return the previous stage in the pipeline, or None if at RTC."""
        order = list(PipelineStage)
        idx = order.index(self)
        if idx > 0:
            return order[idx - 1]
        return None

    @property
    def full_name(self) -> str:
        """Return the full descriptive name of the stage."""
        names = {
            PipelineStage.RTC: "Raw Thought Capture",
            PipelineStage.IDAS: "Inquiry-Driven Analytical Synthesis",
            PipelineStage.SAD: "Specialist Agent Dispatch",
            PipelineStage.CCR: "Critical Challenge Review",
            PipelineStage.ASR: "Adjudicated Synthesis & Resolution",
            PipelineStage.HVA: "Human Validation & Acceptance",
        }
        return names[self]
