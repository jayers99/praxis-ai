# Praxis Guardrails

Version: 0.2.0  
Status: Active (Consistency Guardrail Added)  
Last Updated: 2026-01-05

---

## Purpose

This document defines **execution-level guardrails** for Praxis.

Guardrails are:

- Context-specific
- Explicitly binding during execution
- Designed to reduce ambiguity and risk
- Expected to evolve over time

This file intentionally starts **empty**.

No guardrail should exist without:

- A clear link to principles
- Alignment with governance decisions
- Evidence from execution or learning

---

## Layer Declaration

**Layer:** Execution

This document is constrained by:

- [`decision-arbitration.md`](decision-arbitration.md) (governance)
- Informed by [`opinions/code/principles.md`](opinions/code/principles.md) (opinions)

If a conflict arises:

- Governance arbitrates
- Principles inform
- Execution complies

---

## Scope

This file includes guardrails for:

- **AI / Claude behavior during execution** (Bidirectional Consistency Propagation)
- Coding practices (to be defined)
- Testing expectations (to be defined)
- Issue discipline (to be defined)
- Source control usage (to be defined)
- Security and safety constraints (to be defined)

---

## Activation Criteria

This document becomes **active** only when:

- Specific guardrails are added
- Each guardrail includes rationale and scope
- Guardrails are reviewed against principles
- Conflicts are resolvable via governance

---

## Change Policy

Guardrails may change frequently.

All changes should be:

- Intentional
- Documented
- Reversible where possible

---

## Guardrails

### G1: Bidirectional Consistency Propagation

**Version:** 1.0  
**Status:** Active  
**Added:** 2026-01-05  
**Rationale:** AI assistants lack persistent memory of prior decisions. This causes design regressions where removed concepts reappear in child documents, parent document changes don't propagate downward, and child document assumptions contradict updated parents.

#### Trigger

This guardrail is triggered when AI modifies a file containing **canonical definitions** or when making changes that constitute a **critical decision**.

#### Critical Decision Definition

A "critical decision" is any change that:

1. **Adds, removes, or renames a canonical concept** — domains, layers, stages, privacy levels, environments, subtypes
2. **Changes a constraint** — modifies what is allowed, forbidden, or required
3. **Modifies relationships** between documents or concepts
4. **Changes entry/exit criteria** for lifecycle stages
5. **Alters validation rules** or policy enforcement

**NOT critical decisions:**
- Typo fixes
- Clarifications that don't change meaning
- Adding examples without changing definitions
- Formatting or style improvements

#### Document Dependency Graph

**Canonical Documents** (define concepts that other documents depend on):

```
core/spec/
  ├── domains.md         [CANONICAL: domain definitions]
  ├── lifecycle.md       [CANONICAL: stage definitions]  
  ├── privacy.md         [CANONICAL: privacy level definitions]
  └── sod.md            [CANONICAL: SOD structure]

core/governance/
  ├── layer-model.md     [CANONICAL: layer definitions]
  └── decision-arbitration.md [CANONICAL: governance rules]

CLAUDE.md               [CANONICAL: AI behavior]
```

**Dependent Documents** (must align with canonical sources):

```
Child of domains.md:
  - opinions/{domain}/*.md
  - opinions/{domain}/subtypes/**/*.md
  - CLAUDE.md (Domains section)
  - praxis.yaml (domain field in all projects)

Child of lifecycle.md:
  - core/checklists/{stage}.md
  - examples/*/praxis.yaml
  - CLAUDE.md (Lifecycle Stages section)
  - praxis.yaml (stage field in all projects)

Child of layer-model.md:
  - core/governance/guardrails.md (Layer Declaration)
  - opinions/ (all opinion files reference layers)

Child of privacy.md:
  - CLAUDE.md (Privacy Levels section)
  - praxis.yaml (privacy_level field in all projects)

Child of CLAUDE.md:
  - .github/copilot-instructions.md (if exists)
  - Project-level AI guard files (if exists)
```

#### Consistency Check Ritual

**Before completing a critical decision, AI MUST:**

1. **Identify the scope**
   - Is this a canonical definition change?
   - Which canonical document(s) are affected?

2. **List parent documents**
   - Which documents constrain this file?
   - Are there governance or layer model constraints?

3. **List child documents**
   - Which documents reference concepts defined here?
   - Use the dependency graph above as reference

4. **Verify upward consistency**
   - Does this change conflict with any parent document's constraints?
   - If parent defines allowed values, does this stay within bounds?
   - Are layer boundaries respected?

5. **Verify downward consistency**
   - Do any child documents now contain stale references?
   - Do any child documents reference removed concepts?
   - Are there contradictions between this change and child assumptions?

6. **Resolution**
   - If conflicts found: Resolve ALL conflicts before commit OR flag explicitly for user review
   - If no conflicts: Document the consistency check was performed
   - Update all affected child documents to maintain consistency

#### Examples

**Example 1: Removing a domain**

If AI removes "Planning" domain from `core/spec/domains.md`:
1. Check: Is "Planning" referenced in `CLAUDE.md`? → Update
2. Check: Are there opinion files in `opinions/planning/`? → Remove or flag
3. Check: Do examples use `domain: planning`? → Update or flag
4. Check: Does documentation reference Planning domain? → Update

**Example 2: Adding a new lifecycle stage**

If AI adds "Review" stage to `core/spec/lifecycle.md`:
1. Check: Does this conflict with allowed regressions table? → Verify
2. Update: Add `core/checklists/review.md`
3. Update: Add Review to allowed values in `CLAUDE.md`
4. Check: Do stage transition validations need updates? → Verify

**Example 3: Changing privacy level constraints**

If AI modifies privacy levels in `core/spec/privacy.md`:
1. Check: Does `CLAUDE.md` list match? → Update
2. Check: Are there AI permission modifiers affected? → Update
3. Check: Do validation rules need changes? → Verify

#### Enforcement

- This guardrail is **advisory** for human editors
- This guardrail is **mandatory** for AI assistants (Claude, Copilot, etc.)
- Violations should be caught during code review
- Consistency checks should be documented in commit messages

#### Related Documents

- `core/governance/layer-model.md` — defines the three-layer model
- `core/governance/decision-arbitration.md` — arbitration when conflicts arise
- `core/ai/ai-guards.md` — AI guard design principles

---

## Status

This document is now **active** with the Bidirectional Consistency Propagation guardrail.
