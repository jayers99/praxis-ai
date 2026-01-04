# Commit Stage Checklist

## Entry Criteria

- [ ] SOD (or equivalent artifact) complete and validated
- [ ] Formalization artifact exists and is internally consistent
- [ ] Intent and scope are clear

## Exit Criteria

- [ ] Explicit commitment to proceed
- [ ] Resources allocated (time, effort, budget)
- [ ] Go/No-Go decision made
- [ ] Dependencies identified and unblocked

## Guidance

Commit is the **explicit decision to proceed**. This is where you lock scope and intent, allocate effort, and enforce policy invariants. Only a small subset of formalized work should reach this stage.

**Key Responsibilities:**
- Review formalization artifact for completeness
- Make explicit Go/No-Go decision
- Allocate resources and effort
- Verify dependencies are unblocked

**Go/No-Go Criteria:**

| Decision | Condition |
|----------|-----------|
| **Go** | SOD is complete and internally consistent |
| **Go** | Scope fits available appetite (time/effort budget) |
| **Go** | Dependencies are identified and unblocked |
| **Go** | Success criteria are measurable |
| **No-Go** | Uncertainty about scope or direction remains → regress to Formalize |
| **No-Go** | Dependencies are blocked with no clear resolution |
| **No-Go** | Appetite insufficient for defined scope → reduce scope or wait |

**Critical Questions:**
1. Is the formalization artifact complete?
2. Does the scope fit the available effort budget?
3. Are all dependencies identified and unblocked?
4. Are success criteria measurable and unambiguous?
5. Are we confident we know what we're building?

**What Commit Is Not:**
- Implementation work (that's Execute)
- Scope expansion (scope is locked)
- Re-exploration (that's regressing to Explore/Shape)

## Commit as a Gate

Commit is a **quality gate**. If there's uncertainty about scope, direction, or feasibility, regress to Formalize. Better to fix the foundation than build on shaky ground.

## Progression

Once you've made an explicit commitment and allocated resources, advance to **Execute** to produce the artifact.

## References

- [Lifecycle Spec](../spec/lifecycle.md#6-commit)
- [Stage-Gate Process](https://en.wikipedia.org/wiki/Phase%E2%80%93gate_model) (Robert G. Cooper)
- [Shape Up: Betting Table](https://basecamp.com/shapeup/2.2-chapter-08#the-betting-table)
