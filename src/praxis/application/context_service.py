"""Context bundle service for generating AI-ready project context."""

from __future__ import annotations

from pathlib import Path

from praxis.application.opinions_service import resolve_opinions
from praxis.domain.domains import ARTIFACT_PATHS, Domain
from praxis.domain.models import ContextBundle
from praxis.domain.stages import REQUIRES_ARTIFACT, Stage
from praxis.infrastructure.yaml_loader import load_praxis_config


def get_context(project_root: Path) -> ContextBundle:
    """Generate a deterministic context bundle for a Praxis project.

    Args:
        project_root: Path to the project directory

    Returns:
        ContextBundle with project metadata, opinions, and artifact excerpt
    """
    errors: list[str] = []

    # Load praxis.yaml
    config_result = load_praxis_config(project_root)

    if not config_result.valid or config_result.config is None:
        # Collect error messages
        errors.extend([issue.message for issue in config_result.errors])

        # Return minimal bundle with errors
        return ContextBundle(
            project_name=project_root.name,
            domain="unknown",
            stage="unknown",
            privacy_level="unknown",
            environment="unknown",
            errors=errors,
        )

    config = config_result.config

    # Resolve opinions
    resolved_opinions = resolve_opinions(
        domain=config.domain.value,
        stage=config.stage.value,
        subtype=config.subtype,
        start_path=project_root,
    )

    # Extract opinion file paths
    opinion_paths = [f.path for f in resolved_opinions.existing_files]

    # Get formalize artifact info
    formalize_artifact = _get_formalize_artifact_info(
        project_root, config.domain, config.stage
    )

    return ContextBundle(
        project_name=project_root.name,
        domain=config.domain.value,
        stage=config.stage.value,
        privacy_level=config.privacy_level.value,
        environment=config.environment,
        subtype=config.subtype,
        opinions=opinion_paths,
        formalize_artifact=formalize_artifact,
        errors=errors,
    )


def _get_formalize_artifact_info(
    project_root: Path,
    domain: Domain,
    stage: Stage,
) -> dict[str, str | None]:
    """Get formalize artifact path and excerpt if applicable.

    Args:
        project_root: Project directory
        domain: Project domain
        stage: Current lifecycle stage

    Returns:
        Dict with 'path' and 'excerpt' keys
    """

    # Check if stage requires artifact
    if stage not in REQUIRES_ARTIFACT:
        return {"path": None, "excerpt": None}

    # Get artifact path for domain
    artifact_rel_path = ARTIFACT_PATHS.get(domain)
    if artifact_rel_path is None:
        return {"path": None, "excerpt": None}

    artifact_path = project_root / artifact_rel_path

    if not artifact_path.exists():
        # Artifact required but not found - include path with null excerpt
        return {"path": str(artifact_rel_path), "excerpt": None}

    # Read excerpt (first 100 lines or 4KB)
    try:
        excerpt = _read_artifact_excerpt(artifact_path)
        return {"path": str(artifact_rel_path), "excerpt": excerpt}
    except Exception as e:
        # Error reading file
        return {
            "path": str(artifact_rel_path),
            "excerpt": f"Error reading file: {e}",
        }


def _read_artifact_excerpt(
    artifact_path: Path, max_lines: int = 100, max_bytes: int = 4096
) -> str:
    """Read an excerpt from an artifact file.

    Args:
        artifact_path: Path to the artifact file
        max_lines: Maximum number of lines to read (default: 100)
        max_bytes: Maximum bytes to read (default: 4KB)

    Returns:
        Excerpt text, truncated if necessary
    """
    lines: list[str] = []
    bytes_read = 0

    with artifact_path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i >= max_lines:
                break

            line_bytes = len(line.encode("utf-8"))
            if bytes_read + line_bytes > max_bytes:
                break

            lines.append(line)
            bytes_read += line_bytes

    excerpt = "".join(lines)

    # Add truncation indicator if we stopped early
    with artifact_path.open("r", encoding="utf-8") as f:
        all_lines = f.readlines()
        if len(all_lines) > len(lines):
            excerpt += (
                f"\n... (truncated at {len(lines)} lines "
                f"of {len(all_lines)} total)\n"
            )

    return excerpt
