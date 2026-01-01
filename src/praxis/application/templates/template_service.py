"""Application service for rendering lifecycle stage templates into a project."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from praxis.domain.domains import Domain
from praxis.domain.stages import Stage
from praxis.domain.templates.models import RenderedFile, TemplateRoot, TemplatesRenderResult
from praxis.infrastructure.stage_templates.template_renderer import render_template_to_file
from praxis.infrastructure.stage_templates.template_resolver import (
    TemplateResolver,
    get_core_templates_root,
)


def _default_template_roots(project_root: Path, extra_roots: list[Path] | None = None) -> list[TemplateRoot]:
    roots: list[TemplateRoot] = []

    project_local = project_root / ".praxis" / "templates"
    if project_local.exists():
        roots.append(TemplateRoot(kind="project", path=project_local))

    if extra_roots:
        for p in extra_roots:
            roots.append(TemplateRoot(kind="custom", path=p))

    roots.append(TemplateRoot(kind="core", path=get_core_templates_root()))

    return roots


def render_stage_templates(
    *,
    project_root: Path,
    domain: Domain,
    subtype: str | None,
    stages: list[Stage] | None = None,
    force: bool = False,
    extra_template_roots: list[Path] | None = None,
) -> TemplatesRenderResult:
    """Render stage docs (and minimal domain artifacts) into a project.

    MVP inventory:
    - Stage doc for every stage: docs/<stage>.md
    - Code domain formalization artifact: docs/sod.md
    """

    roots = _default_template_roots(project_root, extra_roots=extra_template_roots)
    resolver = TemplateResolver(roots)

    stages_to_render = stages if stages is not None else list(Stage)

    result = TemplatesRenderResult(success=True)

    context = {
        "today": date.today().isoformat(),
        "domain": domain.value,
        "subtype": subtype or "",
    }

    for stage in stages_to_render:
        try:
            selection = resolver.resolve_stage(domain=domain, stage=stage, subtype=subtype)
            dest = project_root / "docs" / f"{stage.value}.md"
            ok, err, status = render_template_to_file(
                template_path=selection.template_path,
                destination=dest,
                context={**context, "stage": stage.value},
                force=force,
            )

            rendered = RenderedFile(
                destination=dest,
                status=status,
                template_path=selection.template_path,
                provenance=selection.provenance,
                error=err,
            )
            result.rendered.append(rendered)

            if not ok:
                result.success = False
                if err:
                    result.errors.append(err)
                continue

            if status == "created":
                result.created.append(dest)
            elif status == "skipped":
                result.skipped.append(dest)
            elif status == "overwritten":
                result.overwritten.append(dest)
        except Exception as e:  # keep going, report
            result.success = False
            result.errors.append(str(e))
            result.rendered.append(
                RenderedFile(destination=project_root, status="error", error=str(e))
            )

    # Minimal domain artifact: Code domain SOD (generate at Formalize+)
    should_render_sod = any(s >= Stage.FORMALIZE for s in stages_to_render)
    if domain == Domain.CODE and should_render_sod:
        try:
            selection = resolver.resolve_artifact(
                domain=domain,
                artifact_name="sod",
                subtype=subtype,
            )
            dest = project_root / "docs" / "sod.md"
            ok, err, status = render_template_to_file(
                template_path=selection.template_path,
                destination=dest,
                context=context,
                force=force,
            )

            result.rendered.append(
                RenderedFile(
                    destination=dest,
                    status=status,
                    template_path=selection.template_path,
                    provenance=selection.provenance,
                    error=err,
                )
            )

            if not ok:
                result.success = False
                if err:
                    result.errors.append(err)
            else:
                if status == "created":
                    result.created.append(dest)
                elif status == "skipped":
                    result.skipped.append(dest)
                elif status == "overwritten":
                    result.overwritten.append(dest)
        except Exception as e:
            result.success = False
            result.errors.append(str(e))

    _render_create_brief_if_needed(
        project_root=project_root,
        domain=domain,
        subtype=subtype,
        stages_to_render=stages_to_render,
        resolver=resolver,
        force=force,
        context=context,
        result=result,
    )

    return result


def _render_create_brief_if_needed(
    *,
    project_root: Path,
    domain: Domain,
    subtype: str | None,
    stages_to_render: list[Stage],
    resolver: TemplateResolver,
    force: bool,
    context: dict[str, str],
    result: TemplatesRenderResult,
) -> None:
    should_render_brief = any(s >= Stage.FORMALIZE for s in stages_to_render)
    if domain != Domain.CREATE or not should_render_brief:
        return

    try:
        selection = resolver.resolve_artifact(
            domain=domain,
            artifact_name="brief",
            subtype=subtype,
        )
        dest = project_root / "docs" / "brief.md"
        ok, err, status = render_template_to_file(
            template_path=selection.template_path,
            destination=dest,
            context=context,
            force=force,
        )

        result.rendered.append(
            RenderedFile(
                destination=dest,
                status=status,
                template_path=selection.template_path,
                provenance=selection.provenance,
                error=err,
            )
        )

        if not ok:
            result.success = False
            if err:
                result.errors.append(err)
            return

        if status == "created":
            result.created.append(dest)
        elif status == "skipped":
            result.skipped.append(dest)
        elif status == "overwritten":
            result.overwritten.append(dest)
    except Exception as e:
        result.success = False
        result.errors.append(str(e))
