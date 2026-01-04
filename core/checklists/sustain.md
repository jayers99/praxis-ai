# Sustain Stage Checklist

## Entry Criteria

- [ ] Execute complete; artifact delivered
- [ ] Initial implementation meets success criteria
- [ ] Artifact is in production or published

## Exit Criteria

- [ ] Work retired or closed
- [ ] Decision made to end maintenance
- [ ] Replacement or successor identified (if applicable)

## Guidance

Sustain is **active governance of living work**. This is NOT a holding pattern—it's maintenance, monitoring, optimization, and policy enforcement over time.

**Key Responsibilities:**
- Maintain and update delivered work
- Monitor performance and quality
- Respond to issues and defects
- Optimize and improve within contract
- Enforce policy and governance

**Activities:**
- Bug fixes and patches
- Feature additions within scope
- Performance optimization
- Documentation updates
- User support and feedback incorporation
- Security updates

**Critical Question: Iteration vs. New Version?**

"Does this change alter the contract I formalized, or does it extend/refine the implementation of that contract?"

- **Contract change** → New iteration (regress to Formalize)
- **Implementation extension** → Stay in Sustain

### Iteration Triggers by SOD Section

| Section | Change Type | Rationale |
|---------|-------------|-----------|
| **Problem Statement** | Iteration | The problem you're solving has changed or expanded significantly |
| **Desired Outcomes** | Iteration | Fundamental goals have shifted (not just added goals, but changed direction) |
| **Canonical Dimensions** | Iteration | Adding/removing/redefining core concepts or constraints |
| Risks & Mitigations | Sustain | New risks discovered during execution |
| First Executable Increment | Sustain | New increments added |
| Policy Enforcement details | Sustain | Implementation refinements |

**Heuristic:** If you need to change Problem Statement, Desired Outcomes, or core constraints, you're starting a new iteration.

### What Sustain Absorbs

Sustain is more flexible than it might appear. Significant work can happen within Sustain:
- Feature additions that fit existing scope
- Quality bar improvements
- Convention/style overlays
- New implementation patterns
- Performance optimization
- Additional policy rules

**The iteration trigger is about contract changes, not scope size.** A massive feature set stays in Sustain if the formalization contract holds.

## Domain Variance

Sustain semantics vary by domain:
- **Code:** Maintenance, monitoring, operations, bug fixes
- **Write/Create:** Revisions, republication, audience engagement
- **Learn:** Practice, retention, skill maintenance
- **Observe:** Curation, archiving, retrieval optimization

## Progression

When work is retired, replaced, or no longer needed, advance to **Close** to capture learnings and end intentionally.

## References

- [Lifecycle Spec](../spec/lifecycle.md#8-sustain)
- [Lifecycle Spec: Iteration vs. Sustain](../spec/lifecycle.md#iteration-vs-sustain)
- [ITIL Service Operation](https://en.wikipedia.org/wiki/ITIL)
- [DevOps: Operate & Monitor](https://en.wikipedia.org/wiki/DevOps)
