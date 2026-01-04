"""Infrastructure for loading and parsing opinion files."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from praxis.domain.opinions import (
    OpinionFile,
    OpinionFrontmatter,
    OpinionStatus,
    OpinionsTree,
)
from praxis.domain.workspace import ExtensionManifest, OpinionContribution


def parse_frontmatter(
    content: str,
) -> tuple[OpinionFrontmatter | None, str, str | None]:
    """Parse YAML frontmatter from markdown content.

    Returns:
        Tuple of (frontmatter, body, error).
        If parsing fails, frontmatter is None and error contains the message.
    """
    # Match YAML frontmatter delimited by ---
    pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        # No frontmatter found - return content as body
        return None, content, None

    yaml_str = match.group(1)
    body = match.group(2)

    try:
        data = yaml.safe_load(yaml_str)
        if not isinstance(data, dict):
            return None, content, "Frontmatter is not a valid YAML dictionary"

        # Validate required fields (domain is optional for _shared files)
        if "version" not in data:
            return None, body, "Missing required field: version"
        if "status" not in data:
            return None, body, "Missing required field: status"

        # Parse status enum
        try:
            data["status"] = OpinionStatus(data["status"])
        except ValueError:
            return None, body, f"Invalid status: {data['status']}"

        frontmatter = OpinionFrontmatter(**data)
        return frontmatter, body, None

    except yaml.YAMLError as e:
        return None, content, f"Invalid YAML: {e}"
    except Exception as e:
        return None, content, f"Failed to parse frontmatter: {e}"


def load_opinion_file(
    opinions_root: Path, relative_path: str, source: str = "core"
) -> OpinionFile:
    """Load a single opinion file.

    Args:
        opinions_root: Path to the opinions/ directory
        relative_path: Path relative to opinions/ (e.g., "code/principles.md")
        source: Provenance source ('core' or extension name)

    Returns:
        OpinionFile with parsed content or error information
    """
    full_path = opinions_root / relative_path

    if not full_path.exists():
        return OpinionFile(path=relative_path, exists=False, source=source)

    try:
        content = full_path.read_text(encoding="utf-8")
        frontmatter, body, error = parse_frontmatter(content)

        return OpinionFile(
            path=relative_path,
            exists=True,
            frontmatter=frontmatter,
            content=body.strip() if body else None,
            parse_error=error,
            source=source,
        )
    except Exception as e:
        return OpinionFile(
            path=relative_path,
            exists=True,
            frontmatter=None,
            content=None,
            parse_error=f"Failed to read file: {e}",
            source=source,
        )


def build_opinions_tree(opinions_root: Path) -> OpinionsTree:
    """Build a tree of all available opinion files.

    Args:
        opinions_root: Path to the opinions/ directory

    Returns:
        OpinionsTree with all discovered files
    """
    if not opinions_root.exists():
        return OpinionsTree(root=str(opinions_root), total_files=0)

    domains: dict[str, list[str]] = {}
    shared: list[str] = []
    total = 0

    for path in opinions_root.rglob("*.md"):
        relative = path.relative_to(opinions_root)
        parts = relative.parts

        # Skip templates
        if "_templates" in parts:
            continue

        # Skip other underscore directories (except _shared)
        if parts[0].startswith("_") and parts[0] != "_shared":
            continue

        # Use as_posix() for cross-platform path consistency
        relative_str = relative.as_posix()
        total += 1

        if parts[0] == "_shared":
            shared.append(relative_str)
        else:
            domain = parts[0]
            if domain not in domains:
                domains[domain] = []
            domains[domain].append(relative_str)

    # Sort for deterministic output
    shared.sort()
    for domain in domains:
        domains[domain].sort()

    return OpinionsTree(
        root=str(opinions_root),
        domains=dict(sorted(domains.items())),
        shared=shared,
        total_files=total,
    )


def find_opinions_root(start_path: Path) -> Path | None:
    """Find the opinions/ directory, searching upward from start_path.

    Args:
        start_path: Directory to start searching from

    Returns:
        Path to opinions/ directory, or None if not found
    """
    current = start_path.resolve()

    # Search up to 10 levels
    for _ in range(10):
        candidate = current / "opinions"
        if candidate.is_dir():
            return candidate

        parent = current.parent
        if parent == current:
            # Reached filesystem root
            break
        current = parent

    return None


def load_extension_opinions(
    extension_path: Path,
    extension_name: str,
    contributions: list[OpinionContribution],
) -> list[OpinionFile]:
    """Load opinion files contributed by an extension.

    Args:
        extension_path: Path to the extension directory
        extension_name: Name of the extension (for provenance)
        contributions: List of opinion contributions from manifest

    Returns:
        List of OpinionFile objects with extension provenance
    """
    opinions: list[OpinionFile] = []

    for contrib in contributions:
        source_path = extension_path / contrib.source
        if not source_path.exists():
            # Contribution file doesn't exist - skip with error
            opinions.append(
                OpinionFile(
                    path=contrib.target,
                    exists=False,
                    source=extension_name,
                    parse_error=f"Contribution source not found: {contrib.source}",
                )
            )
            continue

        # Load the file
        try:
            content = source_path.read_text(encoding="utf-8")
            frontmatter, body, error = parse_frontmatter(content)

            opinions.append(
                OpinionFile(
                    path=contrib.target,
                    exists=True,
                    frontmatter=frontmatter,
                    content=body.strip() if body else None,
                    parse_error=error,
                    source=extension_name,
                )
            )
        except Exception as e:
            opinions.append(
                OpinionFile(
                    path=contrib.target,
                    exists=False,
                    source=extension_name,
                    parse_error=f"Failed to read file: {e}",
                )
            )

    return opinions


def merge_opinions_with_extensions(
    core_opinions_root: Path,
    extension_manifests: list[tuple[Path, ExtensionManifest]],
) -> tuple[dict[str, OpinionFile], list[str]]:
    """Merge core opinions with extension contributions.

    Conflict resolution: core > alphabetical extension order.

    Args:
        core_opinions_root: Path to core opinions/ directory
        extension_manifests: List of (extension_path, manifest) tuples

    Returns:
        Tuple of (merged_opinions_dict, warnings)
        where merged_opinions_dict maps target_path -> OpinionFile
    """
    merged: dict[str, OpinionFile] = {}
    warnings: list[str] = []

    # First, load core opinions (if they exist)
    if core_opinions_root.exists():
        for path in core_opinions_root.rglob("*.md"):
            relative = path.relative_to(core_opinions_root)
            parts = relative.parts

            # Skip templates
            if "_templates" in parts:
                continue

            # Skip underscore directories except _shared
            if parts[0].startswith("_") and parts[0] != "_shared":
                continue

            relative_str = relative.as_posix()
            opinion = load_opinion_file(core_opinions_root, relative_str, source="core")
            merged[relative_str] = opinion

    # Sort extensions alphabetically for deterministic resolution
    sorted_extensions = sorted(extension_manifests, key=lambda x: x[1].name)

    # Process extensions in reverse alphabetical order
    # (so later alphabetical names win in conflicts)
    for ext_path, manifest in reversed(sorted_extensions):
        ext_opinions = load_extension_opinions(
            ext_path, manifest.name, manifest.contributions.opinions
        )

        for opinion in ext_opinions:
            target_path = opinion.path

            # Check for conflict
            if target_path in merged:
                existing = merged[target_path]
                # Core always wins
                if existing.source == "core":
                    warnings.append(
                        f"Extension '{manifest.name}' attempted to contribute "
                        f"'{target_path}' but core version takes precedence"
                    )
                    continue
                else:
                    # Extension conflict - alphabetically later wins
                    if manifest.name > existing.source:
                        warnings.append(
                            f"Extension '{manifest.name}' overrides '{target_path}' "
                            f"from '{existing.source}' (alphabetical precedence)"
                        )
                        merged[target_path] = opinion
                    else:
                        warnings.append(
                            f"Extension '{existing.source}' takes precedence over "
                            f"'{manifest.name}' for '{target_path}'"
                        )
            else:
                # No conflict - add the contribution
                merged[target_path] = opinion

    return merged, warnings


def build_opinions_tree_with_extensions(
    core_opinions_root: Path,
    extension_manifests: list[tuple[Path, ExtensionManifest]],
) -> OpinionsTree:
    """Build opinions tree including extension contributions.

    Args:
        core_opinions_root: Path to core opinions/ directory
        extension_manifests: List of (extension_path, manifest) tuples

    Returns:
        OpinionsTree with merged opinions and provenance info
    """
    merged, warnings = merge_opinions_with_extensions(
        core_opinions_root, extension_manifests
    )

    domains: dict[str, list[str]] = {}
    shared: list[str] = []
    provenance: dict[str, str] = {}
    extension_contributions: dict[str, list[str]] = {}

    for path, opinion in merged.items():
        if not opinion.exists:
            continue

        parts = path.split("/")

        # Track provenance
        provenance[path] = opinion.source

        # Track extension contributions
        if opinion.source != "core":
            if opinion.source not in extension_contributions:
                extension_contributions[opinion.source] = []
            extension_contributions[opinion.source].append(path)

        # Organize by domain/shared
        if parts[0] == "_shared":
            shared.append(path)
        else:
            domain = parts[0]
            if domain not in domains:
                domains[domain] = []
            domains[domain].append(path)

    # Sort for deterministic output
    shared.sort()
    for domain in domains:
        domains[domain].sort()

    return OpinionsTree(
        root=str(core_opinions_root),
        domains=dict(sorted(domains.items())),
        shared=shared,
        total_files=len(merged),
        provenance=provenance,
        extension_contributions=extension_contributions,
    )
