"""Load extension and example registries from YAML files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from praxis.domain.domains import Domain
from praxis.domain.workspace import ExampleInfo, ExtensionInfo


def _parse_domain(domain_str: str) -> Domain:
    """Parse domain string to Domain enum."""
    try:
        return Domain(domain_str.lower())
    except ValueError:
        return Domain.CODE  # Default fallback


def load_extensions_registry(registry_path: Path) -> list[ExtensionInfo]:
    """Load extensions from extensions.yaml registry file.

    Args:
        registry_path: Path to extensions.yaml file

    Returns:
        List of ExtensionInfo objects

    Raises:
        FileNotFoundError: If registry file doesn't exist
        ValueError: If registry file is malformed
    """
    if not registry_path.exists():
        raise FileNotFoundError(f"Extensions registry not found: {registry_path}")

    with open(registry_path) as f:
        data = yaml.safe_load(f)

    if not data or "extensions" not in data:
        raise ValueError(f"Invalid extensions registry: {registry_path}")

    extensions: list[ExtensionInfo] = []
    ext_data: dict[str, Any] = data["extensions"]

    for name, info in ext_data.items():
        extensions.append(
            ExtensionInfo(
                name=name,
                repo=info.get("repo", ""),
                domain=_parse_domain(info.get("domain", "code")),
                description=info.get("description", ""),
                installed=False,
            )
        )

    return extensions


def load_examples_registry(registry_path: Path) -> list[ExampleInfo]:
    """Load examples from examples.yaml registry file.

    Args:
        registry_path: Path to examples.yaml file

    Returns:
        List of ExampleInfo objects

    Raises:
        FileNotFoundError: If registry file doesn't exist
        ValueError: If registry file is malformed
    """
    if not registry_path.exists():
        raise FileNotFoundError(f"Examples registry not found: {registry_path}")

    with open(registry_path) as f:
        data = yaml.safe_load(f)

    if not data or "examples" not in data:
        raise ValueError(f"Invalid examples registry: {registry_path}")

    examples: list[ExampleInfo] = []
    ex_data: dict[str, Any] = data["examples"]

    for name, info in ex_data.items():
        examples.append(
            ExampleInfo(
                name=name,
                repo=info.get("repo", ""),
                domain=_parse_domain(info.get("domain", "code")),
                description=info.get("description", ""),
                installed=False,
            )
        )

    return examples
