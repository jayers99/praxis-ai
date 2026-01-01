"""Deterministic template resolver."""

from __future__ import annotations

from pathlib import Path

from praxis.domain.domains import Domain
from praxis.domain.stages import Stage
from praxis.domain.templates.models import TemplateProvenance, TemplateRoot, TemplateSelection
from praxis.infrastructure.stage_templates.template_paths import (
    artifact_template_candidates,
    ensure_within_root,
    stage_template_candidates,
)


def get_core_templates_root() -> Path:
    """Return the filesystem path to core templates bundled with the package."""

    # .../praxis/infrastructure/stage_templates/template_resolver.py
    # -> .../praxis/templates
    return Path(__file__).resolve().parents[2] / "templates"


class TemplateResolver:
    def __init__(self, roots: list[TemplateRoot]):
        if not roots:
            raise ValueError("At least one template root is required")
        self._roots = roots

    @property
    def roots(self) -> list[TemplateRoot]:
        return list(self._roots)

    def resolve_stage(
        self, domain: Domain, stage: Stage, subtype: str | None
    ) -> TemplateSelection:
        candidates = stage_template_candidates(domain=domain, stage=stage, subtype=subtype)
        return self._resolve_candidates(candidates)

    def resolve_artifact(
        self,
        domain: Domain,
        artifact_name: str,
        subtype: str | None,
    ) -> TemplateSelection:
        candidates = artifact_template_candidates(
            domain=domain,
            artifact_name=artifact_name,
            subtype=subtype,
        )
        return self._resolve_candidates(candidates)

    def _resolve_candidates(self, candidates: list[str]) -> TemplateSelection:
        attempts: list[str] = []
        for root in self._roots:
            root_path = root.path
            for rel in candidates:
                attempts.append(f"{root.kind}:{rel}")
                candidate_path = root_path / rel
                ensure_within_root(root_path, candidate_path)
                if candidate_path.exists() and candidate_path.is_file():
                    return TemplateSelection(
                        template_path=candidate_path,
                        provenance=TemplateProvenance(
                            root=root,
                            attempts=attempts,
                            selected_relative_path=rel,
                        ),
                    )

        raise FileNotFoundError("No template found. Attempts: " + ", ".join(attempts))
