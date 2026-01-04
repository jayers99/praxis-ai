# Execute Stage Checklist

## Entry Criteria

- [ ] Commit complete; resources allocated
- [ ] Explicit decision to proceed made
- [ ] SOD (or equivalent artifact) exists and is validated

## Exit Criteria

- [ ] Artifact produced per SOD specifications
- [ ] Success criteria met (as defined in formalization artifact)
- [ ] Implementation complete and tested
- [ ] Ready for delivery or deployment

## Guidance

Execute is where you **produce the artifact**. This includes coding, writing, illustration, or other implementation activities. AI behavior is tightly governed and driven by formalized intent.

**Key Responsibilities:**
- Build the implementation per SOD specifications
- Follow the scope and constraints defined in Formalize
- Test and validate against success criteria
- Deliver working artifact

**Activities:**
- Implementation work (coding, writing, creating)
- Testing (unit, integration, acceptance)
- Iteration within scope (refinement, not discovery)
- Quality assurance

**Critical Guardrails:**
1. **Stay within scope:** If scope changes, regress to Formalize
2. **Follow constraints:** Respect the boundaries set in formalization
3. **Validate continuously:** Test against success criteria
4. **Detect drift:** Watch for scope creep or contract changes

**Iteration During Execute:**

Execute supports **refinement iteration** (making it better) but NOT **discovery iteration** (changing what it is).

**Refinement (OK in Execute):**
- Code quality improvements
- Performance optimization
- Bug fixes
- UI/UX polish within defined scope

**Discovery (Requires Formalize Regression):**
- Changing core problem statement
- Adding major features outside scope
- Redefining success criteria
- Changing fundamental direction

**The Test:** "Does this change alter the contract I formalized, or does it extend/refine the implementation of that contract?"
- **Contract change** → Regress to Formalize
- **Implementation extension** → Stay in Execute

## Scope Change Detection

Watch for these signals that indicate formalization contract change:
- "We should also solve [new problem]"
- "Actually, the audience is different than we thought"
- "We need to add [major capability] not in the SOD"
- "The success criteria don't make sense anymore"

If any of these arise, **pause Execute and regress to Formalize**.

## Progression

Once the artifact is produced and meets success criteria, advance to **Sustain** for ongoing governance and maintenance.

## References

- [Lifecycle Spec](../spec/lifecycle.md#7-execute)
- [Agile/Scrum Sprint](https://www.scrum.org/resources/what-is-a-sprint-in-scrum)
- [Shape Up: Build Cycle](https://basecamp.com/shapeup/3.1-chapter-09)
