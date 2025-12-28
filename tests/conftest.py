"""Shared pytest fixtures."""

from __future__ import annotations

from typing import Any

import pytest
from typer.testing import CliRunner


@pytest.fixture
def cli_runner() -> CliRunner:
    """Provide a Typer CLI test runner."""
    return CliRunner()


@pytest.fixture
def context() -> dict[str, Any]:
    """Provide a context dict for BDD step communication."""
    return {}
