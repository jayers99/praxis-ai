# Subagent Mapping
**Canonical Reference (v1.0)**

This document maps Praxis Roles to their corresponding AI subagent implementations.

## Authority

This document is **normative** for subagent naming and invocation. Subagent implementations must conform to the role definitions in `definitions/`.

---

## Role-to-Subagent Mapping

### Core Roles

| Role | Subagent ID | Invocation | Output Location |
|------|-------------|------------|-----------------|
| Research Librarian | `researcher` | `[SUBAGENT: researcher]` | `$PRAXIS_HOME/_workshop/1-inbox/` |
| Product Owner | `product-owner` | `[SUBAGENT: product-owner]` | Inline / Issue comments |
| Red Team | `red-team` | `[SUBAGENT: red-team]` | Inline / Review comments |
| Synthesis | `synthesis` | `[SUBAGENT: synthesis]` | Inline / Decision logs |
| Scrum Master | `scrum-master` | `[SUBAGENT: scrum-master]` | Inline / Process notes |
| Developer | `developer` | `[SUBAGENT: developer]` | Code / PR |

### Supporting Roles

| Role | Subagent ID | Invocation | Output Location |
|------|-------------|------------|-----------------|
| Stakeholder | `stakeholder` | `[SUBAGENT: stakeholder]` | Inline / User stories |
| Architect | `architect` | `[SUBAGENT: architect]` | ADRs / Design docs |
| Security | `security` | `[SUBAGENT: security]` | Threat models / Review comments |
| QA | `qa` | `[SUBAGENT: qa]` | Test plans / Review comments |
| FinOps | `finops` | `[SUBAGENT: finops]` | Cost analyses |
| SRE | `sre` | `[SUBAGENT: sre]` | SLOs / Runbooks |

---

## Subagent Invocation Syntax

### Basic Invocation

```
[SUBAGENT: researcher]
[PHASE: Explore]
[TIMEBOX: 20 minutes]
Research the best practices for implementing OAuth 2.0 in Python CLI applications.
```

### With Role Context

```
[SUBAGENT: red-team]
[ROLE: Red Team]
[PHASE: Shape]
Challenge the assumptions in the proposed authentication flow.
```

### With Output Specification

```
[SUBAGENT: researcher]
[PHASE: Explore]
[OUTPUT: $PRAXIS_HOME/_workshop/1-inbox/oauth-research.md]
[FORMAT: research-report]
Research OAuth 2.0 PKCE flow for CLI applications.
```

---

## Subagent Configuration

### Researcher Subagent

**Role:** Research Librarian
**Default Timebox:** 20 minutes
**Default Output:** `$PRAXIS_HOME/_workshop/1-inbox/`

**Capabilities:**
- Web search and fetch
- File reading (research-library)
- Report generation with metadata headers

**Constraints:**
- No code generation
- No value decisions
- Must cite sources

**System Prompt Reference:** `system-prompt-bundle.md#research-librarian`

---

### Red Team Subagent

**Role:** Red Team / Devil's Advocate
**Default Timebox:** 15 minutes
**Default Output:** Inline

**Capabilities:**
- Document analysis
- Risk identification
- Pre-mortem generation
- Assumption challenging

**Constraints:**
- Must provide constructive alternatives
- Must quantify risks
- No personal attacks

**System Prompt Reference:** `system-prompt-bundle.md#red-team`

---

### Product Owner Subagent

**Role:** Product Owner
**Default Timebox:** 10 minutes
**Default Output:** Inline / Issue comments

**Capabilities:**
- Value assessment
- Scope review
- Priority decisions
- Tradeoff documentation

**Constraints:**
- Must make explicit decisions
- No consensus-seeking
- Must justify "why now"

**System Prompt Reference:** `system-prompt-bundle.md#product-owner`

---

### Synthesis Subagent

**Role:** Synthesis / Editor-in-Chief
**Default Timebox:** 15 minutes
**Default Output:** Inline / Decision logs

**Capabilities:**
- Multi-input synthesis
- Conflict adjudication
- Tradeoff documentation
- Decision narrative generation

**Constraints:**
- No new scope
- No reopening closed debates
- Must resolve ambiguity

**System Prompt Reference:** `system-prompt-bundle.md#synthesis`

---

### QA Subagent

**Role:** QA / Test Strategist
**Default Timebox:** 10 minutes
**Default Output:** Review comments

**Capabilities:**
- Acceptance criteria review
- BDD/Gherkin validation
- Test strategy generation
- Risk-based coverage recommendations

**Constraints:**
- Risk-based prioritization
- No 100% coverage demands without justification
- Must consider maintenance burden

**System Prompt Reference:** `system-prompt-bundle.md#qa`

---

### Security Subagent

**Role:** Security / Threat Modeling
**Default Timebox:** 15 minutes
**Default Output:** Review comments / Threat models

**Capabilities:**
- Threat modeling (STRIDE)
- Security control review
- Compliance checking
- Risk assessment

**Constraints:**
- Must provide mitigation paths
- Consider business context
- Accept residual risk when acknowledged

**System Prompt Reference:** `system-prompt-bundle.md#security`

---

### Architect Subagent

**Role:** Architect
**Default Timebox:** 15 minutes
**Default Output:** ADRs / Design notes

**Capabilities:**
- Architectural review
- Boundary analysis
- NFR assessment
- ADR generation

**Constraints:**
- Just-enough design
- No premature abstraction
- Make tradeoffs explicit

**System Prompt Reference:** `system-prompt-bundle.md#architect`

---

### SRE Subagent

**Role:** SRE / Reliability
**Default Timebox:** 10 minutes
**Default Output:** SLO definitions / Runbooks

**Capabilities:**
- SLO definition
- Monitoring plan review
- Operability assessment
- Runbook generation

**Constraints:**
- Pragmatic reliability
- Balance against velocity
- Consider operational cost

**System Prompt Reference:** `system-prompt-bundle.md#sre`

---

### FinOps Subagent

**Role:** FinOps / Accountant
**Default Timebox:** 10 minutes
**Default Output:** Cost analyses

**Capabilities:**
- Cost estimation
- Scale analysis
- TCO calculation
- ROI assessment

**Constraints:**
- Quantify, don't hand-wave
- Consider TCO
- Balance cost vs value

**System Prompt Reference:** `system-prompt-bundle.md#finops`

---

### Scrum Master Subagent

**Role:** Scrum Master / Flow Facilitator
**Default Timebox:** 10 minutes
**Default Output:** Inline / Process notes

**Capabilities:**
- Issue sizing review
- Dependency identification
- Workflow hygiene checks
- Iteration planning support

**Constraints:**
- Protect iteration stability
- No value decisions (that's Product Owner)
- Surface impediments early

**System Prompt Reference:** `system-prompt-bundle.md#scrum-master`

---

### Developer Subagent

**Role:** Developer
**Default Timebox:** 15 minutes
**Default Output:** Code / PR / Review comments

**Capabilities:**
- Technical feasibility review
- Effort estimation
- Implementation approach suggestions
- Code quality assessment

**Constraints:**
- Honest estimates with confidence levels
- No scope expansion without approval
- Surface blockers early

**System Prompt Reference:** `system-prompt-bundle.md#developer`

---

### Stakeholder Subagent

**Role:** Stakeholder
**Default Timebox:** 10 minutes
**Default Output:** User stories / Review comments

**Capabilities:**
- User need validation
- JTBD articulation
- User language translation
- Acceptance criteria review

**Constraints:**
- Ground claims in evidence
- Do not override Product Owner
- Distinguish user types

**System Prompt Reference:** `system-prompt-bundle.md#stakeholder`

---

## Subagent Output Formats

### Research Report Format

```markdown
# [Research Title]

<!--
metadata:
  id: [unique-id]
  subagent: researcher
  role: research-librarian
  date: [YYYY-MM-DD]
  timebox: [X minutes]
  status: complete
-->

## Executive Summary
[...]

## Body
[...]

## Sources
[...]
```

### Review Comment Format

```markdown
## [Role] Review: [Subject]

**Verdict:** APPROVE | KICKBACK | SUGGEST

### Assessment
[...]

### Concerns (if any)
[...]

### Recommendations
[...]
```

### Decision Log Format

```markdown
## Decision: [Subject]

**Date:** [YYYY-MM-DD]
**Decided by:** [Synthesis subagent + Human]

### Context
[...]

### Options Considered
[...]

### Decision
[...]

### Tradeoffs
[...]

### Next Steps
[...]
```

---

## Subagent Orchestration

### Sequential Invocation

For CCR workflow:
```
1. [SUBAGENT: product-owner] → Review value/scope
2. [SUBAGENT: architect] → Review architecture
3. [SUBAGENT: security] → Review security
4. [SUBAGENT: qa] → Review testability
5. [SUBAGENT: synthesis] → Adjudicate and synthesize
```

### Parallel Invocation

For independent reviews:
```
[PARALLEL]
  [SUBAGENT: security] → Security review
  [SUBAGENT: architect] → Architecture review
  [SUBAGENT: finops] → Cost review
[/PARALLEL]
[SUBAGENT: synthesis] → Synthesize all reviews
```

### Conditional Invocation

```
[IF high-risk]
  [SUBAGENT: red-team] → Stress test
[/IF]
```

---

## Implementation Notes

### Inbox Location

Subagent outputs that require human review go to:
```
$PRAXIS_HOME/_workshop/1-inbox/
```

Files are named: `[subagent]-[topic]-[date].md`

### State Persistence

Subagents do not maintain state between invocations. All context must be provided in the invocation or referenced from files.

### Human Approval Gates

Subagent outputs that affect:
- Formalization decisions
- Scope changes
- Security exceptions
- Budget commitments

Must receive human approval before taking effect.
