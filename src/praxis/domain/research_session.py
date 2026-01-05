"""Domain models for research sessions.

This module defines the core domain entities for managing research sessions
that follow the research-runbook workflow phases.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path


class ResearchPhase(str, Enum):
    """Research session phases aligned with research-runbook.md.

    Phases progress in order:
    intake → rtc → idas → sad → ccr → asr → synthesis
    """

    INTAKE = "intake"  # Initial capture and topic definition
    RTC = "rtc"  # Read The Corpus - source gathering
    IDAS = "idas"  # Identify, Describe, Analyze, Synthesize
    SAD = "sad"  # Structured Artifact Draft
    CCR = "ccr"  # Cross-Check Review
    ASR = "asr"  # Artifact Structured Review
    SYNTHESIS = "synthesis"  # Final synthesis and approval

    @classmethod
    def next_phase(cls, current: "ResearchPhase") -> "ResearchPhase | None":
        """Get the next phase after the current one.

        Returns None if at the final phase (SYNTHESIS).
        """
        order = list(cls)
        current_idx = order.index(current)
        if current_idx < len(order) - 1:
            return order[current_idx + 1]
        return None

    @classmethod
    def phase_index(cls, phase: "ResearchPhase") -> int:
        """Get the 1-based index of a phase."""
        return list(cls).index(phase) + 1

    @classmethod
    def phase_count(cls) -> int:
        """Get total number of phases."""
        return len(list(cls))


class SessionStatus(str, Enum):
    """Research session status."""

    ACTIVE = "active"  # Session is in progress
    APPROVED = "approved"  # Session completed and approved
    REJECTED = "rejected"  # Session was rejected
    ARCHIVED = "archived"  # Session archived (rejected as draft)


@dataclass
class ResearchSession:
    """A research session tracking progress through phases.

    Attributes:
        id: Unique session identifier (auto-generated if not provided)
        topic: Research topic being investigated
        corpus_path: Path to the source corpus for RTC phase
        tier: Risk tier (0-3), higher tiers have stricter requirements
        phase: Current research phase
        status: Session status (active, approved, rejected, archived)
        created_at: When the session was created
        updated_at: When the session was last updated
        phase_history: List of phase transitions with timestamps
        artifact_path: Path to the generated artifact (set during synthesis)
        rationale: Approval/rejection rationale (set at completion)
    """

    id: str
    topic: str
    corpus_path: Path
    tier: int = 2  # Default to mid-level tier
    phase: ResearchPhase = ResearchPhase.INTAKE
    status: SessionStatus = SessionStatus.ACTIVE
    created_at: str = ""  # ISO format timestamp
    updated_at: str = ""  # ISO format timestamp
    phase_history: list[dict[str, str]] = field(default_factory=list)
    artifact_path: Path | None = None
    rationale: str | None = None

    def __post_init__(self) -> None:
        """Set default timestamps if not provided."""
        now = datetime.now().isoformat()
        if not self.created_at:
            self.created_at = now
        if not self.updated_at:
            self.updated_at = now

        # Record initial phase if history is empty
        if not self.phase_history:
            self.phase_history = [{"phase": self.phase.value, "timestamp": self.created_at}]

    def can_advance(self) -> bool:
        """Check if the session can advance to the next phase."""
        if self.status != SessionStatus.ACTIVE:
            return False
        return ResearchPhase.next_phase(self.phase) is not None

    def advance_phase(self) -> ResearchPhase | None:
        """Advance to the next phase if possible.

        Returns the new phase, or None if cannot advance.
        """
        if not self.can_advance():
            return None

        next_phase = ResearchPhase.next_phase(self.phase)
        if next_phase is None:
            return None

        self.phase = next_phase
        self.updated_at = datetime.now().isoformat()
        self.phase_history.append(
            {
                "phase": next_phase.value,
                "timestamp": self.updated_at,
            }
        )
        return next_phase

    def can_approve(self) -> bool:
        """Check if the session can be approved.

        Sessions can only be approved at the synthesis phase.
        """
        return self.status == SessionStatus.ACTIVE and self.phase == ResearchPhase.SYNTHESIS

    def approve(self, rationale: str) -> bool:
        """Approve the research session.

        Args:
            rationale: Reason for approval.

        Returns:
            True if approved successfully, False otherwise.
        """
        if not self.can_approve():
            return False

        self.status = SessionStatus.APPROVED
        self.rationale = rationale
        self.updated_at = datetime.now().isoformat()
        return True

    def reject(self, rationale: str) -> bool:
        """Reject the research session.

        Sessions can be rejected at any phase.

        Args:
            rationale: Reason for rejection.

        Returns:
            True if rejected successfully, False otherwise.
        """
        if self.status != SessionStatus.ACTIVE:
            return False

        self.status = SessionStatus.ARCHIVED
        self.rationale = rationale
        self.updated_at = datetime.now().isoformat()
        return True


@dataclass
class SessionResult:
    """Result of a session operation.

    Attributes:
        success: Whether the operation succeeded
        session: The session if successful
        errors: List of error messages if unsuccessful
    """

    success: bool
    session: ResearchSession | None = None
    errors: list[str] = field(default_factory=list)


def generate_session_id(topic: str) -> str:
    """Generate a unique session ID from topic and timestamp.

    Format: {topic-slug}-{YYYY-MM-DD-HHMMSS}
    """
    import re

    # Create slug from topic
    slug = topic.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")[:30]  # Limit length

    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")

    return f"{slug}-{timestamp}"
