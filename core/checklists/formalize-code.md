# Formalize Stage Checklist — Code Domain Addendum

This addendum provides Code-specific guidance for the Formalize stage.

## Code Domain: Additional Exit Criteria

- [ ] Solution Overview Document (SOD) created at `docs/sod.md`
- [ ] SOD includes technical architecture overview
- [ ] SOD identifies implementation technologies and constraints
- [ ] SOD defines success criteria with measurable outcomes
- [ ] SOD specifies testing strategy (unit, integration, acceptance)

## Code-Specific Guidance

For the Code domain, the Formalize stage produces a **Solution Overview Document (SOD)**. The SOD locks intent and boundaries while remaining implementation-light—it answers "what" and "why" without prescribing "how."

### What the SOD Must Include

1. **Problem Statement** — What specific problem are you solving? Who experiences it?
2. **Desired Outcomes** — What does success look like? How will you measure it?
3. **Scope & Non-Goals** — What's in scope? What's explicitly out of scope?
4. **Technical Constraints** — Languages, frameworks, platforms, performance requirements
5. **Dependencies & Integrations** — External services, APIs, data sources
6. **First Executable Increment** — What's the smallest buildable unit?
7. **Risks & Mitigations** — What could go wrong? How will you address it?

### What the SOD Should NOT Include

- Detailed class diagrams or implementation specifics
- Line-by-line code architecture
- UI mockups (unless they're part of the problem definition)
- Implementation timelines (scope yes, schedule no)

### Formalize → Commit Gate

Before advancing to Commit, verify:
- [ ] SOD is complete and internally consistent
- [ ] All stakeholders have reviewed and approved the SOD
- [ ] Technical feasibility is validated (spikes completed if needed)
- [ ] Scope fits available appetite (time/effort budget)

## References

- [SOD Specification](../spec/sod.md)
- [Lifecycle Spec: Formalize Stage](../spec/lifecycle.md#5-formalize-structural-hinge)
- [Lifecycle Spec: Commit Gate Criteria](../spec/lifecycle.md#6-commit)
