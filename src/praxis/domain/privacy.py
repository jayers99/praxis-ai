"""Privacy level definitions."""

from __future__ import annotations

from enum import Enum


class PrivacyLevel(str, Enum):
    """Privacy levels from least to most restrictive."""

    PUBLIC = "public"
    PUBLIC_TRUSTED = "public-trusted"
    PERSONAL = "personal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

    def __lt__(self, other: object) -> bool:
        """Compare privacy levels by restrictiveness."""
        if not isinstance(other, PrivacyLevel):
            return NotImplemented
        order = list(PrivacyLevel)
        return order.index(self) < order.index(other)

    def __le__(self, other: object) -> bool:
        """Compare privacy levels by restrictiveness."""
        if not isinstance(other, PrivacyLevel):
            return NotImplemented
        return self == other or self < other

    def __gt__(self, other: object) -> bool:
        """Compare privacy levels by restrictiveness."""
        if not isinstance(other, PrivacyLevel):
            return NotImplemented
        order = list(PrivacyLevel)
        return order.index(self) > order.index(other)

    def __ge__(self, other: object) -> bool:
        """Compare privacy levels by restrictiveness."""
        if not isinstance(other, PrivacyLevel):
            return NotImplemented
        return self == other or self > other
