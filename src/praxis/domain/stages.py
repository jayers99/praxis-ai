"""Stage definitions and regression rules."""

from __future__ import annotations

from enum import Enum
from typing import Literal


class Stage(str, Enum):
    """Praxis lifecycle stages in order."""

    CAPTURE = "capture"
    SENSE = "sense"
    EXPLORE = "explore"
    SHAPE = "shape"
    FORMALIZE = "formalize"
    COMMIT = "commit"
    EXECUTE = "execute"
    SUSTAIN = "sustain"
    CLOSE = "close"

    def __lt__(self, other: object) -> bool:
        """Compare stages by lifecycle order."""
        if not isinstance(other, Stage):
            return NotImplemented
        order = list(Stage)
        return order.index(self) < order.index(other)

    def __le__(self, other: object) -> bool:
        """Compare stages by lifecycle order."""
        if not isinstance(other, Stage):
            return NotImplemented
        return self == other or self < other

    def __gt__(self, other: object) -> bool:
        """Compare stages by lifecycle order."""
        if not isinstance(other, Stage):
            return NotImplemented
        order = list(Stage)
        return order.index(self) > order.index(other)

    def __ge__(self, other: object) -> bool:
        """Compare stages by lifecycle order."""
        if not isinstance(other, Stage):
            return NotImplemented
        return self == other or self > other


# Stages that require formalization artifacts (stage >= formalize)
REQUIRES_ARTIFACT: frozenset[Stage] = frozenset({
    Stage.FORMALIZE,
    Stage.COMMIT,
    Stage.EXECUTE,
    Stage.SUSTAIN,
    Stage.CLOSE,
})

# Allowed regression paths (from lifecycle.md lines 104-118)
ALLOWED_REGRESSIONS: dict[Stage, frozenset[Stage]] = {
    Stage.EXECUTE: frozenset({Stage.COMMIT, Stage.FORMALIZE}),
    Stage.SUSTAIN: frozenset({Stage.EXECUTE, Stage.COMMIT}),
    Stage.CLOSE: frozenset({Stage.CAPTURE}),
}

# Fast track: simplified 4-stage lifecycle for small tasks (in order)
FAST_TRACK_STAGES: tuple[Stage, ...] = (
    Stage.CAPTURE,
    Stage.FORMALIZE,
    Stage.EXECUTE,
    Stage.CLOSE,
)

# Full track: all 9 stages (in order)
FULL_TRACK_STAGES: tuple[Stage, ...] = tuple(Stage)


def get_allowed_stages(mode: Literal["full", "fast"]) -> tuple[Stage, ...]:
    """Get the allowed stages for a given lifecycle mode.

    Args:
        mode: Either "full" (all 9 stages) or "fast" (4 stages).

    Returns:
        Tuple of allowed stages for the mode in order.
    """
    if mode == "fast":
        return FAST_TRACK_STAGES
    return FULL_TRACK_STAGES


def is_stage_allowed(stage: Stage, mode: Literal["full", "fast"]) -> bool:
    """Check if a stage is allowed in the given lifecycle mode.

    Args:
        stage: The stage to check.
        mode: Either "full" or "fast".

    Returns:
        True if the stage is allowed in this mode.
    """
    return stage in get_allowed_stages(mode)


def get_next_stage(
    current: Stage, mode: Literal["full", "fast"]
) -> Stage | None:
    """Get the next stage in the lifecycle for the given mode.

    Args:
        current: Current stage.
        mode: Either "full" or "fast".

    Returns:
        Next stage in sequence, or None if at the end.
    """
    allowed = get_allowed_stages(mode)
    all_stages = list(Stage)

    # Find next stage that's in the allowed set
    current_idx = all_stages.index(current)
    for i in range(current_idx + 1, len(all_stages)):
        if all_stages[i] in allowed:
            return all_stages[i]
    return None
