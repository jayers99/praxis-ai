# Worked Example: Iteration vs. Sustain Decision

<!--
metadata:
  id: spec-sustain-worked-example-2025-12-28
  title: Worked Example - Iteration vs Sustain Decision
  date: 2025-12-28
  author: research-librarian
  status: approved
  topic: spec
  also_relevant: []
  keywords: [sustain, iteration, worked-example, cli, governance]
  consensus: medium
  epistemic_standard: example
  sources_count: 0
  supersedes: null
  related: [spec-lifecycle-research-2025-12-28]
  approved_by: human
  approved_date: 2025-12-30
-->

## Executive Summary

- Worked example testing iteration vs. sustain framework against a real project
- Result: CLI ideals represent a quality overlay, not scope change — stays in Sustain
- Key insight: Changes that improve *how* without changing *what* remain in Sustain
- Transition to Iteration requires changing the Problem Statement

## Consensus Rating

**Medium**: Illustrative example. Useful for understanding the governance framework but specific to one project.

## Body

### Context

This worked example tests the iteration vs. sustain governance framework against an actual project to validate its utility.

### Project: CLI Ideals vs. template-python-cli

#### The CLI Ideals

Aspirational qualities for CLI tools:

- Unix philosophy / GNU conventions
- HashiCorp/Docker/AWS UX patterns
- Explicit commands over implicit behavior
- Composability, predictability, script safety
- Backwards compatibility as first-class concern
- Safe for shell pipelines (stdout/stderr separation)
- Meaningful exit codes
- 10+ year maintenance assumption

#### The Current SOD Contract

The template-python-cli SOD defines:

- **Problem:** "Developers need a consistent, well-structured starting point for Python CLI projects"
- **Solution:** Reusable template with hexagonal architecture, Poetry, Typer, pytest-bdd
- **Scope:** Template structure, testing patterns, governance files, working project

#### Analysis

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

#### Result

**None of the CLI ideals trigger iteration.**

The ideals represent a _quality overlay_—they refine _how_ the CLI should behave without changing _what_ the template is trying to solve. The SOD's Problem Statement and Proposed Solution remain unchanged.

### When Would This Become Iteration?

If the 10-year maintenance posture required fundamental additions like:

- Built-in deprecation warning infrastructure
- Version migration tooling
- API stability contract enforcement
- Changelog automation as a core feature

...then collectively these would shift the Problem Statement from "starting point template" to "production longevity framework"—which _would_ warrant a new iteration.

## Reusable Artifacts

### Sustain vs. Iteration Decision Criteria

| Criterion | Sustain | Iteration |
|-----------|---------|-----------|
| Problem Statement | Unchanged | Changed |
| Proposed Solution | Same approach | Different approach |
| Scope | Refined within bounds | Expanded or shifted |
| Artifacts | Quality improvements | New artifact types |
| Success Criteria | Same metrics | New metrics |

### The Key Question

> "Does this change alter the contract I formalized, or extend/refine its implementation?"

- **Alter contract** → Iteration (regress to Formalize)
- **Extend/refine** → Sustain (continue in current stage)

## Related

- [lifecycle.md](../../core/spec/lifecycle.md) — Stage definitions including Sustain governance
- [sod.md](../../core/spec/sod.md) — Solution Overview Document specification

---

_Migrated from research/spec/sustain-worked-example.md_
_Approved: 2025-12-30_
