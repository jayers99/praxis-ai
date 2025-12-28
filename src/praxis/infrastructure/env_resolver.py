"""Resolve environment from PRAXIS_ENV or praxis.yaml."""

from __future__ import annotations

import os


def resolve_environment(yaml_environment: str) -> str:
    """Resolve the effective environment value.

    Environment variable PRAXIS_ENV takes precedence over praxis.yaml value.

    Args:
        yaml_environment: The environment value from praxis.yaml.

    Returns:
        The effective environment (from PRAXIS_ENV if set, otherwise from yaml).
    """
    return os.environ.get("PRAXIS_ENV", yaml_environment)
