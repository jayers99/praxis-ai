"""Research session persistence.

This module handles YAML persistence of research sessions via session.yaml files.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from praxis.domain.research_session import (
    ResearchPhase,
    ResearchSession,
    SessionResult,
    SessionStatus,
    generate_session_id,
)

# Session file name
SESSION_FILE = "session.yaml"


def _session_to_dict(session: ResearchSession) -> dict[str, Any]:
    """Convert a ResearchSession to a dictionary for YAML serialization."""
    data: dict[str, Any] = {
        "id": session.id,
        "topic": session.topic,
        "corpus_path": str(session.corpus_path),
        "tier": session.tier,
        "phase": session.phase.value,
        "status": session.status.value,
        "created_at": session.created_at,
        "updated_at": session.updated_at,
        "phase_history": session.phase_history,
    }

    if session.artifact_path is not None:
        data["artifact_path"] = str(session.artifact_path)

    if session.rationale is not None:
        data["rationale"] = session.rationale

    return data


def _dict_to_session(data: dict[str, Any]) -> ResearchSession:
    """Convert a dictionary to a ResearchSession."""
    session = ResearchSession(
        id=data["id"],
        topic=data["topic"],
        corpus_path=Path(data["corpus_path"]),
        tier=data.get("tier", 2),
        phase=ResearchPhase(data["phase"]),
        status=SessionStatus(data["status"]),
        created_at=data["created_at"],
        updated_at=data["updated_at"],
        phase_history=data.get("phase_history", []),
        artifact_path=(
            Path(data["artifact_path"]) if data.get("artifact_path") else None
        ),
        rationale=data.get("rationale"),
    )
    return session


def get_session_path(working_dir: Path) -> Path:
    """Get the path to session.yaml in the working directory."""
    return working_dir / SESSION_FILE


def session_exists(working_dir: Path) -> bool:
    """Check if a session exists in the working directory."""
    return get_session_path(working_dir).exists()


def load_session(working_dir: Path) -> SessionResult:
    """Load a research session from the working directory.

    Args:
        working_dir: Directory containing session.yaml.

    Returns:
        SessionResult with session if found, or error if not.
    """
    session_path = get_session_path(working_dir)

    if not session_path.exists():
        return SessionResult(
            success=False,
            errors=["No active research session found (session.yaml not found)"],
        )

    try:
        content = session_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)

        if not isinstance(data, dict):
            return SessionResult(
                success=False,
                errors=["Invalid session.yaml format"],
            )

        session = _dict_to_session(data)
        return SessionResult(success=True, session=session)

    except yaml.YAMLError as e:
        return SessionResult(
            success=False,
            errors=[f"Failed to parse session.yaml: {e}"],
        )
    except (KeyError, ValueError) as e:
        return SessionResult(
            success=False,
            errors=[f"Invalid session data: {e}"],
        )


def save_session(working_dir: Path, session: ResearchSession) -> SessionResult:
    """Save a research session to the working directory.

    Args:
        working_dir: Directory to save session.yaml.
        session: The session to save.

    Returns:
        SessionResult indicating success or failure.
    """
    session_path = get_session_path(working_dir)

    try:
        # Ensure directory exists
        working_dir.mkdir(parents=True, exist_ok=True)

        data = _session_to_dict(session)
        content = yaml.dump(data, default_flow_style=False, sort_keys=False)
        session_path.write_text(content, encoding="utf-8")

        return SessionResult(success=True, session=session)

    except Exception as e:
        return SessionResult(
            success=False,
            errors=[f"Failed to save session: {e}"],
        )


def create_session(
    working_dir: Path,
    topic: str,
    corpus_path: Path,
    tier: int = 2,
    force: bool = False,
) -> SessionResult:
    """Create a new research session.

    Args:
        working_dir: Directory to create session in.
        topic: Research topic.
        corpus_path: Path to source corpus.
        tier: Risk tier (0-3).
        force: If True, overwrite existing session.

    Returns:
        SessionResult with the new session or error.
    """
    # Check for existing session
    if session_exists(working_dir) and not force:
        return SessionResult(
            success=False,
            errors=["Active session already exists. Use --force to replace."],
        )

    # Validate corpus path
    if not corpus_path.exists():
        return SessionResult(
            success=False,
            errors=[f"Corpus path does not exist: {corpus_path}"],
        )

    # Validate tier
    if tier < 0 or tier > 3:
        return SessionResult(
            success=False,
            errors=[f"Invalid tier: {tier}. Must be 0-3."],
        )

    # Create session
    session_id = generate_session_id(topic)
    session = ResearchSession(
        id=session_id,
        topic=topic,
        corpus_path=corpus_path,
        tier=tier,
    )

    return save_session(working_dir, session)


def delete_session(working_dir: Path) -> SessionResult:
    """Delete the session file from the working directory.

    Args:
        working_dir: Directory containing session.yaml.

    Returns:
        SessionResult indicating success or failure.
    """
    session_path = get_session_path(working_dir)

    if not session_path.exists():
        return SessionResult(
            success=False,
            errors=["No session to delete"],
        )

    try:
        session_path.unlink()
        return SessionResult(success=True)
    except Exception as e:
        return SessionResult(
            success=False,
            errors=[f"Failed to delete session: {e}"],
        )
