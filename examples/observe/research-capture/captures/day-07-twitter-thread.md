# Day 07 Capture — Twitter Thread

**Date:** 2025-10-07  
**Source:** @ai_governance_expert thread on governance frameworks  
**Type:** Saved thread (copy/paste)

---

## Thread (Reformatted)

**Tweet 1:**
Three principles for AI governance in production:

1️⃣ Transparency (log everything, make decisions auditable)  
2️⃣ Accountability (humans are responsible for outcomes, not algorithms)  
3️⃣ Reversibility (rapid rollback when things go wrong)

**Tweet 2:**
Transparency means:
- Log inputs, outputs, model versions, decisions
- Structured logging (not just text dumps)
- Queryable audit trails (when did we decide X? why?)
- Different views for different stakeholders

**Tweet 3:**
Accountability means:
- Humans own AI decisions (model is a tool, not an actor)
- Clear decision rights (who can override? who escalates?)
- Blameless postmortems (learn from failures, don't hide them)
- Defined roles (who monitors? who responds?)

**Tweet 4:**
Reversibility means:
- Fast rollback (< 5 min to previous state)
- Version control for models, data, configs
- Automated rollback triggers (SLO breaches, anomaly detection)
- Tested rollback procedures (don't discover they don't work during incident)

**Tweet 5:**
Governance isn't bureaucracy. It's the operating system for AI in production.

---

## Personal Reactions

- Three principles: Transparency, Accountability, Reversibility (TAR framework?)
- 5-minute rollback keeps appearing (HN, podcast, now here)
- "Model is a tool, not an actor" (important framing)
- Governance as OS (not red tape)

## Cross-References

- Transparency: aligns with podcast (role-based dashboards)
- Accountability: connects to HN thread (who has authority to override?)
- Reversibility: matches research paper (technical + organizational)

---

**Status:** Saved for reference, patterns emerging
