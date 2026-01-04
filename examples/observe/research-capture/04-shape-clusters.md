# Shape — Capture Clusters

**Stage:** Shape  
**Date:** 2025-10-15

---

## Cluster A: Monitoring & Observability Patterns

**Captures:**
1. HN thread — "Log all inputs, outputs, decisions"
2. Podcast — "Transparency dashboard, role-based views"
3. Twitter thread — "Structured logging, queryable audit trails"
4. Research paper — "Reversibility requires technical capability (version control)"
5. Meeting — "Set up basic monitoring (dashboards, alerts)"

**Cluster theme:** Technical infrastructure for visibility

**Key concepts:**
- Structured logging (not text dumps)
- Role-based dashboards (different views for stakeholders)
- Queryable audit trails (when/why decisions made)
- Version control (models, data, configs)

---

## Cluster B: Decision Rights & Approval Workflows

**Captures:**
1. HN thread — "Who has authority to override the model?"
2. Podcast — "AI suggests, human decides (risk-tiered)"
3. Twitter thread — "Clear decision rights (who can override? who escalates?)"
4. Meeting — "Legal concerned about liability (who's responsible?)"

**Cluster theme:** Organizational structures and accountability

**Key concepts:**
- Decision authority (who can override AI?)
- Risk-tiered oversight (high-risk → human approval)
- Escalation paths (when to involve whom)
- Blameless postmortems (learn, don't hide failures)

---

## Cluster C: Risk Assessment & Rollback

**Captures:**
1. Podcast — "Risk is a spectrum, changes over time"
2. Podcast — "5-minute rollback rule"
3. Twitter thread — "Fast rollback (< 5 min), automated triggers"
4. Research paper — "Reversibility = technical + organizational"
5. Book excerpt — "Scale amplifies harm (biased decisions × 1000/hour)"
6. Meeting — "Risk-tiered approach (low-risk = lightweight, high-risk = formal)"

**Cluster theme:** Continuous risk management and rapid reversion

**Key concepts:**
- Risk as continuous (not one-time assessment)
- < 5 min rollback standard (tested procedures)
- Automated rollback triggers (SLO breaches, anomalies)
- Scale effect (AI errors compound faster than human errors)

---

## Structure Forming (But Still Raw)

### Potential Framework: Three-Layer Governance

**Layer 1: Technical Controls** (Cluster A)
- Monitoring, logging, dashboards
- Version control, rollback mechanisms
- Automated triggers and alerts

**Layer 2: Organizational Processes** (Cluster B)
- Decision rights and approval workflows
- Escalation paths and accountability
- Blameless postmortems and learning loops

**Layer 3: Policy & Standards** (Cluster C)
- Risk assessment frameworks
- Compliance requirements
- Ethical standards (higher bar for AI)

### How Layers Interact

**Example: Automated Rollback**
- **Technical:** Automated trigger (latency spike, error rate)
- **Organizational:** Who gets alerted? Who confirms rollback?
- **Policy:** Under what conditions is automated rollback permitted?

---

## Tension Point (Observe → ?)

A clear argument is forming:

**"Organizations need layered AI governance: technical controls, organizational processes, and policy frameworks that compose into coherent architecture."**

This is no longer raw capture. There's a thesis here.

---

## Decision Point

**Question:** Is this still Observe domain?

**Assessment:**
- ✗ Raw capture: No (structure and argument emerging)
- ✗ Pre-intent: No (intent is clear: synthesize and communicate)
- ✓ Synthesis forming: Yes (moving toward Write domain)

**Action:** Close Observe project, transition to Write domain

---

**Next:** Close this project and create new Write project (Close stage + Transition)
