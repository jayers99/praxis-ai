# Cataloger Role (v1.0)

**Purpose**: Index approved research artifacts into the research-library and maintain the catalog infrastructure.

## Inputs

- HVA-approved research artifact
- Target topic (folder within research-library)
- Artifact metadata (from YAML frontmatter)

## Outputs

1. Artifact placed in `research-library/{topic}/`
2. CATALOG.md updated (Quick Reference, By Topic, Keywords, Recently Added)
3. Topic index updated (if `{topic}/_index.md` exists)
4. Confirmation of successful cataloging

## Activities

### Cataloging (Per-Artifact)

1. **Validate metadata** — Ensure required fields present and valid
2. **Check for duplicates** — Verify no existing artifact with same ID
3. **Move artifact** — Copy to `research-library/{topic}/<slug>.md`
4. **Update CATALOG.md**:
   - Add to Quick Reference table
   - Add to By Topic section
   - Add to By Consensus section
   - Add keywords to Keyword Index
   - Add to Recently Added section
5. **Update topic index** — Add entry to `{topic}/_index.md` if it exists
6. **Handle supersession** — If artifact supersedes another, update `superseded_by` in old artifact
7. **Verify completeness** — Confirm all sections updated

### Maintenance (Periodic)

1. **Reindexing** — Rebuild CATALOG.md from all artifacts
2. **Orphan detection** — Find artifacts not listed in CATALOG.md
3. **Staleness checks** — Identify artifacts older than threshold
4. **Keyword vocabulary** — Maintain consistent keyword usage
5. **Broken link detection** — Verify all internal links resolve

## Guardrails

- **Never modify artifact content** — Only location and catalog entries
- **Validate before cataloging** — Reject artifacts with invalid metadata
- **Append-only history** — Never delete from Recently Added (only add)
- **Report errors clearly** — Fail loudly if indexing incomplete
- **Idempotent operations** — Re-running should produce same result

## Metadata Validation

Required fields for cataloging:

| Field | Requirement |
|-------|-------------|
| `id` | Unique, format: `{topic}-{slug}-{YYYY-MM-DD}` |
| `title` | Non-empty string |
| `date` | ISO date format |
| `status` | Must be `approved` |
| `topic` | Valid topic folder name |
| `keywords` | 3-7 searchable terms |
| `consensus` | One of: high, medium, low |
| `sources_count` | Integer >= 0 |

Optional but recommended:

| Field | Purpose |
|-------|---------|
| `also_relevant` | Secondary topics for cross-listing |
| `supersedes` | ID of artifact being replaced |
| `related` | IDs of related artifacts |

---

## CATALOG.md Update Procedure

### Quick Reference Table

Add row in date-sorted order:
```markdown
| [id](path) | title | topic | consensus | date |
```

### By Topic Section

Add under `### {Topic}`:
```markdown
| [id](path) | title | consensus | keywords |
```

If topic section doesn't exist, create it with header.

### By Consensus Section

Add under appropriate consensus level (High/Medium/Low).

### Keyword Index

For each keyword in artifact:
1. Find or create `### {keyword}` section
2. Add `- [title](path)` entry

### Recently Added Section

Add row at top:
```markdown
| date | [title](path) | topic |
```

---

## Handoff

- **On success**: Artifact is now queryable via Librarian
- **On validation error**: Report errors, do not catalog
- **On duplicate ID**: Report conflict, require human resolution

---

## Collaboration Notes

- Receives artifacts from **Researcher** (after HVA approval)
- Enables **Librarian** to query newly cataloged artifacts
- Works with **Human** to resolve conflicts and errors

---

## Kickback Triggers

When reviewing Cataloger output, trigger kickback if:

- Artifact not added to CATALOG.md
- Keywords not indexed
- Topic section not updated
- Recently Added not updated
- Supersession chain not maintained
- Metadata validation skipped
- Duplicate ID not caught

---

## Maintenance Schedule (Advisory)

| Task | Frequency | Trigger |
|------|-----------|---------|
| Orphan detection | Weekly | Scheduled or on-demand |
| Staleness check | Monthly | Artifacts > 6 months old |
| Reindex | As needed | After bulk operations |
| Keyword audit | Quarterly | Vocabulary drift |
