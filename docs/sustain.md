# Praxis Sustain Stage

**File:** sustain.md
**Version:** v0.1
**Purpose:** Define Sustain stage governance, including when to iterate vs. maintain within existing formalization.

---

## Overview

Sustain is the stage where delivered work is maintained, evaluated, and optimized over time. It includes:

- Bug fixes
- Enhancements
- Performance improvements
- Policy enforcement
- Quality improvements

Sustain is **not** a holding pattern—it's active governance of living work.

---

## Iteration vs. Sustain

A key governance question: **When does a change warrant a new iteration (v2) vs. staying in Sustain?**

### The Core Principle

The SOD's purpose is to lock intent without over-specifying implementation. An iteration is needed when the **intent itself changes**, not the implementation.

### The Test

Ask: **"Does this change alter the contract I formalized, or does it extend/refine the implementation of that contract?"**

- **Contract change** → New iteration
- **Implementation extension** → Sustain

---

## Iteration Triggers by SOD Section

Changes to certain SOD sections signal a contract change requiring iteration. Changes to others fit within Sustain.

| Section                               | Change Type | Rationale                                                                    |
| ------------------------------------- | ----------- | ---------------------------------------------------------------------------- |
| **Problem Statement**                 | Iteration   | The problem you're solving has changed or expanded significantly             |
| **Desired Outcomes**                  | Iteration   | Fundamental goals have shifted (not just added goals, but changed direction) |
| **Canonical Dimensions**              | Iteration   | Adding/removing/redefining domains, stages, privacy levels, or environments  |
| **Deterministic Resolution Model**    | Iteration   | The composition order or logic changes                                       |
| **Abandonment Criteria**              | Iteration   | The success/failure definition has changed                                   |
| Risks & Mitigations                   | Sustain     | New risks discovered during execution                                        |
| First Executable Increment            | Sustain     | New increments added                                                         |
| Policy Enforcement details            | Sustain     | Implementation refinements                                                   |
| Privacy/Lifecycle Interaction details | Sustain     | Clarifications, not redefinitions                                            |

### The Heuristic

**If you need to change Problem Statement, Desired Outcomes, or Canonical Dimensions in the SOD, you're starting a new iteration.**

---

## Key Insight: Sustain Absorbs a Lot

Sustain is more flexible than it might appear. Significant work can happen within Sustain:

- Feature additions that fit existing scope
- Quality bar improvements
- Convention/style overlays
- New implementation patterns
- Performance optimization
- Additional policy rules

The iteration trigger is about **contract changes, not scope size**. A massive feature set stays in Sustain if the formalization contract holds. A small conceptual shift requires iteration if it changes the contract.

---

## Worked Project: CLI Ideals vs. template-python-cli

To validate this framework, we tested applying a comprehensive set of CLI quality ideals to an existing project.

### The CLI Ideals

Aspirational qualities for CLI tools:

- Unix philosophy / GNU conventions
- HashiCorp/Docker/AWS UX patterns
- Explicit commands over implicit behavior
- Composability, predictability, script safety
- Backwards compatibility as first-class concern
- Safe for shell pipelines (stdout/stderr separation)
- Meaningful exit codes
- 10+ year maintenance assumption

### The Current SOD Contract

The template-python-cli SOD defines:

- **Problem:** "Developers need a consistent, well-structured starting point for Python CLI projects"
- **Solution:** Reusable template with hexagonal architecture, Poetry, Typer, pytest-bdd
- **Scope:** Template structure, testing patterns, governance files, working project

### Analysis

| CLI Ideal                         | Classification | Rationale                                             |
| --------------------------------- | -------------- | ----------------------------------------------------- |
| Unix philosophy / GNU conventions | Sustain        | Implementation guidance within existing scope         |
| HashiCorp/Docker/AWS UX patterns  | Sustain        | Style conventions, not scope change                   |
| Explicit commands over implicit   | Sustain        | Already implied by architecture choices               |
| Composability, predictability     | Sustain        | Quality bar, not contract change                      |
| Backwards compatibility           | Sustain        | Adding semver documentation fits existing scope       |
| Shell pipeline safety             | Sustain        | stdout/stderr separation is implementation detail     |
| Meaningful exit codes             | Sustain        | Convention layer, easily added                        |
| 10+ year maintenance assumption   | Sustain        | Aspiration, not a scope change to the template itself |

### Result

**None of the CLI ideals trigger iteration.**

The ideals represent a _quality overlay_—they refine _how_ the CLI should behave without changing _what_ the template is trying to solve. The SOD's Problem Statement and Proposed Solution remain unchanged.

### When Would This Become Iteration?

If the 10-year maintenance posture required fundamental additions like:

- Built-in deprecation warning infrastructure
- Version migration tooling
- API stability contract enforcement
- Changelog automation as a core feature

...then collectively these would shift the Problem Statement from "starting point template" to "production longevity framework"—which _would_ warrant a new iteration.

---

## Future: Iteration Model

When a project requires a new iteration (contract change), Praxis will support:

- Iteration numbering in `praxis.yaml`
- Retrospective artifacts documenting what changed and why
- Iteration-aware regression paths

This capability is deferred until a real use case emerges. See [Issue #23](https://github.com/jayers99/praxis-ai/issues/23) for context.

---

## References

- [lifecycle.md](lifecycle.md) — Stage definitions and regression rules
- [formalize.md](formalize.md) — Formalize stage and artifact definitions
- [sod.md](sod.md) — Solution Overview Document specification
