# Day 12 Capture — Internal Meeting Notes

**Date:** 2025-10-12  
**Source:** Work meeting on AI deployment policies  
**Type:** Meeting notes (unedited)

---

## Attendees
- Engineering lead (me)
- Product manager
- Legal counsel
- VP of Engineering

## Discussion Points (Rough Notes)

### Current State
- We have AI in prod (recommendation engine, anomaly detection)
- No formal governance beyond "code review + deploy"
- Legal concerned about liability (who's responsible when model makes bad rec?)
- Product wants to move faster (governance will slow us down?)

### Proposals Discussed

**Option 1: Lightweight governance (eng lead)**
- Model registry (what's deployed, version, owner)
- Monitoring dashboards (inputs, outputs, metrics)
- Rollback procedures (documented, tested)
- Minimal process overhead

**Option 2: Full governance framework (legal)**
- Pre-deployment review board
- Risk assessment for every model
- Audit trails for all decisions
- Quarterly governance audits
- Formal sign-offs

**Option 3: Hybrid (VP)**
- Risk-tiered approach (low-risk = lightweight, high-risk = formal)
- Start with monitoring + rollback (table stakes)
- Add review process for high-stakes models only
- Iterate based on what we learn

---

## Decision (Tentative)

VP wants Option 3 (hybrid, risk-tiered)

Action items:
- Define risk tiers (what makes a model "high-risk"?)
- Document rollback procedures (test them)
- Set up basic monitoring (dashboards, alerts)
- Revisit in 3 months (did this work?)

---

## Personal Reactions

- Option 3 feels right (proportional to risk)
- Need to define "high-risk" (vague right now)
- Monitoring + rollback = minimum viable governance (everyone agreed)
- Legal wants more than we'll give (but willing to start small)
- This aligns with research (layered governance, risk-based)

---

**Status:** Work context, real-world constraints, actionable next steps
