"""Research session application service.

Orchestrates research session operations: init, status, run, approve, reject.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from praxis.domain.research_session import (
    ResearchPhase,
    SessionStatus,
)
from praxis.infrastructure.research_session_repo import (
    create_session,
    load_session,
    save_session,
)


@dataclass
class ResearchInitResult:
    """Result of initializing a research session."""

    success: bool
    session_id: str | None = None
    phase: str | None = None
    errors: list[str] = field(default_factory=list)


@dataclass
class ResearchStatusResult:
    """Result of getting research session status."""

    success: bool
    session_id: str | None = None
    topic: str | None = None
    phase: str | None = None
    phase_index: int = 0
    phase_count: int = 0
    tier: int = 0
    status: str | None = None
    corpus_path: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    phase_history: list[dict[str, str]] = field(default_factory=list)
    artifact_path: str | None = None
    errors: list[str] = field(default_factory=list)


@dataclass
class ResearchRunResult:
    """Result of running the next research phase."""

    success: bool
    previous_phase: str | None = None
    current_phase: str | None = None
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class ResearchApproveResult:
    """Result of approving research."""

    success: bool
    session_id: str | None = None
    artifact_path: str | None = None
    cataloged: bool = False
    errors: list[str] = field(default_factory=list)


@dataclass
class ResearchRejectResult:
    """Result of rejecting research."""

    success: bool
    session_id: str | None = None
    archived: bool = False
    errors: list[str] = field(default_factory=list)


def init_research(
    working_dir: Path,
    topic: str,
    corpus_path: Path,
    tier: int = 2,
    force: bool = False,
) -> ResearchInitResult:
    """Initialize a new research session.

    Args:
        working_dir: Directory to create session in.
        topic: Research topic.
        corpus_path: Path to source corpus.
        tier: Risk tier (0-3).
        force: If True, overwrite existing session.

    Returns:
        ResearchInitResult with outcome.
    """
    # Validate inputs
    if not topic or not topic.strip():
        return ResearchInitResult(
            success=False,
            errors=["--topic is required"],
        )

    # Create session
    result = create_session(
        working_dir=working_dir,
        topic=topic.strip(),
        corpus_path=corpus_path.resolve(),
        tier=tier,
        force=force,
    )

    if not result.success:
        return ResearchInitResult(
            success=False,
            errors=result.errors,
        )

    session = result.session
    assert session is not None

    return ResearchInitResult(
        success=True,
        session_id=session.id,
        phase=session.phase.value,
    )


def get_research_status(working_dir: Path) -> ResearchStatusResult:
    """Get the status of the current research session.

    Args:
        working_dir: Directory containing session.yaml.

    Returns:
        ResearchStatusResult with session details.
    """
    result = load_session(working_dir)

    if not result.success:
        return ResearchStatusResult(
            success=False,
            errors=result.errors,
        )

    session = result.session
    assert session is not None

    return ResearchStatusResult(
        success=True,
        session_id=session.id,
        topic=session.topic,
        phase=session.phase.value,
        phase_index=ResearchPhase.phase_index(session.phase),
        phase_count=ResearchPhase.phase_count(),
        tier=session.tier,
        status=session.status.value,
        corpus_path=str(session.corpus_path),
        created_at=session.created_at,
        updated_at=session.updated_at,
        phase_history=session.phase_history,
        artifact_path=str(session.artifact_path) if session.artifact_path else None,
    )


def run_research_phase(working_dir: Path) -> ResearchRunResult:
    """Advance to the next research phase.

    Args:
        working_dir: Directory containing session.yaml.

    Returns:
        ResearchRunResult with outcome.
    """
    result = load_session(working_dir)

    if not result.success:
        return ResearchRunResult(
            success=False,
            errors=result.errors,
        )

    session = result.session
    assert session is not None

    # Check if session is active
    if session.status != SessionStatus.ACTIVE:
        return ResearchRunResult(
            success=False,
            errors=[f"Session is not active (status: {session.status.value})"],
        )

    # Check if we can advance
    if not session.can_advance():
        return ResearchRunResult(
            success=False,
            errors=[f"Cannot advance from {session.phase.value} phase"],
        )

    previous_phase = session.phase.value
    new_phase = session.advance_phase()

    if new_phase is None:
        return ResearchRunResult(
            success=False,
            errors=["Failed to advance phase"],
        )

    # Save updated session
    save_result = save_session(working_dir, session)
    if not save_result.success:
        return ResearchRunResult(
            success=False,
            errors=save_result.errors,
        )

    # Build result with phase guidance
    run_result = ResearchRunResult(
        success=True,
        previous_phase=previous_phase,
        current_phase=new_phase.value,
    )

    # Add phase-specific guidance as warnings (informational)
    phase_guidance = {
        ResearchPhase.RTC: "Begin reading the corpus and gathering sources.",
        ResearchPhase.IDAS: "Identify, Describe, Analyze, and Synthesize findings.",
        ResearchPhase.SAD: "Draft the structured artifact.",
        ResearchPhase.CCR: "Perform cross-check review.",
        ResearchPhase.ASR: "Complete artifact structured review.",
        ResearchPhase.SYNTHESIS: "Ready for final synthesis and approval.",
    }

    guidance = phase_guidance.get(new_phase)
    if guidance:
        run_result.warnings.append(guidance)

    return run_result


def approve_research(
    working_dir: Path,
    rationale: str,
    library_path: Path | None = None,
) -> ResearchApproveResult:
    """Approve completed research and catalog to library.

    Args:
        working_dir: Directory containing session.yaml.
        rationale: Rationale for approval.
        library_path: Path to research library (optional, for cataloging).

    Returns:
        ResearchApproveResult with outcome.
    """
    if not rationale or not rationale.strip():
        return ResearchApproveResult(
            success=False,
            errors=["--rationale is required"],
        )

    result = load_session(working_dir)

    if not result.success:
        return ResearchApproveResult(
            success=False,
            errors=result.errors,
        )

    session = result.session
    assert session is not None

    # Check if at synthesis phase
    if session.phase != ResearchPhase.SYNTHESIS:
        return ResearchApproveResult(
            success=False,
            errors=[
                f"Session must be at synthesis phase to approve "
                f"(current phase: {session.phase.value})"
            ],
        )

    # Approve the session
    if not session.approve(rationale.strip()):
        return ResearchApproveResult(
            success=False,
            errors=["Failed to approve session"],
        )

    # Save updated session
    save_result = save_session(working_dir, session)
    if not save_result.success:
        return ResearchApproveResult(
            success=False,
            errors=save_result.errors,
        )

    # Note: Cataloging integration would happen here if library_path is provided
    # For MVP, we mark as approved but cataloging is a separate step

    return ResearchApproveResult(
        success=True,
        session_id=session.id,
        artifact_path=str(session.artifact_path) if session.artifact_path else None,
        cataloged=False,  # Cataloging is a separate step for MVP
    )


def reject_research(working_dir: Path, rationale: str) -> ResearchRejectResult:
    """Reject a research session and archive as draft.

    Args:
        working_dir: Directory containing session.yaml.
        rationale: Rationale for rejection.

    Returns:
        ResearchRejectResult with outcome.
    """
    if not rationale or not rationale.strip():
        return ResearchRejectResult(
            success=False,
            errors=["--rationale is required"],
        )

    result = load_session(working_dir)

    if not result.success:
        return ResearchRejectResult(
            success=False,
            errors=result.errors,
        )

    session = result.session
    assert session is not None

    # Check if session is active
    if session.status != SessionStatus.ACTIVE:
        return ResearchRejectResult(
            success=False,
            errors=[f"Session is not active (status: {session.status.value})"],
        )

    # Reject the session
    if not session.reject(rationale.strip()):
        return ResearchRejectResult(
            success=False,
            errors=["Failed to reject session"],
        )

    # Save updated session
    save_result = save_session(working_dir, session)
    if not save_result.success:
        return ResearchRejectResult(
            success=False,
            errors=save_result.errors,
        )

    return ResearchRejectResult(
        success=True,
        session_id=session.id,
        archived=True,
    )
