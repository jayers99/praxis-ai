# Research Library

_Canonical knowledge repository for Praxis._

## Authority

This library contains **approved research artifacts**. Research is **explanatory** (non-binding) — it informs core specifications but does not override them.

## For Agents: How to Use This Library

### Finding Research

1. **Start with CATALOG.md** — Master index of all artifacts
2. **Browse by topic** — Each topic folder has `_index.md`
3. **Search by keyword** — CATALOG.md has keyword index
4. **Filter by consensus** — High/Medium/Low ratings indicate confidence

### Retrieval Patterns

| Need | Action |
|------|--------|
| Specific artifact by ID | Search CATALOG.md Quick Reference |
| Browse a topic area | Read `{topic}/_index.md` |
| Find by keyword | Search CATALOG.md Keyword Index |
| High-confidence only | Read CATALOG.md "By Consensus" → High |
| Related artifacts | Read artifact → check `related:` field |

### Reading Artifacts

Each artifact has:
- **Metadata block** — YAML in HTML comment at top
- **Executive Summary** — Key findings (≤10 bullets)
- **Consensus Rating** — High/Medium/Low with justification
- **Body** — First principles, findings, dissenting views
- **Reusable Artifacts** — Tables, checklists, schemas
- **Sources** — Numbered citations

### When to Use Research

| Phase | Research Role |
|-------|---------------|
| Explore | Primary — gather information |
| Shape | Consulted — inform options |
| Decide | Consulted — support decisions |
| Execute | Forbidden — no new research |
| Review | Consulted — retrospective analysis |

## Structure

```
research-library/
├── README.md           # This file
├── CATALOG.md          # Master index
├── foundations/        # Theoretical grounding, first principles
├── spec/               # Research behind specifications
├── roles/              # Roles subsystem research
├── patterns/           # Reusable patterns and practices
├── subagents/          # Subagent design research
└── domain/             # Domain-specific research
```

## Metadata Schema

All artifacts use this schema in YAML frontmatter:

```yaml
<!--
metadata:
  id: {topic}-{slug}-{YYYY-MM-DD}    # Unique identifier
  title: string                       # Human-readable title
  date: YYYY-MM-DD                    # Creation date
  status: approved                    # draft|review|approved|superseded
  topic: string                       # Primary topic (folder location)
  also_relevant: [string]             # Secondary topics (cross-listed)
  keywords: [string]                  # 3-7 searchable terms
  consensus: high|medium|low          # Confidence rating
  sources_count: integer              # Number of citations
  related: [string]                   # IDs of related artifacts
  supersedes: string                  # ID of prior version (if any)
-->
```

## Adding Research (For Agents)

Research follows a lifecycle:

```
bench/research/     →    review      →    approved     →    research-library/
   (draft)              (red-team,        (human)            (cataloged)
                         synthesis)
```

### On Approval

1. Move file to `research-library/{topic}/`
2. Rename: drop date suffix (date stays in metadata)
3. Update metadata: `status: approved`, add `approved_date`
4. Add to CATALOG.md (Quick Reference, By Topic, Keywords)
5. Update `{topic}/_index.md`
6. If `also_relevant:` exists: update secondary indexes
7. If supersedes: update old artifact's `superseded_by` field

## Keyword Vocabulary

Use keywords from the seed list when applicable. See CATALOG.md for current keyword index.

Core keywords: `knowledge-management`, `research-library`, `findability`, `metadata`, `lifecycle`, `governance`, `retrieval`, `cataloging`, `atomicity`, `connections`, `consensus`

## Related

- `../research/` — Legacy research (pending migration)
- `../../bench/research/` — Staging area for draft research

---

_Maintained by: research-librarian (librarian function)_
