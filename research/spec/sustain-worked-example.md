# Worked Example: Iteration vs. Sustain Decision

**File:** sustain-worked-example.md
**Purpose:** Validate the iteration vs. sustain framework using a real project.

---

## Context

This worked example tests the iteration vs. sustain governance framework against an actual project to validate its utility.

---

## Project: CLI Ideals vs. template-python-cli

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

## References

- [lifecycle.md](../../core/spec/lifecycle.md) — Stage definitions including Sustain governance
- [sod.md](../../core/spec/sod.md) — Solution Overview Document specification
