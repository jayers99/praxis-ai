# Story: Define Opinions ↔ Praxis Contract

**Project:** opinions-framework  
**Size:** Medium  
**Priority:** High (architectural foundation)  
**Depends on:** 01-refine-lifecycle-story, 02-refine-domains-story

---

## Summary

Define the interface contract between the opinions framework and the Praxis policy engine:
1. What artifact shape does Praxis expect from opinions?
2. How are opinions discovered and loaded?
3. How does inheritance resolution work?

---

## Problem Statement

Without a defined contract, opinion research may produce artifacts that don't integrate with Praxis. The contract must be explicit before generating content.

**Key questions:**
- What file structure does Praxis expect?
- What schema/format must opinion files follow?
- How does Praxis resolve which opinions apply to a given project?

---

## Acceptance Criteria

- [ ] File structure convention is defined (where opinions live, naming)
- [ ] Opinion file schema is defined (required fields, format)
- [ ] Inheritance resolution is defined (domain → subtype → specific)
- [ ] `praxis.yaml` extensions are defined (how to declare subtype)
- [ ] CLI integration is sketched (`praxis opinions` behavior)
- [ ] AI agent integration is sketched (how agents discover opinions)
- [ ] Contract is documented in a dedicated spec file

---

## Contract Components

### 1. File Structure Convention

**Proposed location:** `docs/opinions/`

```
docs/opinions/
├── _shared/                    # Cross-domain principles
│   └── first-principles.md
│
├── code/                       # Code domain
│   ├── README.md               # Domain-level opinions
│   ├── capture.md              # Stage-specific
│   ├── sense.md
│   ├── ...
│   └── subtypes/
│       ├── cli/
│       │   ├── README.md       # CLI-specific opinions
│       │   └── python/
│       │       └── README.md   # CLI-Python specific
│       └── api/
│           └── rest/
│               └── README.md
│
├── write/
│   ├── README.md
│   ├── capture.md
│   └── subtypes/
│       └── technical/
│           └── README.md
│
└── ...
```

### 2. Opinion File Schema

**Proposed format:** Markdown with YAML frontmatter

```markdown
---
domain: code
stage: capture          # Optional: omit for domain-wide
subtype: cli-python     # Optional: omit for domain-wide
inherits:
  - code
  - code/subtypes/cli
version: 1.0
---

# Code × Capture Opinions

## First Principles

1. **Principle name**
   - Rationale: Why this matters
   - Source: Where this comes from
   - Severity: must-have | should-have | nice-to-have

## Quality Gates

- [ ] Gate 1: Description
- [ ] Gate 2: Description

## Anti-Patterns

- **Anti-pattern name:** Why to avoid

## Stage Transition Guidance

When ready to advance to Sense:
- Checklist item 1
- Checklist item 2
```

### 3. Inheritance Resolution

When Praxis evaluates opinions for a project:

```
Input: praxis.yaml
  domain: code
  subtype: cli-python
  stage: capture

Resolution order (most general → most specific):
1. docs/opinions/_shared/first-principles.md
2. docs/opinions/code/README.md
3. docs/opinions/code/capture.md
4. docs/opinions/code/subtypes/cli/README.md
5. docs/opinions/code/subtypes/cli/python/README.md
```

**Merge strategy:** Later files override earlier for conflicting keys; lists are concatenated.

### 4. praxis.yaml Extensions

```yaml
domain: code
stage: capture
privacy_level: public
environment: Home
subtype: cli-python      # NEW: optional, enables subtype resolution
```

**Subtype format:** Slash-separated path matching folder structure.
- `cli` → `subtypes/cli/`
- `cli-python` or `cli/python` → `subtypes/cli/python/`

### 5. CLI Integration

```bash
# Show applicable opinions for current project
praxis opinions

# Generate AI prompt with opinion context
praxis opinions --prompt

# Validate current work against opinion gates
praxis opinions --check

# List all available opinion files
praxis opinions --list
```

### 6. AI Agent Integration

Agents should be instructed (via CLAUDE.md or similar):

```markdown
## Opinions

When working on a Praxis project:
1. Read `praxis.yaml` to determine domain, stage, subtype
2. Load applicable opinions from `docs/opinions/`
3. Apply inheritance: _shared → domain → stage → subtype
4. Use opinions to guide decisions and quality checks
```

---

## Tasks

1. [ ] Draft file structure convention
2. [ ] Draft opinion file schema (frontmatter + sections)
3. [ ] Define inheritance resolution algorithm
4. [ ] Define `praxis.yaml` subtype field
5. [ ] Sketch CLI commands (`praxis opinions`)
6. [ ] Sketch AI agent integration pattern
7. [ ] Document contract in `docs/opinions-contract.md`
8. [ ] Review with stakeholder

---

## Non-Goals

- Not implementing CLI (that's policy engine work)
- Not generating opinion content (that's later stories)
- Not building the inheritance resolver (that's code)

---

## Dependencies

- 01-refine-lifecycle-story (stages must be clear)
- 02-refine-domains-story (domains/subtypes must be clear)

## Blocks

- 04-define-opinion-structure
- 05-tracer-bullet
- All opinion research work

---

## Notes

This story addresses the concern: "I think one of the early tickets should be to define the contract between the opinions, structure, and Praxis."

The contract enables:
1. Opinion authors to know what format to produce
2. Praxis to know how to discover and load opinions
3. AI agents to know how to apply opinions
