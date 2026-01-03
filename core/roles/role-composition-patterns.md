# Role Composition Patterns
**Canonical Reference (v1.0)**

This document defines common patterns for combining roles in specific review or decision scenarios.

## Authority

This document is **normative**. Role compositions should follow these patterns unless explicitly overridden.

---

## Why Composition Patterns?

Individual roles have focused expertise. Complex decisions often require multiple perspectives working together. Composition patterns define:

1. **Which roles** participate together
2. **In what order** they review
3. **How conflicts** are resolved
4. **What outputs** each contributes

---

## Core Composition Patterns

### Pattern 1: Security Review Composition

**Roles:** Security + Architect + Red Team

**Use Case:** Changes affecting trust boundaries, authentication, or data handling.

**Workflow:**
1. **Architect** reviews boundary impact and data flow
2. **Security** performs threat modeling and control review
3. **Red Team** stress-tests for attack vectors
4. **Synthesis** adjudicates if conflicts arise

**Combined Output:**
```markdown
## Security Review: [Feature Name]

### Architect Assessment
- Boundary changes: [...]
- Data flow impact: [...]
- ADR needed: Yes/No

### Security Assessment
- Threat model: [...]
- Required controls: [...]
- Compliance implications: [...]

### Red Team Assessment
- Attack vectors identified: [...]
- Stress test results: [...]
- Residual risks: [...]

### Verdict: APPROVE / KICKBACK
```

---

### Pattern 2: Feasibility Assessment Composition

**Roles:** Developer + Architect + FinOps

**Use Case:** Evaluating whether a proposed feature is technically and economically viable.

**Workflow:**
1. **Architect** assesses architectural fit and complexity
2. **Developer** estimates effort and identifies technical risks
3. **FinOps** models cost implications
4. **Synthesis** produces unified feasibility verdict

**Combined Output:**
```markdown
## Feasibility Assessment: [Feature Name]

### Architectural Fit
- Alignment with existing architecture: [...]
- Required changes: [...]
- Complexity rating: Low/Medium/High

### Technical Feasibility
- Effort estimate: [X story points / Y days]
- Confidence: High/Medium/Low
- Technical risks: [...]
- Dependencies: [...]

### Cost Analysis
- Implementation cost: $X
- Ongoing cost: $Y/month
- ROI assessment: [...]

### Verdict: FEASIBLE / NEEDS REFINEMENT / NOT FEASIBLE
```

---

### Pattern 3: User Validation Composition

**Roles:** Stakeholder + QA + Product Owner

**Use Case:** Ensuring features serve real user needs with testable acceptance criteria.

**Workflow:**
1. **Stakeholder** validates user need is grounded
2. **QA** reviews acceptance criteria for testability
3. **Product Owner** confirms value alignment
4. **Synthesis** produces validation verdict

**Combined Output:**
```markdown
## User Validation: [Feature Name]

### User Need Assessment
- JTBD: [...]
- Evidence: [...]
- Persona: [...]

### Testability Assessment
- Acceptance criteria format: Given-When-Then / Other
- Edge cases covered: Yes/No
- Error paths covered: Yes/No

### Value Assessment
- Strategic alignment: [...]
- Priority justification: [...]

### Verdict: VALIDATED / NEEDS REFINEMENT
```

---

### Pattern 4: Production Readiness Composition

**Roles:** SRE + Security + QA + Developer

**Use Case:** Pre-deployment review ensuring operational readiness.

**Workflow:**
1. **Developer** confirms implementation complete and tested
2. **QA** validates test coverage and acceptance criteria met
3. **Security** confirms security controls in place
4. **SRE** reviews monitoring, alerting, and rollback readiness
5. **Synthesis** produces go/no-go verdict

**Combined Output:**
```markdown
## Production Readiness: [Feature Name]

### Implementation Status
- Code complete: Yes/No
- Tests passing: Yes/No
- Known limitations: [...]

### Quality Status
- Test coverage: X%
- All acceptance criteria met: Yes/No
- Regression risk: Low/Medium/High

### Security Status
- Security review: Passed/Failed
- Controls implemented: [...]
- Residual risks accepted: [...]

### Operability Status
- Monitoring in place: Yes/No
- Alerts configured: Yes/No
- Runbooks written: Yes/No
- Rollback tested: Yes/No

### Verdict: GO / NO-GO / CONDITIONAL GO
Conditions: [if conditional]
```

---

### Pattern 5: Cost-Value Analysis Composition

**Roles:** FinOps + Product Owner + Red Team

**Use Case:** High-investment decisions requiring cost-benefit analysis.

**Workflow:**
1. **FinOps** quantifies costs and models scale
2. **Product Owner** articulates value and priority
3. **Red Team** challenges assumptions and identifies risks
4. **Synthesis** produces investment recommendation

**Combined Output:**
```markdown
## Cost-Value Analysis: [Feature Name]

### Cost Assessment
- Total investment: $X
- Ongoing costs: $Y/month
- 3-year TCO: $Z

### Value Assessment
- Expected benefit: [...]
- Strategic importance: High/Medium/Low
- Urgency: [...]

### Risk Assessment
- Key assumptions: [...]
- Challenged assumptions: [...]
- Risk-adjusted value: [...]

### Recommendation: INVEST / DEFER / REJECT
Rationale: [...]
```

---

### Pattern 6: Scope Change Composition

**Roles:** Product Owner + Scrum Master + Developer + Architect

**Use Case:** Evaluating mid-sprint scope change requests.

**Workflow:**
1. **Product Owner** assesses value and urgency
2. **Developer** estimates disruption and effort
3. **Architect** evaluates technical implications
4. **Scrum Master** assesses process and capacity impact
5. **Synthesis** produces change decision

**Combined Output:**
```markdown
## Scope Change Request: [Change Description]

### Value Assessment
- Business justification: [...]
- Urgency: Critical/High/Medium/Low
- Cost of delay: [...]

### Impact Assessment
- Effort: [X story points / Y days]
- Disruption to current work: [...]
- Technical implications: [...]

### Process Assessment
- Capacity available: Yes/No
- Items displaced: [...]
- Definition of Done achievable: Yes/No

### Decision: ACCEPT / DEFER / REJECT
If accepted, displaced items: [...]
```

---

## Composition Rules

### Invocation

When invoking a composition pattern:

```
[COMPOSITION: Security Review]
[PHASE: Shape]
[ROLES: Security, Architect, Red Team]
Review the proposed authentication changes.
```

### Role Order

Unless otherwise specified, roles review in this order:
1. Information-gathering roles first (Research Librarian, Stakeholder)
2. Domain expert roles next (Architect, Security, Developer)
3. Challenge roles (Red Team, QA)
4. Decision roles last (Product Owner, Synthesis)

### Conflict Resolution

When roles within a composition disagree:
1. Identify the specific conflict
2. Each role states their concern with evidence
3. Synthesis adjudicates based on phase priorities
4. Document the tradeoff in the combined output

### Partial Participation

If a role in the pattern is unavailable or not applicable:
1. Document which role is skipped and why
2. Proceed with remaining roles
3. Flag the gap in the combined output
4. Consider whether the gap introduces unacceptable risk

---

## Creating New Patterns

When creating a new composition pattern:

1. **Identify the decision type** — What recurring scenario needs multiple perspectives?
2. **Select participating roles** — Which roles have relevant expertise?
3. **Define the workflow** — In what order should roles review?
4. **Design the combined output** — What does the unified result look like?
5. **Document conflict resolution** — How are disagreements handled?
6. **Add to this document** — Compositions must be documented to be normative
