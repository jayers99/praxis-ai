# Praxis Opinions Contract (DRAFT)

> **STATUS: DRAFT — Provisional, subject to refinement after opinion structure validation**

**Version:** 0.1.0-draft  
**Date:** 2025-12-28  
**Depends on:** Lifecycle research (complete), Domains research (complete)

---

## 1. Overview

This document defines the contract between the Praxis opinions framework and the Praxis policy engine. It specifies:
- Where opinion files live
- What format they follow
- How inheritance works
- How projects declare their type

---

## 2. File Location Convention

**Root location:** `docs/opinions/` at the repository root

```
docs/opinions/
├── _shared/                        # Cross-domain principles (always apply)
│   └── first-principles.md
│
├── code/                           # Code domain
│   ├── README.md                   # Domain overview and index
│   ├── principles.md               # Domain principles (apply to ALL stages)
│   ├── capture.md                  # Stage: Capture
│   ├── sense.md                    # Stage: Sense
│   ├── explore.md                  # Stage: Explore
│   ├── shape.md                    # Stage: Shape
│   ├── formalize.md                # Stage: Formalize
│   ├── commit.md                   # Stage: Commit
│   ├── execute.md                  # Stage: Execute
│   ├── sustain.md                  # Stage: Sustain
│   ├── close.md                    # Stage: Close
│   └── subtypes/
│       ├── cli/
│       │   ├── README.md           # CLI-specific opinions
│       │   ├── principles.md       # CLI principles (all CLI stages)
│       │   └── python/
│       │       └── README.md       # CLI-Python specific
│       ├── library/
│       ├── api/
│       ├── webapp/
│       ├── infrastructure/
│       └── script/
│
├── create/
│   ├── README.md
│   ├── principles.md               # Create domain principles
│   └── subtypes/
│       ├── visual/
│       ├── audio/
│       ├── video/
│       ├── interactive/
│       ├── generative/
│       └── design/
│
├── write/
│   ├── README.md
│   ├── principles.md               # Write domain principles
│   └── subtypes/
│       ├── technical/
│       ├── business/
│       ├── narrative/
│       ├── academic/
│       └── journalistic/
│
├── learn/
│   ├── README.md
│   ├── principles.md               # Learn domain principles
│   └── subtypes/
│       ├── skill/
│       ├── concept/
│       ├── practice/
│       ├── course/
│       └── exploration/
│
└── observe/
    ├── README.md
    ├── principles.md               # Observe domain principles
    └── subtypes/
        ├── notes/
        ├── bookmarks/
        ├── clips/
        ├── logs/
        └── captures/
```

---

## 3. Opinion File Format

**Format:** Markdown with YAML frontmatter

### 3.1 Frontmatter Schema (Required Fields)

```yaml
---
domain: code                    # Required: code | create | write | learn | observe
version: "1.0"                  # Required: semver string
status: draft                   # Required: draft | active | deprecated
---
```

### 3.2 Frontmatter Schema (Optional Fields)

```yaml
---
stage: capture                  # Optional: restrict to specific stage
subtype: cli                    # Optional: restrict to subtype
inherits:                       # Optional: explicit inheritance override
  - code
  - code/subtypes/cli
author: human                   # Optional: human | ai | hybrid
last_reviewed: 2024-12-28       # Optional: freshness indicator
---
```

### 3.3 Body Structure

```markdown
# [Domain] × [Stage] Opinions

## Principles

Guiding principles for this domain/stage combination.

1. **Principle Name**
   - Rationale: Why this matters
   - Source: Where this comes from (prior art, research)
   - Severity: must-have | should-have | nice-to-have

## Quality Gates

Conditions that should be satisfied before stage transition.

- [ ] Gate description
- [ ] Gate description

## Anti-Patterns

Things to avoid in this domain/stage.

- **Anti-pattern name:** Why to avoid

## Stage Transition Guidance

When advancing to the next stage:

- [ ] Transition criterion
- [ ] Transition criterion

## AI Guidance

Specific guidance for AI assistants working in this domain/stage.

- What AI can do
- What AI should ask about
- What AI should avoid
```

---

## 4. Inheritance Concept

Opinions inherit from **general → specific**. More specific opinions can:
- Add new principles
- Override parent principles
- Add quality gates

### 4.1 Inheritance Chain

```
_shared → domain/principles → domain/stage → subtype/principles → subtype/stage
```

### 4.2 Example Resolution

For a project with:
```yaml
domain: code
stage: capture
subtype: cli
```

Resolution order:
1. `_shared/first-principles.md`
2. `code/README.md` (domain overview)
3. `code/principles.md` (domain principles — applies to ALL stages)
4. `code/capture.md` (stage-specific)
5. `code/subtypes/cli/README.md` (subtype overview)
6. `code/subtypes/cli/principles.md` (subtype principles — if exists)
7. `code/subtypes/cli/capture.md` (subtype stage — if exists)

**Merge rule (draft):** Later opinions override earlier for conflicts; lists concatenate.

---

## 5. praxis.yaml Extension

Projects declare their type in `praxis.yaml`:

```yaml
# Required (existing)
domain: code
stage: capture
privacy_level: public
environment: Home

# New optional field
subtype: cli                    # Enables subtype opinion resolution
```

### 5.1 Subtype Format

- Simple: `cli` → matches `subtypes/cli/`
- Nested: `cli-python` or `cli.python` → matches `subtypes/cli/python/`

### 5.2 Valid Subtypes by Domain

Based on research (02-refine-domains-research-01-subtype-taxonomies.md):

| Domain | Valid Subtypes |
|--------|----------------|
| code | cli, library, api, webapp, infrastructure, script |
| create | visual, audio, video, interactive, generative, design |
| write | technical, business, narrative, academic, journalistic |
| learn | skill, concept, practice, course, exploration |
| observe | notes, bookmarks, clips, logs, captures |

---

## 6. Stage Reference

Based on research (01-refine-lifecycle-research-merged.md):

| Stage | Purpose | Entry Criteria | Exit Criteria |
|-------|---------|----------------|---------------|
| capture | Collect raw inputs | Any input exists | Input stored |
| sense | Convert to understanding | Captured inputs exist | Problem articulated |
| explore | Generate possibilities | Sense complete | 2-3 directions exist |
| shape | Converge to direction | Options exist | Direction chosen |
| formalize | Create durable artifacts | Shape complete | SOD exists |
| commit | Decide to proceed | SOD complete | Resources allocated |
| execute | Produce artifact | Commit complete | Artifact produced |
| sustain | Maintain delivered work | Execute complete | Work retired/closed |
| close | End intentionally | Sustain complete | Leverage captured |

---

## 7. AI Permissions Reference

Based on research (02-refine-domains-research-03-ai-permissions.md):

| Operation | Code | Create | Write | Learn | Observe |
|-----------|:----:|:------:|:-----:|:-----:|:-------:|
| suggest | ✓ | ✓ | ✓ | ✓ | ✓ |
| complete | ✓ | ✓ | ✓ | ✓ | ✗ |
| generate | ? | ✓ | ? | ✓ | ✗ |
| transform | ? | ✓ | ? | ✓ | ✗ |
| execute | ? | — | — | — | — |
| publish | ? | ? | ? | ? | ? |

**Legend:** ✓ = allowed, ? = ask user, ✗ = blocked, — = N/A

*Note: Observe domain blocks AI generation to preserve raw capture authenticity.*

---

## 8. What This Draft Does NOT Cover

Deferred to Story 04.5 (Finalize Contract):

- [ ] Detailed merge algorithm with edge cases
- [ ] CLI command specifications (`praxis opinions`)
- [ ] AI agent integration pattern
- [ ] Conflict resolution rules
- [ ] Error handling (missing files, invalid yaml)
- [ ] Validation rules
- [ ] Migration strategy for schema changes

---

## 9. Open Questions

1. **Subtype depth:** Should subtypes support further nesting? (e.g., `cli-python-flask`)
2. **Cross-domain opinions:** How to handle projects that span domains?
3. **Opinion versioning:** How to handle breaking changes to opinion files?
4. **Auto-detection:** Can praxis infer subtype from project structure?

---

## 10. Sources

This draft synthesizes research from:
- `01-refine-lifecycle-research-merged.md` — Stage definitions
- `02-refine-domains-research-01-subtype-taxonomies.md` — Subtype taxonomies
- `02-refine-domains-research-02-domain-transitions.md` — Domain transitions
- `02-refine-domains-research-03-ai-permissions.md` — AI permission matrix

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0-draft | 2025-12-28 | Initial draft based on prerequisite research |
