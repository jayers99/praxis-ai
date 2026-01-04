# Explore — Connections Between Captures

**Stage:** Explore  
**Date:** 2025-10-14

---

## Connection 1: Human-in-the-Loop Pattern

**Appears in:**
- HN thread (aitech_lead): "Human approval for high-stakes decisions"
- Podcast: "AI suggests, human decides (preserves agency)"
- Twitter thread: "Humans own AI decisions (model is a tool)"

**Connection:**
All three sources describe human oversight, but with nuance:
- Not "human approves everything" (too slow)
- Not "AI decides everything" (too risky)
- Risk-tiered: High-risk → human decides, low-risk → AI acts with audit

---

## Connection 2: The 5-Minute Rollback Standard

**Appears in:**
- Podcast: "If you can't roll it back in under 5 minutes..."
- Twitter thread: "Fast rollback (< 5 min to previous state)"
- Meeting: "Document rollback procedures (test them)"

**Connection:**
Specific, measurable standard emerging across sources:
- Not just "we can rollback" but "< 5 minutes"
- Implies: Tested procedures, automated triggers, version control
- Why 5 minutes? Presumably based on incident response experience

---

## Connection 3: Layered Governance Architecture

**Appears in:**
- Research paper: "Technical standards + institutional structures + policy frameworks must compose"
- HN thread (policy_analyst): "Technical governance alone isn't enough. Need org structures"
- Meeting: Risk-tiered hybrid (lightweight for low-risk, formal for high-risk)

**Connection:**
All sources reject single-layer governance:
- Technical-only = no accountability when things go wrong
- Policy-only = unenforceable without technical controls
- Must integrate across layers (technical, org, policy)

---

## Connection 4: Transparency as Foundation

**Appears in:**
- HN thread: "Log all model inputs, outputs, and decisions"
- Podcast: "Transparency dashboard with role-based views"
- Twitter thread: "Structured logging, queryable audit trails"
- Research paper: "Reversibility requires... communication protocols"

**Connection:**
Transparency isn't an add-on, it's infrastructure:
- Enables accountability (who decided what, when, why?)
- Enables rollback (what state to return to?)
- Enables learning (postmortems, audits, improvement)

---

## Connection 5: Higher Standards for AI (Scale Effect)

**Appears in:**
- Book excerpt: "Algorithms need to be held to higher standards (because of scale)"
- Podcast: "Risk changes over time (continuous assessment)"
- Meeting: "Legal concerned about liability"

**Connection:**
AI's scale changes the ethics:
- One biased human decision = localized harm
- One biased algorithm (×1000/hour) = systemic harm
- Therefore: Higher bar for AI, not lower

---

## Patterns Across Connections

1. **Risk-proportional governance:** Not one-size-fits-all
2. **Multi-layer architecture:** Technical + Organizational + Policy
3. **Measurable standards:** < 5 min rollback, structured logging, defined decision rights
4. **Continuous, not static:** Risk assessment, monitoring, audits are ongoing
5. **Human agency preserved:** AI as tool, humans as decision-makers

---

## Observation (Still in Observe Domain)

Connections are clear, but no argument yet. Just noticing how sources reinforce each other.

---

**Next:** Shape clusters of related captures (Shape stage)
