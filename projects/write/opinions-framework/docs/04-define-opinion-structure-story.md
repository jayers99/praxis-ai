# Story: Define Opinion Structure Templates

**Project:** opinions-framework  
**Size:** Medium  
**Priority:** High (foundation for all opinion content)  
**Depends on:** 03-draft-praxis-contract (complete)

### Budget (by size)

| Size | Time Box | AI Credit Budget |
|------|----------|------------------|
| Small | 30 min | ~20 queries |
| **Medium** | **60 min** | **~50 queries** |
| Large | 120 min | ~100 queries |

*This story is Medium.*

---

## Summary

Create templates for each type of opinion file, based on the draft contract and completed research. This ensures consistency before generating the full opinion corpus.

---

## Problem Statement

The draft contract defines WHERE opinions live and WHAT schema they follow. This story defines HOW to write them — what sections, what depth, what examples.

We have **three distinct file types** that need templates:
1. **`README.md`** — Domain/subtype overview and navigation
2. **`principles.md`** — Cross-stage principles (domain or subtype level)
3. **`{stage}.md`** — Stage-specific opinions

Each requires different content and structure.

---

## Context from Research

### Stages (from lifecycle research)

| Stage | Key Opinion Focus |
|-------|-------------------|
| capture | Minimal friction, no commitment, GTD/Zettelkasten patterns |
| sense | Sensemaking, Weick/Cynefin, interpretation |
| explore | Divergent thinking, abandonment safety |
| shape | Convergent thinking, Shape Up patterns |
| formalize | SOD creation, structural hinge |
| commit | Gates with teeth, betting decisions |
| execute | SOD-bounded work, AI governance |
| sustain | Maintenance patterns (varies by domain) |
| close | Retrospectives, knowledge capture |

### Domains & Subtypes (from domains research)

| Domain | Subtypes | Key Opinion Themes |
|--------|----------|-------------------|
| code | cli, library, api, webapp, infrastructure, script | Security, testing, architecture |
| create | visual, audio, video, interactive, generative, design | Copyright, originality, craft |
| write | technical, business, narrative, academic, journalistic | Voice, clarity, accuracy |
| learn | skill, concept, practice, course, exploration | Retention, application, assessment |
| observe | notes, bookmarks, clips, logs, captures | Raw capture, minimal processing |

### AI Permissions (from AI research)

| Domain | AI Role |
|--------|---------|
| code | Suggest/complete allowed; generate/execute requires approval |
| create | Most permissive; full generation allowed |
| write | Suggest allowed; generation requires approval (voice concerns) |
| learn | Permissive; supports exploration |
| observe | Minimal AI; preserve raw capture authenticity |

---

## Acceptance Criteria

- [ ] README template created (domain/subtype overview)
- [ ] principles.md template created (cross-stage principles)
- [ ] Stage file template created (stage-specific opinions)
- [ ] Each template aligns with draft contract schema
- [ ] Templates tested with one real example (Code domain)
- [ ] Agent instructions for using templates
- [ ] Templates stored in `docs/opinions/_templates/`

---

## Template 1: README.md (Domain/Subtype Overview)

**Purpose:** Navigation, scope definition, links to other files

**Location examples:**
- `docs/opinions/code/README.md`
- `docs/opinions/code/subtypes/cli/README.md`

```markdown
---
domain: code
version: "1.0"
status: active
---

# Code Domain Opinions

> **Scope:** Software development projects — applications, tools, infrastructure, scripts.

## Quick Navigation

- [Principles](principles.md) — Cross-stage principles for all Code projects
- Stages:
  - [Capture](capture.md) | [Sense](sense.md) | [Explore](explore.md)
  - [Shape](shape.md) | [Formalize](formalize.md) | [Commit](commit.md)
  - [Execute](execute.md) | [Sustain](sustain.md) | [Close](close.md)
- Subtypes:
  - [CLI](subtypes/cli/) | [Library](subtypes/library/) | [API](subtypes/api/)
  - [WebApp](subtypes/webapp/) | [Infrastructure](subtypes/infrastructure/) | [Script](subtypes/script/)

## Domain at a Glance

| Aspect | Code Domain |
|--------|-------------|
| Primary artifact | Working software |
| Quality signals | Tests pass, builds succeed, reviews approved |
| AI role | Suggest/complete allowed; generate/execute ask |
| Key risks | Security, maintainability, correctness |

## When to Use This Domain

Use **Code** when the primary deliverable is software that:
- Compiles or interprets
- Has automated tests
- Ships to users or other systems

## Related Domains

- **Write** for documentation accompanying code
- **Learn** for skill development related to code

---

*Last updated: {{DATE}}*
```

---

## Template 2: principles.md (Cross-Stage Principles)

**Purpose:** Principles that apply to ALL stages within a domain or subtype

**Location examples:**
- `docs/opinions/code/principles.md`
- `docs/opinions/code/subtypes/cli/principles.md`

```markdown
---
domain: code
version: "1.0"
status: active
---

# Code Domain Principles

> **Scope:** These principles apply across ALL lifecycle stages for Code projects.

## Core Principles

### 1. Correctness Over Cleverness

- **Statement:** Prefer clear, correct code over clever optimizations
- **Rationale:** Clever code is harder to maintain and debug
- **Source:** Clean Code (Martin), KISS principle
- **Severity:** must-have

### 2. Test What Matters

- **Statement:** Cover critical paths, don't chase coverage numbers
- **Rationale:** 100% coverage doesn't mean 100% correct
- **Source:** Kent Beck, Test-Driven Development
- **Severity:** should-have

### 3. Dependencies Are Liabilities

- **Statement:** Every dependency is a risk; add deliberately
- **Rationale:** Dependencies rot, break, and introduce vulnerabilities
- **Source:** Praxis philosophy
- **Severity:** should-have

## AI Guidelines (All Stages)

| Operation | Permission | Notes |
|-----------|------------|-------|
| suggest | ✓ allowed | Always |
| complete | ✓ allowed | In-context completion |
| generate | ? ask | User approval for new files |
| transform | ? ask | Refactoring needs approval |
| execute | ? ask | Never run without approval |

## Anti-Patterns (All Stages)

### Premature Optimization

- **What:** Optimizing before measuring
- **Why bad:** Wastes effort on non-bottlenecks
- **Instead:** Profile first, optimize where it matters

### Cargo Cult Programming

- **What:** Copying patterns without understanding
- **Why bad:** Creates fragile, unmaintainable code
- **Instead:** Understand before applying

---

*Last updated: {{DATE}}*
```

---

## Template 3: {stage}.md (Stage-Specific Opinions)

**Purpose:** Opinions for a specific Domain × Stage combination

**Location examples:**
- `docs/opinions/code/capture.md`
- `docs/opinions/code/subtypes/cli/execute.md`

```markdown
---
domain: code
stage: capture
version: "1.0"
status: active
---

# Code × Capture Opinions

> **Summary:** Opinions for the initial capture phase of code projects — collecting ideas, requirements, and inspiration before any commitment.

## Stage Context

| Aspect | Capture Stage |
|--------|---------------|
| Entry criteria | Any input exists (idea, requirement, bug report) |
| Exit criteria | Input stored in retrievable location |
| Commitment level | None — abandonment is safe |
| AI role | Suggest allowed; generation ask |

## Principles

### 1. Capture Everything, Curate Later

- **Statement:** Don't filter during capture; that's Sense's job
- **Rationale:** Premature filtering loses valuable ideas
- **Source:** GTD (David Allen), Zettelkasten (Luhmann)
- **Severity:** must-have

### 2. Location Over Organization

- **Statement:** Storing matters more than categorizing at this stage
- **Rationale:** Perfect organization slows capture velocity
- **Source:** Building a Second Brain (Forte)
- **Severity:** should-have

## Quality Gates

Before advancing to **Sense**:

| Gate | Description | Severity |
|------|-------------|----------|
| G1 | Input is stored in a searchable location | must-have |
| G2 | Input has minimal metadata (date, source) | should-have |
| G3 | Similar existing items identified (dedup check) | nice-to-have |

## Anti-Patterns

### Analysis Paralysis at Capture

- **What:** Spending too much time organizing or evaluating during capture
- **Why bad:** Slows capture velocity, discourages future captures
- **Instead:** Quick capture, defer organization to Sense

### Capture Without Context

- **What:** Storing a link or snippet with no note on why it matters
- **Why bad:** Future self won't remember relevance
- **Instead:** Add one sentence of context during capture

## Stage Transition Checklist

To advance from **Capture** → **Sense**:

- [ ] Input is stored and retrievable
- [ ] Basic context is attached (date, source, reason)
- [ ] Input is not a duplicate of existing item
- [ ] You've stopped actively capturing for this topic

## AI Guidance

### What AI Can Do

- Suggest tags or categories (user accepts/rejects)
- Identify potential duplicates
- Add metadata from source (author, date, URL)

### What AI Should Ask About

- Whether to proceed with more detailed organization
- Whether this relates to existing projects

### What AI Should Avoid

- Auto-generating content beyond what was captured
- Making commitment decisions (that's Commit stage)
- Extensive formatting or structuring (that's Sense stage)

## References

- [Getting Things Done](https://gettingthingsdone.com/) — David Allen
- [Building a Second Brain](https://fortelabs.com/blog/basboverview/) — Tiago Forte
- [Zettelkasten Method](https://zettelkasten.de/) — Niklas Luhmann

---

*Last updated: {{DATE}}*
```

---

## File Locations

Create templates at:

```
docs/opinions/_templates/
├── README-template.md           # Domain/subtype overview template
├── principles-template.md       # Cross-stage principles template
├── stage-template.md            # Stage-specific opinion template
└── GUIDE.md                     # How to use these templates
```

---

## Tasks

1. [ ] Create `_templates/` directory
2. [ ] Create README template with navigation structure
3. [ ] Create principles template with severity-tagged principles
4. [ ] Create stage template with entry/exit, gates, anti-patterns, AI guidance
5. [ ] Create GUIDE.md explaining when to use each template
6. [ ] Test templates by drafting Code domain files:
   - [ ] `code/README.md`
   - [ ] `code/principles.md`
   - [ ] `code/capture.md`
7. [ ] Refine based on friction encountered
8. [ ] Update draft contract if schema changes needed

---

## Definition of Done

- [ ] Three templates created and stored in `_templates/`
- [ ] GUIDE.md explains template usage
- [ ] At least one real file created from each template
- [ ] Templates align with draft contract schema
- [ ] Time box respected

---

## Agent Instructions

1. Read this story completely
2. Review the draft contract at `docs/opinions-contract-draft.md`
3. Create templates following the structures above
4. Test with Code domain files
5. Document any schema refinements needed
6. Commit with message: `docs: opinion structure templates`
7. Create PR with handoff:
   ```
   gh pr create --title "Story 04: Opinion Structure Templates" --body-file <handoff.md> --base main
   ```

---

## Handoff Template

```markdown
## Summary
Templates created and tested with Code domain examples

## Files Changed
- List of template files created
- List of example opinion files created

## Decisions Made
- Any template refinements from testing
- Schema changes needed for draft contract

## Open Questions
- Friction points discovered
- Suggestions for GUIDE.md

## Time Spent
- Actual vs budget

Closes #XX
```

---

## Dependencies

- 03-draft-praxis-contract (complete ✓)

## Blocks

- 04.5-finalize-praxis-contract (may update based on learnings)
- 05-tracer-bullet (needs templates to follow)
- All opinion research work

---

## Notes

Three templates, not one:
1. **README** = navigation (what's here, where to go)
2. **principles** = beliefs (apply across stages)
3. **stage** = actions (specific to stage)

This distinction emerged from the inheritance model in the draft contract.
