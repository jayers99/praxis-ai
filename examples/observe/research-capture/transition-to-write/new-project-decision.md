# Transition to Write Domain — New Project Created

**Date:** 2025-10-16  
**From:** Observe domain (AI Governance research-capture)  
**To:** Write domain (AI Governance synthesis article)

---

## Transition Decision

**Why transition:**
- Clear thesis emerged: "Organizations need layered AI governance"
- Intent shifted from "capture for later" to "synthesize and communicate"
- Structure forming (three-layer framework)
- Audience identified (engineering managers, technical leads)

**Transition rule:** When synthesis and external communication become intent, Observe must transition to appropriate domain.

**Appropriate domain:** **Write** (structured externalized thought)

---

## New Write Project Details

### Project Initialization

```bash
# In user's workspace (not in this example directory)
praxis new ai-governance-article --domain write --privacy public
cd ai-governance-article
praxis templates render --stage formalize  # Creates docs/brief.md
```

### Project Configuration (praxis.yaml)

```yaml
domain: write
stage: formalize
privacy_level: public
environment: Home
subtype: technical
```

---

## Writing Brief (Required Formalize Artifact)

**File:** `docs/brief.md`

### Thesis
Organizations need layered AI governance—technical controls, organizational processes, and policy frameworks—that compose into coherent architecture. No single layer is sufficient; effective governance emerges from their integration.

### Audience
- **Primary:** Engineering managers and technical leads responsible for AI deployment
- **Secondary:** Compliance officers, product managers, senior engineers

### Scope (In)
- Three-layer governance framework (technical, organizational, policy)
- How layers interact (examples: rollback, oversight, risk assessment)
- Measurable standards (< 5 min rollback, structured logging, decision rights)
- Risk-proportional approach (not one-size-fits-all)

### Scope (Out)
- Specific tool recommendations (keep tool-agnostic)
- Regulatory compliance deep-dive (focus on principles, not regulations)
- AI safety research (focus on governance, not alignment)

### Source Material
**All captures from Observe project:**
- HN thread (human-in-the-loop patterns)
- Research paper (Dafoe 2018, layered governance)
- Podcast (transparency dashboards, risk spectrum)
- Twitter thread (TAR framework: Transparency, Accountability, Reversibility)
- Book excerpt (O'Neil, higher standards for algorithms)
- Meeting notes (real-world constraints, risk-tiered approach)

---

## Lifecycle Progression (Write Project)

**Current stage:** Formalize (Writing Brief created)

**Next stages:**
1. **Commit:** Decide to proceed with article
2. **Execute:** Draft → Revise → Polish
3. **Sustain:** Publish, update based on feedback
4. **Close:** Archive or transition to new project

---

## Key Differences: Observe vs. Write

| Aspect | Observe Project | Write Project |
|--------|----------------|---------------|
| **Intent** | Capture without judgment | Synthesize and communicate |
| **Artifacts** | Raw captures, light themes | Writing Brief, drafts, final article |
| **Formalize** | NO formalize artifact | REQUIRED: docs/brief.md |
| **Execution** | No execution stage | Execute = drafting and revision |
| **Output** | Source material | Published article |

---

## How Source Material Transfers

### Observe Project Delivers:
- 6 raw captures (primary sources)
- Themes identified (3 layers: technical, org, policy)
- Connections mapped (5 key patterns)
- Framework roughed out (three-layer governance)

### Write Project Uses:
- Captures as evidence/examples in article
- Themes as article structure (3 main sections)
- Connections as supporting arguments
- Framework as core thesis

**Relationship:** Observe project = research phase, Write project = synthesis phase

---

## Governance Boundary

**Observe project governance:**
- No formalize artifact required
- No commit decision needed
- No execution governance
- Close when intent emerges or captures go stale

**Write project governance:**
- Writing Brief required (formalize artifact)
- Explicit commit decision (proceed or abandon)
- Governed execution (drafting, revision, publication)
- Sustain after publication (updates, corrections)

**Why separate projects?** Each domain has different governance requirements. Observe is pre-formalization; Write requires formalized intent.

---

## Success Criteria (Write Project)

From Writing Brief:

1. Article published on engineering blog or Medium
2. Clearly explains three-layer governance framework
3. Provides concrete examples (measurable standards, real scenarios)
4. Resonates with target audience (engineering managers)
5. No factual corrections needed post-publication

---

## Transition Complete

**Observe project:** Closed (Oct 16, 2025)  
**Write project:** Created (Oct 16, 2025), currently in Formalize stage

**Next action in Write project:** Commit decision (proceed with drafting or abandon)

---

**Key learning:** Observe domain is temporary. When intent crystallizes, transition to appropriate execution domain (Write, Learn, Code, Create).
