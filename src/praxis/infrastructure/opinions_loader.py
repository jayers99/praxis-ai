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


def load_opinion_file(opinions_root: Path, relative_path: str) -> OpinionFile:
    """Load a single opinion file.

    Args:
        opinions_root: Path to the opinions/ directory
        relative_path: Path relative to opinions/ (e.g., "code/principles.md")

    Returns:
        OpinionFile with parsed content or error information
    """
    full_path = opinions_root / relative_path

    if not full_path.exists():
        return OpinionFile(path=relative_path, exists=False)

    try:
        content = full_path.read_text(encoding="utf-8")
        frontmatter, body, error = parse_frontmatter(content)

        return OpinionFile(
            path=relative_path,
            exists=True,
            frontmatter=frontmatter,
            content=body.strip() if body else None,
            parse_error=error,
        )
    except Exception as e:
        return OpinionFile(
            path=relative_path,
            exists=True,
            frontmatter=None,
            content=None,
            parse_error=f"Failed to read file: {e}",
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
