# Formalize Stage Checklist

## Entry Criteria

- [ ] Shape complete; direction chosen
- [ ] Single direction chosen from multiple options
- [ ] Scope roughed out
- [ ] Major tradeoffs resolved

## Exit Criteria

- [ ] Formalization artifact exists (SOD, Brief, or Plan)
- [ ] Artifact includes scope and constraints
- [ ] Artifact includes success criteria
- [ ] Intent is explicit and documented
- [ ] Boundaries are clearly defined

## Guidance

Formalize is the **structural hinge** in the Praxis lifecycle—the explicit boundary between exploration and execution. This stage converts shaped thinking into durable, policy-bearing artifacts.

**Key Responsibilities:**
- Establish explicit intent, scope, constraints, and success criteria
- Create domain-specific artifact (SOD for Code, Brief for Create/Write, Plan for Learn)
- Lock the "what" before moving to "how"

**Why This Matters:**
Before Formalize, iteration means discovery ("What is this?"). After Formalize, iteration means refinement ("How good can this be?"). Recognizing scope changes during Execute means regression to Formalize.

### Formalize Spine (All Domains)

Every Formalize artifact MUST explicitly define:

1. **Intent & Outcome** — Problem/thesis/creative intent, audience, success criteria, why now
2. **Scope & Boundaries** — In scope, out of scope (non-goals), assumptions, dependencies
3. **Constraints** — Domain constraints, environment overlay, privacy classification, tooling limits, time/effort caps
4. **Execution Framing** — First executable increment, risks & mitigations, open questions as explicit spikes
5. **Commit Criteria** — Success is unambiguous, scope is bounded, constraints are complete, unknowns are resolved or spiked

## Domain-Specific Artifacts

| Domain | Artifact | Location |
|--------|----------|----------|
| Code | Solution Overview Document (SOD) | `docs/sod.md` |
| Create | Creative Brief | `docs/brief.md` |
| Write | Writing Brief | `docs/brief.md` |
| Learn | Learning Plan | `docs/plan.md` |
| Observe | (none required) | — |

## References

- [Lifecycle Spec](../spec/lifecycle.md#5-formalize-structural-hinge)
- [SOD Specification](../spec/sod.md)
