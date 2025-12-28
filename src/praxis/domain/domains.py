"""Domain definitions and artifact path mappings."""

from __future__ import annotations

from enum import Enum
from pathlib import Path


class Domain(str, Enum):
    """Praxis project domains."""

    CODE = "code"
    CREATE = "create"
    WRITE = "write"
    OBSERVE = "observe"
    LEARN = "learn"


# Artifact path conventions (from ADR-002)
ARTIFACT_PATHS: dict[Domain, Path | None] = {
    Domain.CODE: Path("docs/sod.md"),
    Domain.CREATE: Path("docs/brief.md"),
    Domain.WRITE: Path("docs/brief.md"),
    Domain.LEARN: Path("docs/plan.md"),
    Domain.OBSERVE: None,  # Observe domain has no required artifact
}
