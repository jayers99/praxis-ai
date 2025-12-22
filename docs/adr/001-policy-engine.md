# ADR-001: Policy Engine Selection

**Status:** Exploratory
**Date:** 2025-12-21
**Deciders:** TBD

---

## Context

Praxis requires a policy engine to enforce governance rules across the lifecycle. The engine must:

1. Encode domain and lifecycle rules declaratively
2. Enforce privacy invariants at validation time
3. Validate stage transitions and reclassification
4. Guarantee deterministic, order-independent composition
5. Remain human-readable for solo-author workflows

This is a foundational choice that affects all downstream tooling.

---

## Decision Drivers

- **Composability** — Rules should combine without order dependency
- **Type safety** — Catch errors at validation time, not runtime
- **Readability** — Non-experts should understand policies
- **Ecosystem** — Tooling, docs, community support
- **Portability** — Not locked to a specific runtime or platform
- **Learning curve** — Acceptable for a solo author / small team

---

## Options Considered

### Option 1: CUE

**Description:** Configuration language with types, constraints, and unification.

| Pros | Cons |
|------|------|
| Strong composition via unification | Smaller ecosystem than alternatives |
| Types and constraints in one language | Learning curve for unification model |
| Can validate AND generate configs | Less tooling than JSON Schema |
| Good fit for "dimensions compose" model | |

**Fit for Praxis:** High — unification model maps well to "domain + stage + privacy = behavior"

### Option 2: JSON Schema + Custom Validator

**Description:** Standard schema language with hand-written validation logic.

| Pros | Cons |
|------|------|
| Widely understood | No native composition |
| Excellent tooling | Verbose for complex constraints |
| Language-agnostic | Validation-only (no generation) |
| | Custom code for cross-field rules |

**Fit for Praxis:** Medium — works but requires more custom code

### Option 3: OPA/Rego

**Description:** Policy-as-code engine from CNCF.

| Pros | Cons |
|------|------|
| Powerful policy language | Overkill for solo/small use |
| Strong in authorization domain | Steep learning curve |
| Good for multi-tenant scenarios | Heavier runtime |
| | Less natural for config generation |

**Fit for Praxis:** Low — designed for different scale and use case

### Option 4: Custom DSL

**Description:** Create a Praxis-specific policy language.

| Pros | Cons |
|------|------|
| Tailored exactly to needs | Maintenance burden |
| No external dependencies | Reinventing solved problems |
| | No ecosystem |
| | Documentation burden |

**Fit for Praxis:** Low — premature optimization

### Option 5: Python with Pydantic

**Description:** Use Python dataclasses/Pydantic for schema, custom validators for rules.

| Pros | Cons |
|------|------|
| Familiar to Python developers | Policy mixed with implementation |
| Strong typing with Pydantic | Less declarative |
| Easy to start | Harder to audit/review policies |
| Good test tooling | |

**Fit for Praxis:** Medium — pragmatic starting point, may outgrow

---

## Current Recommendation

**CUE** is the leading candidate due to:

1. Unification model matches Praxis's compositional dimensions
2. Single language for schema + validation + generation
3. Declarative and auditable
4. Reasonable learning investment for the value

However, this remains **exploratory** until validated by the first executable increment.

---

## Validation Plan

1. Implement minimal schema for Code domain in CUE
2. Write 3-5 test cases (valid configs, invalid transitions, privacy violations)
3. Evaluate friction: Is CUE helping or hindering?
4. If CUE proves wrong, fall back to Pydantic (Option 5) as pragmatic alternative

---

## Decision

**Deferred** — Will be finalized after first increment validation.

---

## Consequences

### If CUE is adopted:
- Must learn CUE syntax and unification model
- Policy files are `.cue`, versioned alongside code
- CLI tooling depends on CUE runtime

### If CUE is rejected:
- Fall back to Pydantic + custom validators
- Policy lives in Python code
- Less separation between policy and implementation

---

## Related

- SOD v0.3 Section 7 (Policy Enforcement)
- GitHub Issue: Policy engine exploration spike
