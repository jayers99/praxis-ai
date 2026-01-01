"""Specialist types and domain mappings for SAD stage."""

from __future__ import annotations

from enum import Enum

from praxis.domain.domains import Domain


class SpecialistType(str, Enum):
    """Types of specialist agents for SAD stage."""

    ARCHITECT = "architect"
    SECURITY = "security"
    OPERATIONS = "operations"
    TESTING = "testing"
    PERFORMANCE = "performance"
    DOMAIN_EXPERT = "domain_expert"
    RESEARCHER = "researcher"

    @property
    def description(self) -> str:
        """Return human-readable description of the specialist."""
        descriptions = {
            SpecialistType.ARCHITECT: "System and software architecture",
            SpecialistType.SECURITY: "Security analysis and threat modeling",
            SpecialistType.OPERATIONS: "Operations and infrastructure",
            SpecialistType.TESTING: "Testing strategy and quality assurance",
            SpecialistType.PERFORMANCE: "Performance optimization",
            SpecialistType.DOMAIN_EXPERT: "Domain-specific expertise",
            SpecialistType.RESEARCHER: "Research and literature review",
        }
        return descriptions[self]


# Default specialists per domain
DOMAIN_SPECIALISTS: dict[Domain, list[SpecialistType]] = {
    Domain.CODE: [
        SpecialistType.ARCHITECT,
        SpecialistType.SECURITY,
        SpecialistType.TESTING,
        SpecialistType.OPERATIONS,
    ],
    Domain.CREATE: [
        SpecialistType.DOMAIN_EXPERT,
        SpecialistType.RESEARCHER,
    ],
    Domain.WRITE: [
        SpecialistType.DOMAIN_EXPERT,
        SpecialistType.RESEARCHER,
    ],
    Domain.LEARN: [
        SpecialistType.DOMAIN_EXPERT,
        SpecialistType.RESEARCHER,
    ],
    Domain.OBSERVE: [
        SpecialistType.RESEARCHER,
    ],
}


def get_specialists_for_domain(domain: Domain) -> list[SpecialistType]:
    """Return recommended specialists for a domain."""
    return DOMAIN_SPECIALISTS.get(domain, [SpecialistType.RESEARCHER])
