"""Application service for opinions resolution."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from praxis.domain.opinions import (
    OpinionFile,
    OpinionsTree,
    ResolvedOpinions,
)
from praxis.infrastructure.manifest_loader import discover_extension_manifests
from praxis.infrastructure.opinions_loader import (
    build_opinions_tree,
    build_opinions_tree_with_extensions,
    find_opinions_root,
    load_opinion_file,
    merge_opinions_with_extensions,
)
from praxis.infrastructure.workspace_config_repo import load_workspace_config


def _get_extension_manifests(
    start_path: Path,
) -> list[tuple[Path, Any]] | None:
    """Discover extension manifests from workspace.

    Args:
        start_path: Starting path to search for workspace

    Returns:
        List of (extension_path, manifest) tuples, or None if no workspace found
    """
    # Try to find workspace by looking for PRAXIS_HOME env var
    praxis_home = os.environ.get("PRAXIS_HOME")
    if not praxis_home:
        return None

    workspace_path = Path(praxis_home)
    if not workspace_path.exists():
        return None

    # Load workspace config
    try:
        config = load_workspace_config(workspace_path)
    except Exception:
        return None

    # Discover extension manifests
    extensions_path = workspace_path / "extensions"
    if not extensions_path.exists():
        return None

    manifest_results = discover_extension_manifests(
        extensions_path, config.installed_extensions
    )

    # Filter to successful manifests only
    manifests: list[tuple[Path, Any]] = []
    for result in manifest_results:
        if result.success and result.manifest:
            ext_path = extensions_path / result.extension_name
            manifests.append((ext_path, result.manifest))

    return manifests if manifests else None


def compute_resolution_chain(
    domain: str,
    stage: str | None = None,
    subtype: str | None = None,
) -> list[str]:
    """Compute the ordered list of opinion file paths to resolve.

    Resolution order (general → specific):
    1. _shared/first-principles.md
    2. {domain}/README.md
    3. {domain}/principles.md
    4. {domain}/{stage}.md (if stage provided)
    5. {domain}/subtypes/{subtype}/README.md (if subtype provided)
    6. {domain}/subtypes/{subtype}/principles.md (if subtype provided)
    7. {domain}/subtypes/{subtype}/{stage}.md (if both provided)

    For nested subtypes (e.g., "cli-python"), each level is resolved:
    - subtypes/cli/README.md, subtypes/cli/principles.md, subtypes/cli/{stage}.md
    - subtypes/cli/python/README.md, subtypes/cli/python/principles.md, ...

    Args:
        domain: The domain (code, create, write, learn, observe)
        stage: Optional lifecycle stage
        subtype: Optional subtype (may be nested with hyphens or dots)

    Returns:
        Ordered list of relative paths to check
    """
    paths: list[str] = []

    # 1. Shared principles (always apply)
    paths.append("_shared/first-principles.md")

    # 2. Domain level
    paths.append(f"{domain}/README.md")
    paths.append(f"{domain}/principles.md")

    # 3. Domain stage (if provided)
    if stage:
        paths.append(f"{domain}/{stage}.md")

    # 4. Subtype chain (if provided)
    if subtype:
        # Handle nested subtypes per opinions-contract.md section 5.1:
        # Both "cli-python" (hyphen) and "cli.python" (dot) → ["cli", "python"]
        segments = subtype.replace(".", "-").split("-")
        accumulated = f"{domain}/subtypes"

        for segment in segments:
            accumulated = f"{accumulated}/{segment}"
            paths.append(f"{accumulated}/README.md")
            paths.append(f"{accumulated}/principles.md")
            if stage:
                paths.append(f"{accumulated}/{stage}.md")

    return paths


def resolve_opinions(
    domain: str,
    stage: str | None = None,
    subtype: str | None = None,
    opinions_root: Path | None = None,
    start_path: Path | None = None,
) -> ResolvedOpinions:
    """Resolve applicable opinions for a project context.

    Includes extension contributions if workspace is available.

    Args:
        domain: The domain (code, create, write, learn, observe)
        stage: Optional lifecycle stage
        subtype: Optional subtype
        opinions_root: Explicit path to opinions/ directory
        start_path: Directory to search from (if opinions_root not provided)

    Returns:
        ResolvedOpinions with files in resolution order
    """
    warnings: list[str] = []

    # Find opinions root
    if opinions_root is None:
        if start_path is None:
            start_path = Path.cwd()
        opinions_root = find_opinions_root(start_path)

    if opinions_root is None or not opinions_root.exists():
        warnings.append("No opinions directory found")
        return ResolvedOpinions(
            domain=domain,
            stage=stage,
            subtype=subtype,
            files=[],
            warnings=warnings,
        )

    # Get extension manifests (if workspace available)
    extension_manifests = _get_extension_manifests(start_path or Path.cwd())

    # Merge opinions from core and extensions
    if extension_manifests:
        merged, merge_warnings = merge_opinions_with_extensions(
            opinions_root, extension_manifests
        )
        warnings.extend(merge_warnings)
    else:
        # No extensions - just load core opinions
        merged = {}
        for path in opinions_root.rglob("*.md"):
            relative = path.relative_to(opinions_root)
            parts = relative.parts
            if "_templates" in parts:
                continue
            if parts[0].startswith("_") and parts[0] != "_shared":
                continue
            relative_str = relative.as_posix()
            merged[relative_str] = load_opinion_file(
                opinions_root, relative_str, source="core"
            )

    # Compute resolution chain
    chain = compute_resolution_chain(domain, stage, subtype)

    # Load files in resolution order
    files: list[OpinionFile] = []
    for file_path in chain:
        if file_path in merged:
            opinion_file = merged[file_path]
            if opinion_file.exists:
                files.append(opinion_file)
                # Check for parse errors
                if opinion_file.parse_error:
                    warnings.append(
                        f"Parse error in {file_path}: {opinion_file.parse_error}"
                    )
                # Check for deprecated status
                if (
                    opinion_file.frontmatter
                    and opinion_file.frontmatter.status.value == "deprecated"
                ):
                    warnings.append(f"Deprecated opinion file: {file_path}")

    return ResolvedOpinions(
        domain=domain,
        stage=stage,
        subtype=subtype,
        files=files,
        warnings=warnings,
    )


def format_prompt_output(resolved: ResolvedOpinions) -> str:
    """Format resolved opinions as a copy-pasteable AI context block.

    Args:
        resolved: The resolved opinions

    Returns:
        Markdown-formatted string suitable for AI context
    """
    lines: list[str] = []

    # Header
    lines.append("# Praxis Opinions Context")
    lines.append("")
    lines.append(f"**Domain:** {resolved.domain}")
    if resolved.stage:
        lines.append(f"**Stage:** {resolved.stage}")
    if resolved.subtype:
        lines.append(f"**Subtype:** {resolved.subtype}")
    lines.append("")

    # AI guidelines for interpreting and applying these opinions
    lines.append("## AI Guidelines")
    lines.append("")
    lines.append("- Opinions are advisory guidance, not hard rules")
    lines.append("- If user instruction conflicts with opinion, follow user")
    lines.append("- Use quality gates when evaluating readiness")
    lines.append("")

    # Provenance
    lines.append("## Applied Opinions")
    lines.append("")
    lines.append(f"The following {len(resolved.existing_files)} opinion files apply:")
    lines.append("")
    for i, f in enumerate(resolved.existing_files, 1):
        lines.append(f"{i}. `{f.path}`")
    lines.append("")

    # Content sections
    lines.append("---")
    lines.append("")

    for opinion in resolved.existing_files:
        lines.append(f"## {opinion.path}")
        lines.append("")
        if opinion.content:
            lines.append(opinion.content)
        else:
            lines.append("*(No content)*")
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def format_json_output(resolved: ResolvedOpinions) -> dict[str, Any]:
    """Format resolved opinions as a JSON-serializable dict.

    Args:
        resolved: The resolved opinions

    Returns:
        Dict with stable schema for automation
    """
    return {
        "domain": resolved.domain,
        "stage": resolved.stage,
        "subtype": resolved.subtype,
        "files": [
            {
                "path": f.path,
                "exists": f.exists,
                "status": f.frontmatter.status.value if f.frontmatter else None,
                "version": f.frontmatter.version if f.frontmatter else None,
                "parse_error": f.parse_error,
            }
            for f in resolved.files
        ],
        "warnings": resolved.warnings,
    }


def format_list_output(tree: OpinionsTree) -> str:
    """Format opinions tree as a human-readable tree structure.

    Args:
        tree: The opinions tree

    Returns:
        Tree-formatted string with provenance information
    """
    lines: list[str] = []

    lines.append("opinions/")

    # Shared files
    if tree.shared:
        lines.append("├── _shared/")
        for i, path in enumerate(tree.shared):
            # Extract filename from path
            filename = path.split("/")[-1]
            prefix = "│   └── " if i == len(tree.shared) - 1 else "│   ├── "
            # Add provenance if available
            source = tree.provenance.get(path, "core")
            source_label = f" [{source}]" if source != "core" else ""
            lines.append(f"{prefix}{filename}{source_label}")

    # Domain files
    domain_list = list(tree.domains.items())
    for d_idx, (domain, files) in enumerate(domain_list):
        is_last_domain = d_idx == len(domain_list) - 1
        domain_prefix = "└── " if is_last_domain else "├── "
        lines.append(f"{domain_prefix}{domain}/")

        # Group files by subdirectory
        subdir_prefix = "    " if is_last_domain else "│   "

        for f_idx, filepath in enumerate(files):
            is_last_file = f_idx == len(files) - 1
            # Get path relative to domain
            rel_path = filepath.split("/", 1)[1] if "/" in filepath else filepath
            file_prefix = "└── " if is_last_file else "├── "
            # Add provenance if available
            source = tree.provenance.get(filepath, "core")
            source_label = f" [{source}]" if source != "core" else ""
            lines.append(f"{subdir_prefix}{file_prefix}{rel_path}{source_label}")

    lines.append("")
    lines.append(f"Total: {tree.total_files} opinion files")

    # Show extension contributions summary if any
    if tree.extension_contributions:
        lines.append("")
        lines.append("Extension contributions:")
        for ext_name in sorted(tree.extension_contributions.keys()):
            count = len(tree.extension_contributions[ext_name])
            lines.append(f"  • {ext_name}: {count} file(s)")

    return "\n".join(lines)


def get_opinions_tree(
    opinions_root: Path | None = None,
    start_path: Path | None = None,
) -> tuple[OpinionsTree | None, str | None]:
    """Get the tree of all available opinion files.

    Args:
        opinions_root: Explicit path to opinions/ directory
        start_path: Directory to search from (if opinions_root not provided)

    Returns:
        Tuple of (tree, warning). Tree is None if opinions/ not found.
    """
    if opinions_root is None:
        if start_path is None:
            start_path = Path.cwd()
        opinions_root = find_opinions_root(start_path)

    if opinions_root is None or not opinions_root.exists():
        return None, "No opinions directory found"

    # Get extension manifests (if workspace available)
    extension_manifests = _get_extension_manifests(start_path or Path.cwd())

    if extension_manifests:
        tree = build_opinions_tree_with_extensions(opinions_root, extension_manifests)
    else:
        tree = build_opinions_tree(opinions_root)

    return tree, None
