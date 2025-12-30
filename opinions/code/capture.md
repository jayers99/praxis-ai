---
domain: code
stage: capture
version: "1.0"
status: draft
---

# Code × Capture Opinions

> **Summary:** Opinions for the initial capture phase of code projects — collecting ideas, requirements, bug reports, and inspiration before any commitment.

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
- **Rationale:** Premature filtering loses valuable ideas; capture velocity matters
- **Source:** GTD (David Allen), Zettelkasten (Luhmann)
- **Severity:** must-have

### 2. Location Over Organization

- **Statement:** Storing matters more than categorizing at this stage
- **Rationale:** Perfect organization slows capture velocity
- **Source:** Building a Second Brain (Forte)
- **Severity:** should-have

### 3. Context is Cheap Now, Expensive Later

- **Statement:** Add minimal context (why, source, date) during capture
- **Rationale:** Future self won't remember why something mattered
- **Source:** Praxis philosophy
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

### Premature Solution Design

- **What:** Jumping to architecture or implementation during capture
- **Why bad:** Skips understanding the problem; wastes effort on wrong solution
- **Instead:** Capture the problem statement; defer solution to Shape

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
- Extract key points from long captures

### What AI Should Ask About

- Whether to proceed with more detailed organization
- Whether this relates to existing projects

### What AI Should Avoid

- Auto-generating code or solutions beyond what was captured
- Making commitment decisions (that's Commit stage)
- Extensive formatting or structuring (that's Sense stage)
- Discarding or filtering inputs

## Code-Specific Capture Examples

| Input Type | Capture Location | Minimal Context |
|------------|------------------|-----------------|
| Bug report | Issue tracker | Reproduction steps, error message |
| Feature idea | `scratch/ideas/` or issue | Problem it solves, user story |
| Technical spike | `scratch/spikes/` | Question being answered |
| Dependency update | Issue tracker | Motivation, breaking changes |
| Refactoring idea | `TODO` comment or issue | Smell identified, direction |

## References

- [Getting Things Done](https://gettingthingsdone.com/) — David Allen
- [Building a Second Brain](https://fortelabs.com/blog/basboverview/) — Tiago Forte
- [Zettelkasten Method](https://zettelkasten.de/) — Niklas Luhmann

---

*Last updated: 2025-12-28*
