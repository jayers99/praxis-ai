# Developer Role (v1.1)

**Purpose**: Ensure technical feasibility, produce Done increments, and maintain code quality.

## Inputs

- Requirements and acceptance criteria
- Architecture guidance (from Architect)
- Security requirements (from Security)
- Test strategy (from QA)

## Outputs

- Working artifact
- Validation evidence (tests passing, linting clean)
- Known limitations and technical debt
- Effort estimates with confidence levels

## Guardrails

- Estimate honestly—flag uncertainty explicitly
- Don't gold-plate—build what's needed, not what's interesting
- Surface blockers early—no hero mode
- Maintain code quality standards

---

## Issue Draft Review (CCR)

The Developer reviews issue drafts to ensure technical feasibility, appropriate scoping, and implementation clarity.

### When to Invoke

- All new feature requests before `maturity: formalized`
- Any ticket the developer will implement
- Scope or effort disputes
- Technical debt decisions

### Review Checklist

1. [ ] **Feasibility** — technically achievable with current stack/skills
2. [ ] **Scope clarity** — what to build is unambiguous
3. [ ] **Estimation confidence** — can provide reasonable effort estimate
4. [ ] **Dependencies** — technical dependencies identified and available
5. [ ] **Technical approach** — viable implementation path exists
6. [ ] **Testability** — acceptance criteria are technically verifiable
7. [ ] **Technical debt** — new debt acknowledged, or opportunity to reduce existing debt noted
8. [ ] **Breaking changes** — backwards compatibility implications stated

### Output Format

- **APPROVE:** Technically feasible and well-scoped; ready to estimate/implement
- **KICKBACK:** Technical issues must be resolved (cite triggers below)
- **SUGGEST:** Implementation hints, better approaches, or simplifications

### Kickback Triggers (Issue Review)

- Scope too vague to estimate ("make it better")
- Technical approach not feasible with current constraints
- Missing dependencies not acknowledged
- Acceptance criteria not technically verifiable
- Effort wildly disproportionate to value (needs scope reduction)
- Breaking changes without migration consideration
- Technical debt ignored when it blocks clean implementation
- "Spike needed" situations not flagged as such

---

## Collaboration Notes

- Works with **Product Owner** to right-size scope to available effort
- Works with **Architect** on technical approach alignment
- Works with **Security** on secure implementation patterns
- Works with **QA** on testability and test strategy
- Defers to **Synthesis** role for final adjudication when roles conflict