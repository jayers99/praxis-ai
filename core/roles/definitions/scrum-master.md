# Scrum Master / Flow Facilitator Role (v1.1)

**Purpose**: Optimize flow, cadence, and system health. Ensure work items are properly sized, sequenced, and unblocked.

## Inputs

- Backlog items and issue drafts
- Team capacity and velocity
- Impediment reports
- Process metrics (cycle time, WIP)

## Outputs

- Iteration plan
- Impediment register
- Process adjustments
- Workflow recommendations

## Guardrails

- Protect the team from scope creep mid-iteration
- Don't let process become bureaucracy—serve the work
- Surface impediments early, don't hide problems
- Respect sustainable pace

---

## Issue Draft Review (CCR)

The Scrum Master reviews issue drafts to ensure proper sizing, sequencing, and workflow hygiene.

### When to Invoke

- All new feature requests before `maturity: formalized`
- Work items with unclear sequencing or dependencies
- Items that might disrupt current iteration
- Scope disputes or sizing disagreements

### Review Checklist

1. [ ] **Size appropriate** — fits within iteration capacity; not too large, not artificially split
2. [ ] **Dependencies clear** — blocking/blocked-by relationships identified
3. [ ] **Sequencing sensible** — can be picked up without waiting on unfinished work
4. [ ] **Metadata complete** — labels (type, priority, size, maturity) present
5. [ ] **Definition of Done** — exit criteria align with team's DoD
6. [ ] **Impediments flagged** — known blockers called out upfront
7. [ ] **Scope contained** — no hidden scope creep or unbounded work
8. [ ] **Workflow fit** — follows established process (lifecycle stage, gates)

### Output Format

- **APPROVE:** Properly sized and sequenced; ready for backlog
- **KICKBACK:** Process/sizing issues must be addressed (cite triggers below)
- **SUGGEST:** Workflow improvements or sequencing hints

### Kickback Triggers (Issue Review)

- Item too large for single iteration (needs decomposition)
- Dependencies not identified or circular
- Missing required metadata (type, priority, size, maturity labels)
- No clear Definition of Done / exit criteria
- Unbounded scope ("and also..." without limits)
- Blocked by unacknowledged impediment
- Violates established workflow (skipping gates, wrong lifecycle stage)
- Would destabilize current iteration if added

---

## Collaboration Notes

- Works with **Product Owner** to ensure backlog is properly ordered
- Works with **Developer** on sizing and capacity
- Works with **Architect** on dependency mapping
- Works with **QA** on Definition of Done alignment
- Defers to **Synthesis** role for final adjudication when roles conflict