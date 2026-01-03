"""Stage definitions and regression rules."""

from __future__ import annotations

from enum import Enum


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
