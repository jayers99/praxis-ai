---
name: "Feature Request"
about: "Request a new feature or enhancement for Praxis"
title: "Feature: "
labels: ["type:feature"]
---

## Issue metadata (required)

- **Type:** feature
- **Priority:** [P0/P1/P2/P3]
- **Size:** [XS/S/M/L/XL]
- **Maturity:** [raw/shaped/formalized/ready]

## Labels to apply (required)

- `type:feature`
- `priority:P[0-3]`
- `size:[XS/S/M/L/XL]`
- `maturity:[raw/shaped/formalized/ready]`

## Problem

<!-- Describe the problem this feature solves. Why is this needed? -->

## Outcome

<!-- What does success look like? What will users be able to do? -->

## MVP scope

<!-- What is the minimum viable implementation? List numbered items. -->

## Non-goals

<!-- What is explicitly out of scope? -->

## Acceptance criteria

<!-- Checkboxes for verifiable outcomes -->

- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Tests pass (no regressions)
- [ ] PR includes clear UAT instructions for reviewers

## Proposed approach

<!-- High-level implementation strategy. How will this be built? -->

## Architectural Context

<!--
Level Selection Quick Reference (for initial estimation; Architect has final authority):
| Size | Files | New Components | Layers | Level |
|------|-------|----------------|--------|-------|
| XS/S | 1-2   | 0              | 1      | 0     |
| M    | 2-5   | 0-1            | 1-2    | 1     |
| L    | 5+    | 2+             | 2-3    | 2     |
| XL   | 10+   | Novel          | All    | 3     |

Rule: When in doubt, go one level higher.
Default: Level 1 for all non-trivial work.
-->

**Level:** [0/1/2/3] (use table above for initial estimate; Architect confirms during CCR)

### Placement
- **Layer:** [domain | application | infrastructure]
- **Module:** [path/to/module/]

### Patterns to Follow
| Pattern | Example File | Notes |
|---------|--------------|-------|
| [Pattern name] | [path/to/example.py] | [optional guidance] |

### Constraints
- Must NOT import from: [forbidden modules]
- New dependencies require: [adapter creation | human approval]
- If architectural placement unclear: **Ask before implementing**

<!-- For Level 2+ only: -->
### New Components (Level 2+)
<!-- Remove this section if Level 0 or 1 -->
- New port: [domain/ports/X.py]
- New adapter: [infrastructure/adapters/X.py]
- New service: [application/services/X.py]

### Dependency Direction (Level 2+)
<!-- Remove this section if Level 0 or 1 -->
<!-- ← = "depends on", ↑ = "implements" -->
```
Domain ← Application ← Infrastructure
        ↑               ↑
        └── Ports ──────┘ (Adapters implement ports)
```

<!-- For Level 3 only: -->
### Human Review Checkpoints (Level 3)
<!-- Remove this section if Level 0, 1, or 2 -->
- [ ] Pre-implementation: Architect approves design sketch
- [ ] Mid-implementation: Review after core logic complete
- [ ] Post-implementation: Verify dependency rules followed

## Risks / open questions

<!-- What could go wrong? What uncertainties remain? -->

## Links

<!-- Related issues, docs, prior art, research -->

---

<!-- 
EXAMPLE: Before/After Architectural Context

BEFORE (Inadequate):
## Proposed approach
Add a new endpoint for user preferences.

AFTER (Level 1 — Adequate):
## Architectural Context

**Level:** 1

### Placement
- **Layer:** application
- **Module:** application/services/

### Patterns to Follow
| Pattern | Example File | Notes |
|---------|--------------|-------|
| Service pattern | application/services/user_service.py | Follow validation approach |
| API endpoint | infrastructure/api/users.py | Follow response format |

### Constraints
- Must NOT import from infrastructure/ in service layer
- New validation rules go in domain/validators/
- If unclear, ask before implementing
-->
