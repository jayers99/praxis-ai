"""Subtype definitions and validation per domain.

Per opinions-contract.md section 5.2, each domain has valid subtypes.
"""

from __future__ import annotations

from praxis.domain.domains import Domain

# Valid subtypes by domain (from core/spec/domains.md and opinions-contract.md)
VALID_SUBTYPES: dict[Domain, list[str]] = {
    Domain.CODE: ["cli", "library", "api", "webapp", "infrastructure", "script"],
    Domain.CREATE: ["visual", "audio", "video", "interactive", "generative", "design"],
    Domain.WRITE: ["technical", "business", "narrative", "academic", "journalistic"],
    Domain.LEARN: ["skill", "concept", "practice", "course", "exploration"],
    Domain.OBSERVE: ["notes", "bookmarks", "clips", "logs", "captures"],
}


class SubtypeValidationError(ValueError):
    """Error raised when subtype validation fails."""

    def __init__(self, subtype: str, domain: Domain, valid_subtypes: list[str]) -> None:
        self.subtype = subtype
        self.domain = domain
        self.valid_subtypes = valid_subtypes
        valid_list = ", ".join(valid_subtypes)
        super().__init__(
            f"Invalid subtype '{subtype}' for domain '{domain.value}'. "
            f"Valid subtypes: {valid_list}"
        )


def validate_subtype_for_domain(subtype: str, domain: Domain) -> None:
    """Validate that a subtype is valid for a given domain.

    Args:
        subtype: The subtype to validate (e.g., "cli", "api")
        domain: The domain to validate against

    Raises:
        SubtypeValidationError: If subtype is invalid for the domain
    """
    valid = VALID_SUBTYPES.get(domain, [])

    # Handle nested subtypes (e.g., "cli-python" → base is "cli")
    base_subtype = subtype.replace(".", "-").split("-")[0]

    if base_subtype not in valid:
        raise SubtypeValidationError(subtype, domain, valid)


def get_valid_subtypes(domain: Domain) -> list[str]:
    """Get valid subtypes for a domain.

    Args:
        domain: The domain

    Returns:
        List of valid subtype names
    """
    return VALID_SUBTYPES.get(domain, [])
