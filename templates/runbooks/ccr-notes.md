# CCR Notes — Template (`30.10-ccr-notes.md`)

## Metadata

- Ticket: <slug>
- Ticket folder: <path>
- Draft under review: <path to current issue draft>
- CCR mode: Sequential
- Pass: 1 | 2
- Date: <YYYY-MM-DD>

## Source of Truth

- Current issue draft file: <path>
- CCR notes file: <this file>

## Global Directives (All Roles)

- Primary authority is your single role definition doc in `praxis-ai/core/roles/definitions/`.
  - The role definition doc should contain (in order of importance) the role’s principles and relevant opinions, with backing research references for each where applicable.
  - Start by reading this one role doc; only consult additional docs if the role doc points to them or if a gap is discovered.
- Use `praxis-ai/core/roles/kickback-rubrics.md` as the shared standard for structured kickbacks.
- Prefer citing _Praxis AI_ sources:
  - Roles: `praxis-ai/core/roles/definitions/`
  - Specs: `praxis-ai/core/spec/`
  - Opinions: `praxis-ai/opinions/`
  - Research Library (when needed): `praxis-ai/research-library/`
- If you consult a doc, list it under “Docs consulted” (explicit paths).
- Keep findings tied to the issue draft content; avoid inventing new scope.

## Reference Docs (shared)

- Authority & change control: `praxis-ai/core/authority-and-change-control.md`
- Kickback rubrics: `praxis-ai/core/roles/kickback-rubrics.md`
- Role lifecycle matrix: `praxis-ai/core/roles/lifecycle-matrix.md`

---

## Pass 1 — Role Reviews

### Research Librarian (Pass 1)

<a id="CCR.P1.RESEARCH_LIBRARIAN"></a>

**Role definition:** `praxis-ai/core/roles/definitions/00-research-librarian.md`

**Directives**

- Validate provenance: what claims need sources/citations.
- Flag missing context, missing definitions, or ambiguous terms.
- Separate consensus vs speculation vs open questions.

**Docs consulted**

- [ ] `praxis-ai/core/roles/definitions/00-research-librarian.md`
- [ ] `praxis-ai/research-library/README.md`
- [ ] Other: <paths>

**Verdict:** APPROVE | KICKBACK | SUGGEST

**Findings (high signal)**

-

**Required changes (if any)**

- [ ]

**Suggested citations to include in the draft (sparse)**

- <cite target + rationale>

**Open questions**

-

---

### Product Owner (Pass 1)

<a id="CCR.P1.PRODUCT_OWNER"></a>

**Role definition:** `praxis-ai/core/roles/definitions/01-product-owner.md`

**Directives**

- Ensure value + “why now” are explicit.
- Ensure scope is bounded (in-scope and out-of-scope).
- Ensure success criteria are measurable and verifiable.

**Docs consulted**

- [ ] `praxis-ai/core/roles/definitions/01-product-owner.md`
- [ ] `praxis-ai/core/roles/kickback-rubrics.md`
- [ ] Relevant opinions (browse as needed): `praxis-ai/opinions/`
- [ ] Other: <paths>

**Verdict:** APPROVE | KICKBACK | SUGGEST

**Value & scope assessment**

- Value proposition:
- Why now:
- In scope:
- Out of scope:

**Required changes (if any)**

- [ ]

**Suggestions (non-blocking)**

-

**Citations to include in the draft (sparse)**

- <cite target + rationale>

---

### Architect (Pass 1)

<a id="CCR.P1.ARCHITECT"></a>

**Role definition:** `praxis-ai/core/roles/definitions/07-architect.md`

**Directives**

- Validate boundary clarity and integration points.
- Ensure NFRs (performance/reliability/etc.) are called out where relevant.
- Flag breaking changes and migration expectations.

**Docs consulted**

- [ ] `praxis-ai/core/roles/definitions/07-architect.md`
- [ ] Specs (browse as needed): `praxis-ai/core/spec/`
- [ ] Relevant opinions (browse as needed): `praxis-ai/opinions/`
- [ ] Other: <paths>

**Verdict:** APPROVE | KICKBACK | SUGGEST

**System/boundary notes**

- Affected components:
- Interfaces/integration points:
- NFRs:
- Migration/breaking change notes:

**Required changes (if any)**

- [ ]

**Suggestions (non-blocking)**

-

**Citations to include in the draft (sparse)**

- <cite target + rationale>

---

### Lead Developer (Pass 1)

<a id="CCR.P1.DEVELOPER"></a>

**Role definition:** `praxis-ai/core/roles/definitions/05-developer.md`

**Directives**

- Validate feasibility and implementation clarity.
- Flag missing dependencies, unrealistic scope, or “spike needed” unknowns.
- Ensure acceptance criteria are technically verifiable.

**Docs consulted**

- [ ] `praxis-ai/core/roles/definitions/05-developer.md`
- [ ] Relevant opinions (browse as needed): `praxis-ai/opinions/code/` (if code ticket)
- [ ] Other: <paths>

**Verdict:** APPROVE | KICKBACK | SUGGEST

**Feasibility notes**

- Key unknowns/spikes:
- Dependencies:
- Suggested implementation approach:

**Required changes (if any)**

- [ ]

**Suggestions (non-blocking)**

-

**Citations to include in the draft (sparse)**

- <cite target + rationale>

---

### QA / Test Strategist (Pass 1)

<a id="CCR.P1.QA"></a>

**Role definition:** `praxis-ai/core/roles/definitions/09-qa.md`

**Directives**

- Ensure acceptance criteria are present and testable.
- Prefer Given/When/Then for behaviors when applicable.
- Identify high-risk scenarios and propose a risk-based test strategy.

**Docs consulted**

- [ ] `praxis-ai/core/roles/definitions/09-qa.md`
- [ ] `praxis-ai/research-library/patterns/tdd-bdd-ai-verification.md`
- [ ] `praxis-ai/research-library/patterns/ai-code-verification-workflow.md`
- [ ] `praxis-ai/opinions/code/testing.md`
- [ ] Other: <paths>

**Verdict:** APPROVE | KICKBACK | SUGGEST

**Test strategy notes**

- Risks:
- Coverage priorities:
- Proposed validation approach:

**Required changes (if any)**

- [ ]

**Suggestions (non-blocking)**

-

**Citations to include in the draft (sparse)**

- <cite target + rationale>

---

### Red Team (Pass 1)

<a id="CCR.P1.RED_TEAM"></a>

**Role definition:** `praxis-ai/core/roles/definitions/02-red-team.md`

**Directives**

- Stress-test assumptions; enumerate failure modes.
- Quantify risk (severity/likelihood) where possible.
- Always propose constructive mitigations.

**Docs consulted**

- [ ] `praxis-ai/core/roles/definitions/02-red-team.md`
- [ ] `praxis-ai/core/roles/kickback-rubrics.md`
- [ ] Specs/opinions as needed: `praxis-ai/core/spec/`, `praxis-ai/opinions/`
- [ ] Other: <paths>

**Verdict:** APPROVE | KICKBACK | SUGGEST

**Top risks**

- Risk 1 (severity/likelihood):
- Risk 2 (severity/likelihood):

**Assumptions challenged**

-

**Mitigations**

-

**Required changes (if any)**

- [ ]

**Citations to include in the draft (sparse)**

- <cite target + rationale>

---

## Pass 2 — Deltas Only

> Record only deltas relative to Pass 1.

### Product Owner (Pass 2)

<a id="CCR.P2.PRODUCT_OWNER"></a>

**Verdict:** APPROVE | KICKBACK | SUGGEST

**Deltas**

-

### Architect (Pass 2)

<a id="CCR.P2.ARCHITECT"></a>

**Verdict:** APPROVE | KICKBACK | SUGGEST

**Deltas**

-

### Lead Developer (Pass 2)

<a id="CCR.P2.DEVELOPER"></a>

**Verdict:** APPROVE | KICKBACK | SUGGEST

**Deltas**

-

### QA / Test Strategist (Pass 2)

<a id="CCR.P2.QA"></a>

**Verdict:** APPROVE | KICKBACK | SUGGEST

**Deltas**

-

### Red Team (Pass 2)

<a id="CCR.P2.RED_TEAM"></a>

**Verdict:** APPROVE | KICKBACK | SUGGEST

**Deltas**

-
