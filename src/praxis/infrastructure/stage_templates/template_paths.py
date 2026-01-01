"""Template path computation and validation helpers."""

from __future__ import annotations

import re
from pathlib import Path

from praxis.domain.domains import Domain
from praxis.domain.stages import Stage

_SUBTYPE_PATTERN = re.compile(r"^[a-z0-9-]+$")
_ARTIFACT_PATTERN = re.compile(r"^[a-z0-9-]+$")


def validate_subtype(subtype: str) -> None:
    if not _SUBTYPE_PATTERN.match(subtype):
        raise ValueError(
            "Invalid subtype. Use lowercase letters, numbers, and dashes only."
        )


def validate_artifact_name(artifact_name: str) -> None:
    if not _ARTIFACT_PATTERN.match(artifact_name):
        raise ValueError(
            "Invalid artifact name. Use lowercase letters, numbers, and dashes only."
        )


def stage_template_candidates(
    domain: Domain, stage: Stage, subtype: str | None
) -> list[str]:
    candidates: list[str] = []
    if subtype:
        validate_subtype(subtype)
        candidates.append(
            f"domain/{domain.value}/subtype/{subtype}/stage/{stage.value}.md"
        )
    candidates.append(f"domain/{domain.value}/stage/{stage.value}.md")
    candidates.append(f"stage/{stage.value}.md")
    return candidates


def artifact_template_candidates(
    domain: Domain,
    artifact_name: str,
    subtype: str | None,
) -> list[str]:
    candidates: list[str] = []
    validate_artifact_name(artifact_name)
    if subtype:
        validate_subtype(subtype)
        candidates.append(
            f"domain/{domain.value}/subtype/{subtype}/artifact/{artifact_name}.md"
        )
    candidates.append(f"domain/{domain.value}/artifact/{artifact_name}.md")
    return candidates


def ensure_within_root(root: Path, path: Path) -> None:
    """Ensure a resolved path stays within its root directory."""

    root_resolved = root.resolve()
    path_resolved = path.resolve()

    try:
        path_resolved.relative_to(root_resolved)
    except ValueError as e:
        raise ValueError("Resolved path escapes template root") from e
