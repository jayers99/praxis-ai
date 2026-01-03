"""Domain models for the stage template system."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

TemplateRootKind = Literal["project", "extension", "core", "custom"]


class TemplateRoot(BaseModel):
    """A root directory to search for templates."""

    kind: TemplateRootKind
    path: Path


class TemplateProvenance(BaseModel):
    """Explains why a template was selected."""

    root: TemplateRoot
    attempts: list[str] = Field(default_factory=list)
    selected_relative_path: str


class TemplateSelection(BaseModel):
    """The selected template path plus provenance."""

    template_path: Path
    provenance: TemplateProvenance


class RenderedFile(BaseModel):
    """Result of rendering a single file."""

    destination: Path
    status: Literal["created", "skipped", "overwritten", "error"]
    template_path: Path | None = None
    provenance: TemplateProvenance | None = None
    error: str | None = None


class TemplatesRenderResult(BaseModel):
    """Result of rendering a set of templates into a project."""

    success: bool
    created: list[Path] = Field(default_factory=list)
    skipped: list[Path] = Field(default_factory=list)
    overwritten: list[Path] = Field(default_factory=list)
    rendered: list[RenderedFile] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    info: list[str] = Field(default_factory=list)
