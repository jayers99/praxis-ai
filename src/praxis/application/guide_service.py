"""Application service for guide content retrieval."""

from __future__ import annotations

from pathlib import Path

from praxis.infrastructure.guide_loader import (
    load_domain_guide,
    load_lifecycle_guide,
    load_privacy_guide,
)


def get_lifecycle_guide(framework_root: Path | None = None) -> str:
    """Get lifecycle guide content.

    Args:
        framework_root: Optional framework root path.
            If None, uses current file location.

    Returns:
        Formatted guide text for terminal display

    Raises:
        FileNotFoundError: If lifecycle.md does not exist
    """
    if framework_root is None:
        # Calculate framework root from this file's location
        # This file is at: src/praxis/application/guide_service.py
        # Framework root is 3 levels up
        framework_root = Path(__file__).parent.parent.parent.parent

    spec_root = framework_root / "core" / "spec"
    return load_lifecycle_guide(spec_root)


def get_privacy_guide(framework_root: Path | None = None) -> str:
    """Get privacy guide content.

    Args:
        framework_root: Optional framework root path.
            If None, uses current file location.

    Returns:
        Formatted guide text for terminal display

    Raises:
        FileNotFoundError: If privacy.md does not exist
    """
    if framework_root is None:
        framework_root = Path(__file__).parent.parent.parent.parent

    spec_root = framework_root / "core" / "spec"
    return load_privacy_guide(spec_root)


def get_domain_guide(domain: str, framework_root: Path | None = None) -> str:
    """Get domain-specific guide content.

    Args:
        domain: Domain name (code, create, write, learn, observe)
        framework_root: Optional framework root path.
            If None, uses current file location.

    Returns:
        Formatted guide text for terminal display

    Raises:
        FileNotFoundError: If domains.md does not exist
        ValueError: If domain is unknown
    """
    if framework_root is None:
        framework_root = Path(__file__).parent.parent.parent.parent

    spec_root = framework_root / "core" / "spec"
    return load_domain_guide(spec_root, domain)
