from __future__ import annotations

from pathlib import Path

import pytest

from praxis.domain.domains import Domain
from praxis.domain.stages import Stage
from praxis.domain.templates.models import TemplateRoot
from praxis.infrastructure.stage_templates.template_resolver import TemplateResolver
from praxis.infrastructure.stage_templates.template_renderer import render_template_text
from praxis.infrastructure.stage_templates.template_renderer import render_template_to_file


def test_resolver_is_deterministic(tmp_path: Path) -> None:
    core = tmp_path / "core"
    (core / "stage").mkdir(parents=True)
    (core / "stage" / "capture.md").write_text("core")

    roots = [TemplateRoot(kind="core", path=core)]
    resolver = TemplateResolver(roots)

    a = resolver.resolve_stage(domain=Domain.CODE, stage=Stage.CAPTURE, subtype=None)
    b = resolver.resolve_stage(domain=Domain.CODE, stage=Stage.CAPTURE, subtype=None)

    assert a.template_path == b.template_path
    assert a.provenance.selected_relative_path == "stage/capture.md"


def test_resolver_precedence_project_over_core(tmp_path: Path) -> None:
    project = tmp_path / "project"
    core = tmp_path / "core"

    (project / "stage").mkdir(parents=True)
    (core / "stage").mkdir(parents=True)

    (project / "stage" / "capture.md").write_text("project")
    (core / "stage" / "capture.md").write_text("core")

    roots = [
        TemplateRoot(kind="project", path=project),
        TemplateRoot(kind="core", path=core),
    ]
    resolver = TemplateResolver(roots)

    selection = resolver.resolve_stage(domain=Domain.CODE, stage=Stage.CAPTURE, subtype=None)
    assert selection.template_path.read_text() == "project"
    assert selection.provenance.root.kind == "project"


def test_renderer_skips_existing_by_default(tmp_path: Path) -> None:
    template = tmp_path / "t.md"
    dest = tmp_path / "out.md"

    template.write_text("hello")
    dest.write_text("existing")

    ok, err, status = render_template_to_file(
        template_path=template,
        destination=dest,
        context={},
        force=False,
    )

    assert ok is True
    assert err is None
    assert status == "skipped"
    assert dest.read_text() == "existing"


def test_renderer_overwrites_with_force(tmp_path: Path) -> None:
    template = tmp_path / "t.md"
    dest = tmp_path / "out.md"

    template.write_text("hello")
    dest.write_text("existing")

    ok, err, status = render_template_to_file(
        template_path=template,
        destination=dest,
        context={},
        force=True,
    )

    assert ok is True
    assert err is None
    assert status == "overwritten"
    assert dest.read_text() == "hello"


def test_render_template_text_substitutes_defined_variables() -> None:
    rendered = render_template_text("Hello {name}!", {"name": "World"})
    assert rendered == "Hello World!"


def test_render_template_text_preserves_missing_variables() -> None:
    rendered = render_template_text("Hello {name} {missing}", {"name": "World"})
    assert rendered == "Hello World {missing}"


def test_subtype_validation_rejects_path_traversal(tmp_path: Path) -> None:
    core = tmp_path / "core"
    (core / "stage").mkdir(parents=True)
    (core / "stage" / "capture.md").write_text("core")

    resolver = TemplateResolver([TemplateRoot(kind="core", path=core)])

    with pytest.raises(ValueError):
        resolver.resolve_stage(
            domain=Domain.CODE,
            stage=Stage.CAPTURE,
            subtype="../evil",
        )


def test_artifact_name_validation_rejects_path_traversal(tmp_path: Path) -> None:
    core = tmp_path / "core"
    (core / "domain" / "code" / "artifact").mkdir(parents=True)
    (core / "domain" / "code" / "artifact" / "sod.md").write_text("core")

    resolver = TemplateResolver([TemplateRoot(kind="core", path=core)])

    with pytest.raises(ValueError):
        resolver.resolve_artifact(
            domain=Domain.CODE,
            artifact_name="../evil",
            subtype=None,
        )
