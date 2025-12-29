# Story: Define Opinion Folder Structure Template

**Project:** opinions-framework  
**Size:** Small  
**Priority:** High (template for all opinions)  
**Depends on:** 03-define-praxis-contract-story

---

## Summary

Create a template that defines what a "complete" opinion folder looks like for any Domain × Stage cell. This template will guide all opinion research and ensure consistency.

---

## Problem Statement

Before generating 45+ opinion files, we need a template that:
- Defines required vs. optional sections
- Ensures consistent structure across all cells
- Makes opinions machine-parseable for Praxis integration

---

## Acceptance Criteria

- [ ] Template file created with all required sections
- [ ] Each section has clear purpose and example content
- [ ] Template follows the schema defined in 03-define-praxis-contract
- [ ] Template is usable by both humans and AI agents
- [ ] Template includes guidance for must-have vs. nice-to-have tagging
- [ ] Template is validated against at least one real example

---

## Proposed Template

**File:** `docs/opinions/_template/opinion-template.md`

```markdown
---
domain: {{DOMAIN}}
stage: {{STAGE}}                    # Omit for domain-wide opinions
subtype: {{SUBTYPE}}                # Omit for domain/stage-wide opinions
inherits:                           # List parent opinion files
  - {{DOMAIN}}
  - {{DOMAIN}}/subtypes/{{PARENT}}
version: 1.0
last_updated: {{DATE}}
---

# {{DOMAIN}} × {{STAGE}} Opinions

> **Summary:** One-sentence description of what this opinion file covers.

---

## First Principles

Core beliefs that guide work in this cell. Tagged by severity.

### 1. {{Principle Name}}

- **Statement:** Clear, actionable principle
- **Rationale:** Why this matters
- **Source:** Key influencer or research backing this
- **Severity:** `must-have` | `should-have` | `nice-to-have`

### 2. {{Principle Name}}

...

---

## Quality Gates

Checkpoints that should be satisfied before advancing to the next stage.

| Gate | Description | Severity |
|------|-------------|----------|
| G1 | {{Description}} | must-have |
| G2 | {{Description}} | should-have |

---

## Anti-Patterns

What to avoid at this stage. Common mistakes and why they're problematic.

### {{Anti-Pattern Name}}

- **Description:** What it looks like
- **Why it's bad:** Consequences
- **Instead:** What to do instead

---

## Stage Transition Checklist

Before advancing from {{STAGE}} to {{NEXT_STAGE}}:

- [ ] {{Checklist item 1}}
- [ ] {{Checklist item 2}}
- [ ] {{Checklist item 3}}

---

## AI Guidance

Specific instructions for AI agents working in this cell.

### Recommended Prompts

```
{{Example prompt for AI to use at this stage}}
```

### Watch For

- {{Common AI mistake at this stage}}
- {{Another thing AI should avoid}}

---

## References

- [Source 1](url) — Brief description
- [Source 2](url) — Brief description

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | {{DATE}} | Initial version |
```

---

## Template Sections Explained

| Section | Required? | Purpose |
|---------|-----------|---------|
| Frontmatter | Yes | Machine-readable metadata for Praxis |
| Summary | Yes | Quick orientation |
| First Principles | Yes | Core beliefs with severity tags |
| Quality Gates | Yes | Pre-advancement checklist |
| Anti-Patterns | Yes | What to avoid |
| Stage Transition | Yes | Explicit advancement criteria |
| AI Guidance | Optional | Specific AI agent instructions |
| References | Optional | Source attribution |
| Changelog | Optional | Version tracking |

---

## Tasks

1. [ ] Create template file at `docs/opinions/_template/opinion-template.md`
2. [ ] Create section-by-section writing guide
3. [ ] Test template by drafting one real opinion (Code × Capture)
4. [ ] Refine based on friction encountered
5. [ ] Document in contract spec

---

## Non-Goals

- Not filling in opinions (that's tracer bullet and later)
- Not creating all 45 opinion files
- Not implementing Praxis parsing of opinions

---

## Dependencies

- 03-define-praxis-contract-story (schema must be settled)

## Blocks

- 05-tracer-bullet (needs template to follow)
- All opinion research work

---

## Notes

This is a small but critical story. The template ensures:
1. Consistency across all opinion files
2. Machine-parseability for Praxis integration
3. Clear guidance for opinion authors (human or AI)
