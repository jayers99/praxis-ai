# Architecture Decision Records

This section documents significant architectural decisions made in the Praxis project.

---

## What are ADRs?

Architecture Decision Records (ADRs) capture important architectural decisions along with their context and consequences. Each ADR describes a single decision and provides:

- **Context:** What is the issue we're facing?
- **Decision:** What decision did we make?
- **Consequences:** What are the trade-offs and implications?

---

## Active ADRs

### ADR-001: Policy Engine Implementation

**Status:** Accepted  
**Date:** 2025-12  
**Context:** Choose policy validation approach  
**Decision:** Use Pydantic v2 for validation (not CUE)  

[Read ADR-001 →](001-policy-engine.md)

---

### ADR-002: Validation Model

**Status:** Accepted  
**Date:** 2025-12  
**Context:** Define validation rules and severity levels  
**Decision:** Four-tier validation model (error/warning for unknown values, missing artifacts, regressions, privacy downgrades)  

[Read ADR-002 →](002-validation-model.md)

---

### ADR-003: Extension Manifest Format

**Status:** Accepted  
**Date:** 2025-12  
**Context:** Standardize extension metadata  
**Decision:** YAML-based manifest with semantic versioning  

[Read ADR-003 →](003-extension-manifest.md)

---

### ADR-004: Versioning and Naming Schemes

**Status:** Accepted  
**Date:** 2026-01-05  
**Context:** Establish versioning strategy across ecosystem  
**Decision:** SemVer for all components, git tags for templates, naming conventions for templates and extensions  

[Read ADR-004 →](004-versioning-and-naming-schemes.md)

---

## ADR Template

When creating a new ADR, use this template:

```markdown
# ADR-XXX: [Title]

**Status:** [Proposed | Accepted | Deprecated | Superseded]  
**Date:** YYYY-MM-DD  
**Authors:** [Names]

## Context

What is the issue that we're seeing that is motivating this decision or change?

## Decision

What is the change that we're proposing and/or doing?

## Consequences

What becomes easier or more difficult to do because of this change?

### Positive Consequences

- Benefit 1
- Benefit 2

### Negative Consequences

- Trade-off 1
- Trade-off 2

## Alternatives Considered

What other options did we consider?

### Alternative 1: [Name]

**Pros:**
- Pro 1

**Cons:**
- Con 1

**Why rejected:** Rationale

## References

- Link to related issue
- Link to related documentation
```

---

## See Also

- [Contributing Guide](../CONTRIBUTING.md) — How to contribute to Praxis
- [Specification](../core/spec/sod.md) — Core specification
