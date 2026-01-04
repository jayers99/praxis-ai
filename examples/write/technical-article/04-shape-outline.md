# Shape — Article Outline

**Stage:** Shape  
**Date:** 2025-01-18

---

## Working title

**"Testing in Production: A Pragmatic Approach for Modern Systems"**

Alternative: "Why You're Already Testing in Production (And How to Do It Right)"

---

## Structure

### Hook / Intro (150 words)

**Opening statement:** "If you're not testing in production, you're not testing what your users actually experience."

**Problem setup:**
- Staging never matches prod (data, scale, user behavior)
- "TiP" stigmatized as reckless
- But absence of TiP means critical issues surface unexpectedly

**Thesis:** TiP is pragmatic when done with proper guardrails

---

### Section 1: Why Testing in Production is Necessary (400 words)

**Key points:**
- Production has emergent properties staging can't replicate
- Real user behavior differs from test scenarios
- Scale issues only appear at production load
- Third-party integrations behave differently

**Examples:**
- Caching behavior changes with real traffic patterns
- Rate limiting only triggers at prod scale
- User workflows reveal edge cases QA didn't anticipate

**Conclusion:** The question isn't "if" but "how safely"

---

### Section 2: How to Test in Production Safely (700 words)

**Framework: Three pillars**

#### 2a. Observability (200 words)
- Must have visibility before TiP
- Metrics, logs, traces as baseline
- Alerting on anomalies
- Example: SLO-based monitoring

#### 2b. Progressive Delivery (300 words)
- Feature flags for kill switches
- Canary releases (1% → 10% → 100%)
- Blue-green deployments
- A/B testing as TiP in disguise
- Example: Rolling out payment processor change

#### 2c. Risk Management (200 words)
- Circuit breakers for failure isolation
- Rate limiting to contain blast radius
- Automated rollback triggers
- Runbooks for common scenarios

---

### Section 3: When NOT to Test in Production (250 words)

**Maturity gates:**
- Don't TiP before you have observability
- Don't TiP with irreversible operations (financial transactions, data deletion)
- Don't TiP with PII without data protection

**Risk scenarios to avoid:**
- Compliance-heavy domains (healthcare, finance) without approval
- Systems with legal liability (e.g., medical devices)
- When you can't quickly rollback

**Point:** TiP is an advanced practice, not a beginner move

---

### Conclusion: Adoption Path (200 words)

**Maturity model:**
1. **Level 1:** Staging-only, no TiP
2. **Level 2:** Observability in place, passive monitoring in prod
3. **Level 3:** Feature flags + canary releases
4. **Level 4:** Automated progressive delivery + risk controls
5. **Level 5:** TiP as default, staging for integration only

**Call to action:** Assess your current level, focus on next step

**Final thought:** "The safest way to test in production is to test in production deliberately, not accidentally."

---

## Target length

1500-2000 words total (currently structured for ~1700)

---

## Tone notes

- Authoritative but not preachy
- Acknowledge trade-offs
- Use concrete examples, avoid abstractions
- Speak to manager concerns (risk, value, team readiness)

---

**Next:** Formalize this into a Writing Brief (Formalize stage)
