"""CATALOG.md writer for research library.

Updates all sections of CATALOG.md when cataloging artifacts.
Follows the format defined in the Cataloger role specification.
"""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from praxis.domain.catalog import CatalogEntry


def _find_section_boundaries(
    content: str, section_header: str
) -> tuple[int, int] | None:
    """Find the start and end positions of a markdown section.

    Args:
        content: Full CATALOG.md content.
        section_header: Section header to find (e.g., "## Quick Reference").

    Returns:
        Tuple of (start_pos, end_pos) or None if not found.
        start_pos points to the line after the header.
        end_pos points to the next ## header or end of file.
    """
    # Find section header
    header_pattern = re.escape(section_header) + r"\s*\n"
    match = re.search(header_pattern, content)

    if not match:
        return None

    start_pos = match.end()

    # Find next section (## heading) or end of file
    next_section = re.search(r"\n##\s+", content[start_pos:])
    if next_section:
        end_pos = start_pos + next_section.start()
    else:
        end_pos = len(content)

    return (start_pos, end_pos)


def _update_quick_reference(content: str, entry: CatalogEntry) -> str:
    """Update the Quick Reference table with a new entry.

    Adds entry in date-sorted order (newest first).

    Args:
        content: Current CATALOG.md content.
        entry: Catalog entry to add.

    Returns:
        Updated content.
    """
    boundaries = _find_section_boundaries(content, "## Quick Reference")
    if not boundaries:
        raise ValueError("Quick Reference section not found in CATALOG.md")

    start_pos, end_pos = boundaries
    section = content[start_pos:end_pos]

    # Parse existing table
    table_pattern = (
        r"\| \[([^\]]+)\]\(([^\)]+)\) \| ([^\|]+) \| "
        r"([^\|]+) \| ([^\|]+) \| ([^\|]+) \|"
    )

    rows = []
    for match in re.finditer(table_pattern, section):
        row_id = match.group(1).strip()
        row_path = match.group(2).strip()
        row_title = match.group(3).strip()
        row_topic = match.group(4).strip()
        row_consensus = match.group(5).strip()
        row_date = match.group(6).strip()
        rows.append((row_date, row_id, row_path, row_title, row_topic, row_consensus))

    # Add new entry
    new_row = (
        entry.date,
        entry.id,
        str(entry.path),
        entry.title,
        entry.topic,
        entry.consensus,
    )
    rows.append(new_row)

    # Sort by date (newest first)
    rows.sort(reverse=True, key=lambda r: r[0])

    # Rebuild table
    table_lines = [
        "| ID | Title | Topic | Consensus | Date |",
        "|----|-------|-------|-----------|------|",
    ]
    for row in rows:
        date, row_id, row_path, title, topic, consensus = row
        table_lines.append(
            f"| [{row_id}]({row_path}) | {title} | {topic} | {consensus} | {date} |"
        )

    new_section = "\n".join(table_lines) + "\n"

    # Replace section
    return content[:start_pos] + new_section + content[end_pos:]


def _update_by_topic(content: str, entry: CatalogEntry) -> str:
    """Update the By Topic section with a new entry.

    Creates topic subsection if it doesn't exist.

    Args:
        content: Current CATALOG.md content.
        entry: Catalog entry to add.

    Returns:
        Updated content.
    """
    boundaries = _find_section_boundaries(content, "## By Topic")
    if not boundaries:
        raise ValueError("By Topic section not found in CATALOG.md")

    start_pos, end_pos = boundaries
    section = content[start_pos:end_pos]

    # Find or create topic subsection
    topic_header = f"### {entry.topic.title()}"
    topic_pattern = re.escape(topic_header) + r"\s*\n"
    topic_match = re.search(topic_pattern, section)

    keywords_str = ", ".join(entry.keywords)
    new_entry_line = (
        f"| [{entry.id}]({entry.path}) | {entry.title} | "
        f"{entry.consensus} | {keywords_str} |\n"
    )

    if topic_match:
        # Topic exists, add to it
        # Find the table in this topic subsection
        topic_start = topic_match.end()

        # Find next subsection or end
        next_topic = re.search(r"\n###\s+", section[topic_start:])
        if next_topic:
            topic_end = topic_start + next_topic.start()
        else:
            topic_end = len(section)

        topic_section = section[topic_start:topic_end]

        # Insert after table header (skip first 2 lines)
        lines = topic_section.split("\n")
        if len(lines) >= 2:
            # Insert after header row and separator
            lines.insert(2, new_entry_line.rstrip())
            new_topic_section = "\n".join(lines)
        else:
            # No table yet, create it
            new_topic_section = (
                "\n| ID | Title | Consensus | Keywords |\n"
                "|----|-------|-----------|----------|\n"
                + new_entry_line
            )

        new_section = (
            section[:topic_start] + new_topic_section + section[topic_end:]
        )
    else:
        # Topic doesn't exist, create new subsection
        # Insert alphabetically among existing topics
        topic_headers = list(re.finditer(r"\n### ([^\n]+)", section))

        # Find insertion point
        insert_pos = None
        for i, header_match in enumerate(topic_headers):
            existing_topic = header_match.group(1).strip()
            if entry.topic.title() < existing_topic:
                insert_pos = header_match.start()
                break

        if insert_pos is None:
            # Add at end of topics
            insert_pos = len(section) - 1

        new_topic_block = (
            f"\n### {entry.topic.title()}\n\n"
            "| ID | Title | Consensus | Keywords |\n"
            "|----|-------|-----------|----------|\n"
            + new_entry_line
            + "\n"
        )

        new_section = section[:insert_pos] + new_topic_block + section[insert_pos:]

    return content[:start_pos] + new_section + content[end_pos:]


def _update_by_consensus(content: str, entry: CatalogEntry) -> str:
    """Update the By Consensus section with a new entry.

    Args:
        content: Current CATALOG.md content.
        entry: Catalog entry to add.

    Returns:
        Updated content.
    """
    boundaries = _find_section_boundaries(content, "## By Consensus")
    if not boundaries:
        raise ValueError("By Consensus section not found in CATALOG.md")

    start_pos, end_pos = boundaries
    section = content[start_pos:end_pos]

    # Map consensus values to section headers
    consensus_lower = entry.consensus.lower()
    if "high" in consensus_lower:
        subsection = "### High Consensus"
    elif "strong" in consensus_lower:
        subsection = "### Strong Consensus"
    elif "medium" in consensus_lower:
        subsection = "### Medium Consensus"
    elif "partial" in consensus_lower:
        subsection = "### Partial Consensus (hypothesis under evaluation)"
    elif "low" in consensus_lower:
        subsection = "### Low Consensus (use with caution)"
    else:
        # Default to Medium
        subsection = "### Medium Consensus"

    # Find subsection
    subsection_pattern = re.escape(subsection) + r"\s*\n"
    subsection_match = re.search(subsection_pattern, section)

    if not subsection_match:
        raise ValueError(f"Consensus subsection not found: {subsection}")

    subsection_start = subsection_match.end()

    # Find next subsection or end
    next_subsection = re.search(r"\n###\s+", section[subsection_start:])
    if next_subsection:
        subsection_end = subsection_start + next_subsection.start()
    else:
        subsection_end = len(section)

    # Create new entry line
    keywords_str = ", ".join(entry.keywords[:3])  # Show first 3 keywords
    new_entry_line = (
        f"- [{entry.title}]({entry.path}) — "
        f"{entry.topic} — {keywords_str}\n"
    )

    # Insert at beginning of subsection (after blank line if exists)
    subsection_content = section[subsection_start:subsection_end]
    lines = subsection_content.split("\n")

    # Skip leading blank lines
    insert_idx = 0
    while insert_idx < len(lines) and not lines[insert_idx].strip():
        insert_idx += 1

    lines.insert(insert_idx, new_entry_line.rstrip())
    new_subsection_content = "\n".join(lines)

    new_section = (
        section[:subsection_start]
        + new_subsection_content
        + section[subsection_end:]
    )

    return content[:start_pos] + new_section + content[end_pos:]


def _update_keyword_index(content: str, entry: CatalogEntry) -> str:
    """Update the Keyword Index with entries for each keyword.

    Args:
        content: Current CATALOG.md content.
        entry: Catalog entry to add.

    Returns:
        Updated content.
    """
    boundaries = _find_section_boundaries(content, "## Keyword Index")
    if not boundaries:
        raise ValueError("Keyword Index section not found in CATALOG.md")

    start_pos, end_pos = boundaries
    section = content[start_pos:end_pos]

    # For each keyword, find or create subsection
    for keyword in entry.keywords:
        keyword_header = f"### {keyword}"
        keyword_pattern = re.escape(keyword_header) + r"\s*\n"
        keyword_match = re.search(keyword_pattern, section)

        new_entry_line = f"- [{entry.title}]({entry.path})\n"

        if keyword_match:
            # Keyword section exists, add entry
            keyword_start = keyword_match.end()

            # Find next keyword or end
            next_keyword = re.search(r"\n###\s+", section[keyword_start:])
            if next_keyword:
                keyword_end = keyword_start + next_keyword.start()
            else:
                keyword_end = len(section)

            # Insert entry (after blank line if exists)
            keyword_content = section[keyword_start:keyword_end]
            lines = keyword_content.split("\n")

            # Skip leading blank lines
            insert_idx = 0
            while insert_idx < len(lines) and not lines[insert_idx].strip():
                insert_idx += 1

            lines.insert(insert_idx, new_entry_line.rstrip())
            new_keyword_content = "\n".join(lines)

            section = (
                section[:keyword_start]
                + new_keyword_content
                + section[keyword_end:]
            )
        else:
            # Keyword section doesn't exist, create it
            # Find alphabetical insertion point
            keyword_headers = list(re.finditer(r"\n### ([^\n]+)", section))

            insert_pos = None
            for header_match in keyword_headers:
                existing_keyword = header_match.group(1).strip()
                if keyword.lower() < existing_keyword.lower():
                    insert_pos = header_match.start()
                    break

            if insert_pos is None:
                # Add at end
                insert_pos = len(section) - 1

            new_keyword_block = (
                f"\n### {keyword}\n" + new_entry_line + "\n"
            )

            section = section[:insert_pos] + new_keyword_block + section[insert_pos:]

    return content[:start_pos] + section + content[end_pos:]


def _update_recently_added(content: str, entry: CatalogEntry) -> str:
    """Update the Recently Added section with a new entry at the top.

    Args:
        content: Current CATALOG.md content.
        entry: Catalog entry to add.

    Returns:
        Updated content.
    """
    boundaries = _find_section_boundaries(content, "## Recently Added")
    if not boundaries:
        raise ValueError("Recently Added section not found in CATALOG.md")

    start_pos, end_pos = boundaries
    section = content[start_pos:end_pos]

    # Find table start (skip header and separator)
    lines = section.split("\n")

    # Find where to insert (after table header)
    insert_idx = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("|---"):
            insert_idx = i + 1
            break

    # Create new row
    new_row = f"| {entry.date} | [{entry.title}]({entry.path}) | {entry.topic} |"

    lines.insert(insert_idx, new_row)
    new_section = "\n".join(lines)

    return content[:start_pos] + new_section + content[end_pos:]


def update_catalog(catalog_path: Path, entry: CatalogEntry) -> None:
    """Update all sections of CATALOG.md with a new entry.

    Updates:
    - Quick Reference table
    - By Topic section
    - By Consensus section
    - Keyword Index
    - Recently Added section

    Args:
        catalog_path: Path to CATALOG.md file.
        entry: Catalog entry to add.

    Raises:
        FileNotFoundError: If CATALOG.md doesn't exist.
        ValueError: If any required section is missing.
    """
    if not catalog_path.exists():
        raise FileNotFoundError(f"CATALOG.md not found: {catalog_path}")

    content = catalog_path.read_text(encoding="utf-8")

    # Update each section in sequence
    content = _update_quick_reference(content, entry)
    content = _update_by_topic(content, entry)
    content = _update_by_consensus(content, entry)
    content = _update_keyword_index(content, entry)
    content = _update_recently_added(content, entry)

    # Update metadata at top (total artifacts count)
    # Pattern: _Total artifacts: NN_
    total_pattern = r"_Total artifacts: (\d+)_"
    match = re.search(total_pattern, content)
    if match:
        current_count = int(match.group(1))
        new_count = current_count + 1
        content = re.sub(
            total_pattern, f"_Total artifacts: {new_count}_", content
        )

    # Update last updated timestamp
    today = datetime.now().strftime("%Y-%m-%d")
    updated_pattern = r"_Last updated: [^_]+_"
    content = re.sub(updated_pattern, f"_Last updated: {today}_", content)

    # Write atomically
    temp_path = catalog_path.with_suffix(".md.tmp")
    temp_path.write_text(content, encoding="utf-8")
    temp_path.replace(catalog_path)
