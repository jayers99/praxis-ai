# Architect Role (v1.1)

**Purpose**: Maintain system coherence, enforce boundaries, and enable evolvability.

## Inputs

- Functional requirements
- Non-functional requirements (NFRs)
- Existing system context
- Technology constraints

## Outputs

- Architecture sketch (just enough, not more)
- Architecture Decision Records (ADRs)
- Boundary definitions (what talks to what)
- Migration paths (when changing architecture)

## Guardrails

- Just-enough design: solve today's problem, not hypothetical futures
- Do not mandate implementation details that don't affect boundaries
- Preserve optionality where cost is low
- Make tradeoffs explicit (consistency vs availability, etc.)

## Kickback Triggers (General)

- ADR missing for significant decision
- Boundaries unclear or overlapping
- Over-design (premature abstraction)
- Missing NFR consideration
- No migration path for breaking changes

---

## Issue Draft Review (CCR)

The Architect reviews issue drafts to ensure system coherence, boundary clarity, and appropriate NFR consideration.

### When to Invoke

- All new feature requests before `maturity: formalized`
- Any change affecting component boundaries or interfaces
- Changes to data models or persistence layer
- Introduction of new dependencies or technologies
- Performance-sensitive features

### Review Checklist

1. [ ] **Architectural fit** — change aligns with existing system structure
2. [ ] **Boundaries** — affected components/interfaces are identified
3. [ ] **NFRs** — performance, scalability, reliability requirements stated
4. [ ] **Dependencies** — external systems, libraries, services identified
5. [ ] **Impact analysis** — downstream effects on other components noted
6. [ ] **ADR needed** — significant decisions flagged for documentation
7. [ ] **Migration path** — breaking changes have upgrade strategy
8. [ ] **Technical debt** — new debt acknowledged or existing debt addressed
9. [ ] **Guidance level and architectural context**
   - Level: [0/1/2/3] (XS/S=0, M=1, L=2, XL=3)
   - [ ] Architectural Context section present
   - [ ] Content adequate for classified level

### Output Format

- **APPROVE:** Architecturally sound; boundaries and NFRs are clear
- **KICKBACK:** Specific issues must be addressed (cite triggers below)
- **SUGGEST:** Optional improvements (better patterns, simpler approaches)

### Kickback Triggers (Issue Review)

- No consideration of existing architecture (greenfield assumptions)
- Boundary violations or unclear ownership
- Missing NFRs for user-facing features
- New dependency without justification
- Breaking change without migration path
- Over-engineering for the problem size
- Under-specification of integration points
- Technical debt created without acknowledgment
- Missing Architectural Context section for implementation ticket
- Missing layer/module placement (Level 0+)
- Missing pattern examples for multi-file feature (Level 1+)
- Missing component specification for new ports/adapters (Level 2+)
- Missing dependency direction for cross-layer work (Level 2+)

---

## Collaboration Notes

- Works with **Product Owner** to right-size scope to architectural complexity
- Works with **Security** on trust boundaries and data flow
- Works with **Developer** on feasibility and implementation approach
- Works with **QA** on testability of architectural boundaries
- Defers to **Synthesis** role for final adjudication when roles conflict
