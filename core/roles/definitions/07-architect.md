# Architect Role (v1.0)

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

## Kickback Triggers
- ADR missing for significant decision
- Boundaries unclear or overlapping
- Over-design (premature abstraction)
- Missing NFR consideration
- No migration path for breaking changes
