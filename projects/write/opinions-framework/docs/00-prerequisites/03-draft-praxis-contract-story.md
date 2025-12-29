# Story: Draft Praxis-Opinions Contract

**Project:** opinions-framework  
**Size:** Small  
**Priority:** High (prerequisite for opinion structure)  
**Depends on:** 01-refine-lifecycle, 02-refine-domains

### Budget (by size)

| Size | Time Box | AI Credit Budget |
|------|----------|------------------|
| **Small** | **30 min** | **~20 queries** |
| Medium | 60 min | ~50 queries |
| Large | 120 min | ~100 queries |

*This story is Small.*

---

## Summary

Create a **draft** contract between opinions and Praxis — enough to enable the opinion structure story, but not finalized until after structure is validated.

---

## Problem Statement

We need enough contract definition to write opinion files, but finalizing the contract before testing the structure is premature.

**Draft contract provides:**
- File structure convention
- Basic schema
- Inheritance concept

**Finalized contract adds (later):**
- Refined schema based on real opinions
- CLI integration design
- AI agent integration pattern
- Edge cases and error handling

---

## Acceptance Criteria (Draft)

- [ ] File location convention defined (`docs/opinions/`)
- [ ] Basic folder structure defined
- [ ] Opinion frontmatter schema drafted (required fields only)
- [ ] Inheritance concept documented (not algorithm)
- [ ] `praxis.yaml` subtype field documented
- [ ] Draft is marked as "provisional, subject to refinement"

---

## Draft Contract Components

### 1. File Location

**Convention:** `docs/opinions/` at repo root

```
docs/opinions/
├── _shared/                    # Cross-domain principles
├── code/                       # Code domain
│   ├── README.md               # Domain-level opinions
│   ├── capture.md              # Stage-specific
│   └── subtypes/               # Subtype opinions
│       └── cli/
├── write/
├── create/
├── learn/
└── observe/
```

### 2. Opinion File Format

**Format:** Markdown with YAML frontmatter

```markdown
---
domain: code
stage: capture          # Optional: omit for domain-wide
subtype: cli            # Optional: omit for domain-wide
version: 1.0
status: draft           # draft | active | deprecated
---

# [Domain] × [Stage] Opinions

## Principles

## Quality Gates

## Anti-Patterns

## Stage Transition Guidance
```

### 3. Inheritance Concept

Opinions inherit from general → specific:

```
_shared → domain → stage → subtype
```

Example resolution for `code/cli` project in `capture`:
1. `_shared/first-principles.md`
2. `code/README.md`
3. `code/capture.md`
4. `code/subtypes/cli/README.md`
5. `code/subtypes/cli/capture.md` (if exists)

### 4. praxis.yaml Extension

```yaml
domain: code
stage: capture
privacy_level: public
environment: Home
subtype: cli            # NEW: enables subtype opinion resolution
```

---

## Tasks

1. [ ] Document file location convention
2. [ ] Document folder structure
3. [ ] Document basic frontmatter schema
4. [ ] Document inheritance concept
5. [ ] Document praxis.yaml subtype
6. [ ] Create `docs/opinions-contract-draft.md`
7. [ ] Mark as provisional

---

## Non-Goals (Deferred to 04.5)

- CLI integration design
- AI agent integration pattern
- Detailed merge algorithm
- Error handling
- Edge cases
- Conflict resolution rules

---

## Output

**File:** `projects/write/opinions-framework/docs/opinions-contract-draft.md`

This draft enables:
- Opinion authors to start writing files
- Structure story to use realistic format
- Refinement based on actual usage

---

## Agent Instructions

1. Read this story completely
2. Execute the tasks respecting the 30-minute time box
3. Create the output file at `projects/write/opinions-framework/docs/opinions-contract-draft.md`
4. Include all contract components from this story
5. Mark as "DRAFT - Provisional, subject to refinement"
6. Commit changes to your branch with message: `docs: draft praxis-opinions contract`
7. Create a PR with handoff summary:
   ```
   gh pr create --title "Story 03: Draft Praxis-Opinions Contract" --body-file <handoff.md> --base main
   ```
8. Include "Closes #XX" in your PR body

---

## Handoff Template

```markdown
## Summary
What you created and key decisions

## Files Changed
- List of files created/modified

## Decisions Made
- Key choices and rationale

## Open Questions
- What remains unknown or needs validation

## Time Spent
- Actual time vs budget

## Follow-Up Needed
- What 04.5 should refine

Closes #XX
```

---

## Definition of Done

- [ ] Contract draft document created
- [ ] All acceptance criteria addressed
- [ ] Marked as provisional
- [ ] Time box respected
- [ ] PR created with handoff

---

## Next Step

After 04-opinion-structure story validates the format, story 04.5 will finalize the contract with:
- Refined schema based on real opinions
- CLI commands specified
- AI integration specified
- Full inheritance algorithm
