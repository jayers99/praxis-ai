"""Infrastructure for loading guide content from spec files."""

from __future__ import annotations

from pathlib import Path


def load_lifecycle_guide(spec_root: Path) -> str:
    """Load lifecycle guide content from lifecycle.md.

    Args:
        spec_root: Path to core/spec directory

    Returns:
        Formatted guide text for terminal display

    Raises:
        FileNotFoundError: If lifecycle.md does not exist
    """
    lifecycle_path = spec_root / "lifecycle.md"

    if not lifecycle_path.exists():
        raise FileNotFoundError(f"Spec file not found: {lifecycle_path}")

    # Extract key sections
    output_lines = []
    output_lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    output_lines.append("PRAXIS LIFECYCLE")
    output_lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    output_lines.append("")

    # Add lifecycle stages (extracted from section headers)
    output_lines.append("Nine stages organize all work:")
    output_lines.append("")
    output_lines.append("  1. Capture    → Collect raw inputs with minimal friction")
    output_lines.append("  2. Sense      → Convert inputs into understanding")
    output_lines.append("  3. Explore    → Generate possibilities without obligation")
    output_lines.append("  4. Shape      → Converge toward a viable direction")
    # noqa: E501 - Keep user-visible strings readable
    output_lines.append("  5. Formalize  → Convert thinking into durable artifacts (HINGE)")
    output_lines.append("  6. Commit     → Explicitly decide to proceed")
    output_lines.append("  7. Execute    → Produce the artifact")
    output_lines.append("  8. Sustain    → Maintain and govern delivered work")
    output_lines.append("  9. Close      → End work intentionally, capture leverage")
    output_lines.append("")

    # Add Formalize hinge concept
    output_lines.append("━━━ Formalize: The Structural Hinge ━━━")
    output_lines.append("")
    output_lines.append("Formalize is the boundary between exploration and execution.")
    # noqa: E501 - Keep user-visible strings readable
    output_lines.append("It's where thinking becomes durable, policy-bearing artifacts.")
    output_lines.append("")
    output_lines.append("Before Formalize: Discovery iteration (what is this?)")
    output_lines.append("After Formalize:  Refinement iteration (how good can it be?)")
    output_lines.append("")
    output_lines.append("Critical Rule: No execution without formalization artifacts.")
    output_lines.append("")

    # Add allowed regressions
    output_lines.append("━━━ Allowed Stage Regressions ━━━")
    output_lines.append("")
    output_lines.append("  Execute → Commit, Formalize")
    output_lines.append("  Sustain → Execute, Commit")
    output_lines.append("  Close   → Capture (seed new work)")
    output_lines.append("")

    # Add reference to full doc
    output_lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    output_lines.append("For full details: core/spec/lifecycle.md")
    output_lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    return "\n".join(output_lines)


def load_privacy_guide(spec_root: Path) -> str:
    """Load privacy guide content from privacy.md.

    Args:
        spec_root: Path to core/spec directory

    Returns:
        Formatted guide text for terminal display

    Raises:
        FileNotFoundError: If privacy.md does not exist
    """
    privacy_path = spec_root / "privacy.md"

    if not privacy_path.exists():
        raise FileNotFoundError(f"Spec file not found: {privacy_path}")

    output_lines = []
    output_lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    output_lines.append("PRAXIS PRIVACY MODEL")
    output_lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    output_lines.append("")
    output_lines.append("Five privacy levels (least to most restrictive):")
    output_lines.append("")

    # Privacy levels with brief descriptions
    output_lines.append("  1. Public")
    # noqa: E501 - Keep user-visible strings readable
    output_lines.append("     Safe for unrestricted publication and broad collaboration")
    output_lines.append("")

    output_lines.append("  2. Public – Trusted Collaborators")
    # noqa: E501 - Keep user-visible strings readable
    output_lines.append("     Broadly shareable but collaboration intentionally limited")
    output_lines.append("")

    output_lines.append("  3. Personal")
    # noqa: E501 - Keep user-visible strings readable
    output_lines.append("     Private to author or trusted collaborators; " "low-to-moderate sensitivity")
    output_lines.append("")

    output_lines.append("  4. Confidential")
    # noqa: E501 - Keep user-visible strings readable
    output_lines.append("     Sensitive material requiring deliberate containment and abstraction")
    output_lines.append("")

    output_lines.append("  5. Restricted")
    # noqa: E501 - Keep user-visible strings readable
    output_lines.append("     Single-custodian, maximum secrecy; exposure minimized by design")
    output_lines.append("")

    output_lines.append("━━━ Behavioral Constraints ━━━")
    output_lines.append("")
    output_lines.append("Privacy level controls:")
    output_lines.append("  • Storage (repos, cloud)")
    output_lines.append("  • AI tool usage")
    output_lines.append("  • Artifact specificity")
    output_lines.append("  • Collaboration scope")
    output_lines.append("")

    output_lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    output_lines.append("For full details: core/spec/privacy.md")
    output_lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    return "\n".join(output_lines)


def load_domain_guide(spec_root: Path, domain: str) -> str:
    """Load domain-specific guide content from domains.md.

    Args:
        spec_root: Path to core/spec directory
        domain: Domain name (code, create, write, learn, observe)

    Returns:
        Formatted guide text for terminal display

    Raises:
        FileNotFoundError: If domains.md does not exist
        ValueError: If domain is unknown
    """
    domains_path = spec_root / "domains.md"

    if not domains_path.exists():
        raise FileNotFoundError(f"Spec file not found: {domains_path}")

    # Domain-specific content
    domain_info = {
        "code": {
            "intent": "Functional systems and tools",
            "artifact": "docs/sod.md",
            "artifact_name": "Solution Overview Document (SOD)",
            "subtypes": ["cli", "library", "api", "webapp", "infrastructure", "script"],
        },
        "create": {
            "intent": "Aesthetic and expressive output (any medium)",
            "artifact": "docs/brief.md",
            "artifact_name": "Creative Brief",
            # noqa: E501 - Keep domain info readable
            "subtypes": [
                "visual",
                "audio",
                "video",
                "interactive",
                "generative",
                "design",
            ],
        },
        "write": {
            "intent": "Structured thought and communication",
            "artifact": "docs/brief.md",
            "artifact_name": "Writing Brief",
            # noqa: E501 - Keep domain info readable
            "subtypes": [
                "technical",
                "business",
                "narrative",
                "academic",
                "journalistic",
            ],
        },
        "learn": {
            "intent": "Skill formation and knowledge acquisition",
            "artifact": "docs/plan.md",
            "artifact_name": "Learning Plan",
            "subtypes": ["skill", "concept", "practice", "course", "exploration"],
        },
        "observe": {
            "intent": "Raw capture and collection",
            "artifact": "(none required)",
            "artifact_name": "No formalize artifact",
            "subtypes": ["notes", "bookmarks", "clips", "logs", "captures"],
        },
    }

    if domain not in domain_info:
        valid_domains = ", ".join(domain_info.keys())
        raise ValueError(f"Unknown domain: {domain}. Valid: {valid_domains}")

    info = domain_info[domain]

    output_lines = []
    output_lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    output_lines.append(f"PRAXIS DOMAIN: {domain.upper()}")
    output_lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    output_lines.append("")
    output_lines.append(f"Purpose: {info['intent']}")
    output_lines.append("")

    output_lines.append("━━━ Formalize Artifact ━━━")
    output_lines.append("")
    output_lines.append(f"  {info['artifact_name']}")
    output_lines.append(f"  Location: {info['artifact']}")
    output_lines.append("")

    if info["subtypes"]:
        output_lines.append("━━━ Subtypes ━━━")
        output_lines.append("")
        for subtype in info["subtypes"]:
            output_lines.append(f"  • {domain}.{subtype}")
        output_lines.append("")

    output_lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    output_lines.append("For full details: core/spec/domains.md")
    output_lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    return "\n".join(output_lines)
