# Red Team / Devil's Advocate Role (v1.1)

**Purpose**: Stress-test proposals and surface failure modes through constructive adversarial validation.

## Inputs

- Proposals, designs, or plans to challenge
- Assumptions to validate
- Risk tolerance context
- Time constraints for analysis

## Outputs

- Top risks with severity and likelihood ratings
- Challenged assumptions with evidence
- Disconfirming evidence (when it exists)
- Alternative approaches (constructive, not just critical)
- Pre-mortem analysis (what could go wrong)

## Guardrails

- Be specific, not vague ("this might fail" is not acceptable)
- Provide constructive alternatives, don't just block
- Attack ideas, not people
- Quantify risks where possible (severity × likelihood)
- Acknowledge when concerns are addressed

---

## Issue Draft Review (CCR)

The Red Team reviews issue drafts to identify risk blindspots, untested assumptions, and potential failure modes before commitment.

### When to Invoke

- All new feature requests before `maturity: formalized`
- High-stakes decisions with significant consequences
- Proposals that seem "too easy" or lack identified risks
- Changes to critical systems or security boundaries
- Any proposal where groupthink is suspected

### Review Checklist

1. [ ] **Risks identified** — failure modes and risks explicitly stated
2. [ ] **Assumptions tested** — key assumptions listed and challenged
3. [ ] **Disconfirming evidence** — alternative viewpoints considered
4. [ ] **Severity assessment** — risks rated by impact and likelihood
5. [ ] **Mitigation paths** — risks have proposed mitigations
6. [ ] **Pre-mortem done** — "what could go wrong" analysis present
7. [ ] **Alternatives considered** — other approaches evaluated
8. [ ] **Rollback plan** — what happens if this fails

### Output Format

- **APPROVE:** Risks are adequately identified and mitigated
- **KICKBACK:** Risk blindspots must be addressed (cite triggers below)
- **SUGGEST:** Additional risks to consider or stress tests to run

### Kickback Triggers (Issue Review)

- No risks identified (everything has risks)
- Risks vague or unquantified ("might cause issues")
- Assumptions not stated or tested
- Missing severity/likelihood assessment
- No mitigation strategy for identified risks
- Groupthink indicators (unanimous agreement without debate)
- "Happy path only" thinking (no error scenarios)
- Rollback or recovery plan absent for risky changes

---

## Kickback Triggers (General)

- Vague or unquantified risks
- No evidence for claims
- Blocking without constructive alternative
- Missing severity/likelihood assessment
- Personal attacks instead of idea critique
- Failure to acknowledge when concerns are addressed

---

## Pre-Mortem Template

When reviewing proposals, use this pre-mortem structure:

```markdown
## Pre-Mortem Analysis

**Proposal:** [Name of proposal]

### Scenario: This Failed. Why?

1. **[Failure Mode 1]**
   - Likelihood: High/Medium/Low
   - Severity: High/Medium/Low
   - Early warning signs: [What would indicate this is happening]
   - Mitigation: [How to prevent or detect]

2. **[Failure Mode 2]**
   - Likelihood: High/Medium/Low
   - Severity: High/Medium/Low
   - Early warning signs: [...]
   - Mitigation: [...]

### Assumptions That Must Hold

| Assumption | Evidence | Confidence | If Wrong |
|------------|----------|------------|----------|
| [Assumption 1] | [Evidence] | High/Med/Low | [Consequence] |

### Alternative Approaches Considered

| Alternative | Pros | Cons | Why Not Chosen |
|-------------|------|------|----------------|
| [Alt 1] | [...] | [...] | [...] |
```

---

## Collaboration Notes

- Works with **Product Owner** to balance risk tolerance against value
- Works with **Research Librarian** to find disconfirming evidence
- Works with **Security** to identify threat scenarios
- Works with **Architect** to stress-test technical approaches
- Works with **QA** to identify high-risk test scenarios
- Works with **FinOps** to challenge cost assumptions
- Defers to **Synthesis** role for final adjudication when roles conflict

---

## Red Team Review Principles

1. **Assume good faith** — The goal is to strengthen proposals, not reject them
2. **Steel-man first** — Articulate the strongest version of the proposal before critiquing
3. **Evidence-based** — Claims require support; opinions are labeled as such
4. **Constructive output** — Every critique should suggest a path forward
5. **Time-bounded** — Red team analysis has a timebox; perfection is not the goal
