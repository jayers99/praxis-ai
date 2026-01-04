"""Privacy guardrails for AI prompt exports."""

from __future__ import annotations

import re
from typing import NamedTuple

from praxis.domain.privacy import PrivacyLevel


class RedactionPattern(NamedTuple):
    """A pattern for redacting sensitive content."""

    name: str
    regex: re.Pattern[str]
    replacement_template: str = "[REDACTED:{name}]"


class PrivacyConstraint(NamedTuple):
    """Privacy constraint text for a given privacy level."""

    level: PrivacyLevel
    constraint_text: str
    warning_text: str


class PrivacyGuard:
    """Privacy guardrails for controlling AI prompt exports."""

    # Privacy constraints per privacy.md section 3
    CONSTRAINTS = [
        PrivacyConstraint(
            level=PrivacyLevel.PUBLIC,
            constraint_text="",
            warning_text="",
        ),
        PrivacyConstraint(
            level=PrivacyLevel.PUBLIC_TRUSTED,
            constraint_text="",
            warning_text="",
        ),
        PrivacyConstraint(
            level=PrivacyLevel.PERSONAL,
            constraint_text="No credentials, secrets, or regulated identifiers",
            warning_text=(
                "⚠️  Privacy Level: PERSONAL - "
                "Review exported content before sharing with AI"
            ),
        ),
        PrivacyConstraint(
            level=PrivacyLevel.CONFIDENTIAL,
            constraint_text=(
                "Redacted or abstracted inputs only; "
                "no raw logs, configs, or identifiers"
            ),
            warning_text=(
                "⚠️  Privacy Level: CONFIDENTIAL - "
                "Sensitive content detected. Use --redact or review carefully"
            ),
        ),
        PrivacyConstraint(
            level=PrivacyLevel.RESTRICTED,
            constraint_text=(
                "No external AI with raw content; "
                "abstract summaries only, never source material"
            ),
            warning_text=(
                "⚠️  Privacy Level: RESTRICTED - "
                "Maximum secrecy. Verify no sensitive content before AI use"
            ),
        ),
    ]

    # MVP redaction patterns (defense-in-depth, not security guarantee)
    REDACTION_PATTERNS = [
        RedactionPattern(
            name="API_KEY",
            regex=re.compile(
                r"(?i)(api[_-]?key|secret[_-]?key|auth[_-]?token)\s*[=:]\s*\S+"
            ),
        ),
        RedactionPattern(
            name="PASSWORD",
            regex=re.compile(
                r"(?i)(password|passwd|pwd)\s*[=:]\s*\S+"
            ),
        ),
        RedactionPattern(
            name="AWS_ACCESS_KEY",
            regex=re.compile(r"AKIA[0-9A-Z]{16}"),
        ),
        RedactionPattern(
            name="AWS_SECRET",
            regex=re.compile(
                r"(?i)(aws_secret_access_key|aws_secret)\s*[=:]\s*[A-Za-z0-9/+=]{40}"
            ),
        ),
        RedactionPattern(
            name="JWT",
            regex=re.compile(r"eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*"),
        ),
        RedactionPattern(
            name="PRIVATE_KEY",
            regex=re.compile(r"-----BEGIN.*PRIVATE KEY-----"),
        ),
    ]

    @classmethod
    def get_constraint(cls, level: PrivacyLevel) -> PrivacyConstraint:
        """Get privacy constraint for a given level.

        Args:
            level: Privacy level to get constraint for

        Returns:
            PrivacyConstraint with text and warning
        """
        for constraint in cls.CONSTRAINTS:
            if constraint.level == level:
                return constraint
        # Default to no constraint for unknown levels
        return PrivacyConstraint(level=level, constraint_text="", warning_text="")

    @classmethod
    def redact_content(cls, content: str) -> tuple[str, list[str]]:
        """Redact sensitive patterns from content.

        Args:
            content: Content to redact

        Returns:
            Tuple of (redacted_content, list of pattern names found)
        """
        redacted = content
        patterns_found: list[str] = []

        for pattern in cls.REDACTION_PATTERNS:
            matches = pattern.regex.findall(redacted)
            if matches:
                patterns_found.append(pattern.name)
                replacement = pattern.replacement_template.format(name=pattern.name)
                redacted = pattern.regex.sub(replacement, redacted)

        return redacted, patterns_found

    @classmethod
    def should_warn(cls, level: PrivacyLevel) -> bool:
        """Check if privacy level should trigger a warning.

        Args:
            level: Privacy level to check

        Returns:
            True if warnings should be shown
        """
        return level >= PrivacyLevel.PERSONAL
