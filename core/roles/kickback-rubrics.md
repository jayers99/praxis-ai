# Kickback Rubrics by Role
**Canonical Reference (v1.0)**

Kickbacks are structured rejection notices. They enable quality loops without ambiguity.

## Universal Kickback Template

All kickbacks must include:

- **What failed**: Specific output that did not meet standards
- **What is missing**: Required elements not present
- **Standard not met**: Reference to the violated requirement
- **Direction for revision**: Concrete next steps
- **Effort cap**: Maximum time/tokens to spend on revision

## Role-Specific Emphasis

### Research Librarian
- Missing sources or citations
- Unclear distinction between consensus and speculation
- Excess verbosity without signal
- No metadata header

### Product Owner
- No clear decision stated
- Tradeoffs unstated or hidden
- Scope creep (adding items without deprioritizing)
- Consensus-seeking instead of deciding

### Red Team
- Vague or unquantified risks
- No evidence for claims
- Blocking without constructive alternative
- Missing severity/likelihood assessment

### Synthesis
- Ambiguity remains after synthesis
- Execution path unclear
- Reopened debate that was closed
- Missing tradeoff table

### Developer
- Acceptance criteria unmet
- Validation evidence missing
- Known limitations undocumented
- Scope expanded without approval

### Scrum Master
- Flow blockers not identified
- Process change without rationale
- Missing iteration plan
- Impediments untracked

### Stakeholder Proxy
- User language not grounded in evidence
- Jobs-to-be-done vague or assumed
- Acceptance feedback missing

### Architect
- ADR missing for significant decision
- Boundaries unclear
- Over-design (premature abstraction)

### QA
- Test strategy missing risk prioritization
- High-risk scenarios not enumerated

### Security
- Threat model incomplete
- Mitigations not mapped to threats

### FinOps
- Cost drivers unquantified
- Optimization levers not identified

### SRE
- SLOs undefined
- Monitoring plan missing
