"""Application service for rendering lifecycle stage templates into a project."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from praxis.domain.domains import Domain
from praxis.domain.stages import Stage
from praxis.domain.templates.models import (
    RenderedFile,
    TemplateRoot,
    TemplatesRenderResult,
)
from praxis.domain.workspace import ExtensionManifest
from praxis.infrastructure.stage_templates.template_renderer import (
    render_template_to_file,
)
from praxis.infrastructure.stage_templates.template_resolver import (
    TemplateResolver,
    get_core_templates_root,
)


def _build_extension_template_roots(
    extension_manifests: list[tuple[Path, ExtensionManifest]],
    subtype: str | None,
) -> list[TemplateRoot]:
    """Build TemplateRoot entries for extension template contributions.

    Extensions should have templates following the standard structure.
    The manifest's template contributions are used for subtype filtering.

    Args:
        extension_manifests: List of (extension_path, manifest) tuples
        subtype: Current project subtype (for filtering)

    Returns:
        List of TemplateRoot entries, sorted alphabetically by extension name
    """
    roots: list[TemplateRoot] = []

    # Sort extensions alphabetically for deterministic precedence
    sorted_manifests = sorted(extension_manifests, key=lambda x: x[1].name)

    for ext_path, manifest in sorted_manifests:
        # Check if this extension contributes any templates
        if not manifest.contributions.templates:
            continue

        # Check if any templates apply to this subtype
        has_applicable_template = False
        for template in manifest.contributions.templates:
            # Empty subtypes list means applies to all subtypes
            if not template.subtypes or (subtype and subtype in template.subtypes):
                has_applicable_template = True
                break

        if has_applicable_template:
            # Extensions organize templates in a templates/ subdirectory
            # following the standard template structure
            templates_dir = ext_path / "templates"
            if templates_dir.exists():
                roots.append(TemplateRoot(kind="extension", path=templates_dir))

    return roots


def _default_template_roots(
    project_root: Path,
    extra_roots: list[Path] | None = None,
    extension_roots: list[TemplateRoot] | None = None,
) -> list[TemplateRoot]:
    roots: list[TemplateRoot] = []

    # 1. Project-local templates (.praxis/templates/)
    project_local = project_root / ".praxis" / "templates"
    if project_local.exists():
        roots.append(TemplateRoot(kind="project", path=project_local))

    # 2. Custom/extra roots (--template-root CLI arg)
    if extra_roots:
        for p in extra_roots:
            roots.append(TemplateRoot(kind="custom", path=p))

    # 3. Extension roots (alphabetically sorted, before core)
    # Extensions can provide domain/subtype-specific templates
    if extension_roots:
        roots.extend(extension_roots)

    # 4. Core bundled templates (fallback for generic templates)
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
    extension_manifests: list[tuple[Path, ExtensionManifest]] | None = None,
) -> TemplatesRenderResult:
    """Render stage docs and domain-specific formalization artifacts.

    MVP inventory:
    - Stage doc for every stage: docs/<stage>.md
    - Domain-specific formalization artifacts as applicable (Formalize+):
        - Code: docs/sod.md
        - Create/Write: docs/brief.md
        - Learn: docs/plan.md

    Args:
        project_root: Path to project directory
        domain: Project domain
        subtype: Optional project subtype
        stages: Optional list of specific stages to render (defaults to all)
        force: Whether to overwrite existing files
        extra_template_roots: Additional template directories from CLI
        extension_manifests: List of (extension_path, manifest) tuples
    """

    # Build extension template roots with subtype filtering
    extension_roots: list[TemplateRoot] | None = None
    if extension_manifests:
        extension_roots = _build_extension_template_roots(extension_manifests, subtype)

    roots = _default_template_roots(
        project_root,
        extra_roots=extra_template_roots,
        extension_roots=extension_roots,
    )
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
            result.rendered.append(RenderedFile(destination=project_root, status="error", error=str(e)))

    _render_minimal_domain_artifact_if_needed(
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


def _render_minimal_domain_artifact_if_needed(
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
    should_render_artifact = any(s >= Stage.FORMALIZE for s in stages_to_render)
    if not should_render_artifact:
        return

    artifact_name: str | None
    filename: str | None

    if domain == Domain.CODE:
        artifact_name = "sod"
        filename = "sod.md"
    elif domain in (Domain.CREATE, Domain.WRITE):
        artifact_name = "brief"
        filename = "brief.md"
    elif domain == Domain.LEARN:
        artifact_name = "plan"
        filename = "plan.md"
    elif domain == Domain.OBSERVE:
        # Observe domain has no formalize artifact
        msg = (
            "Observe domain has no formalize artifact. " "Observe is for raw capture and does not cross into execution."
        )
        result.info.append(msg)
        return
    else:
        return

    try:
        selection = resolver.resolve_artifact(
            domain=domain,
            artifact_name=artifact_name,
            subtype=subtype,
        )
        dest = project_root / "docs" / filename
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
