# Sustain — Post-Publication Updates

**Stage:** Sustain  
**Date:** 2025-02-01 onwards

---

## Post-Publication Activity Log

### Week 1 (2025-01-26 to 2025-02-01)

**Engagement metrics:**
- 247 views (exceeded baseline of 150 for technical articles)
- 5 comments, all constructive
- 3 Slack threads discussing TiP adoption
- 1 engineering manager cited article in sprint planning

**Issues found:**
- Typo in code comment example (line 47, "canary releaes" → "canary releases")
  - **Fix:** Corrected typo, republished (no contract change, stays in Sustain) ✓
  - **Date:** 2025-01-27

**Reader feedback:**
- Request for clarification: "What's a reasonable p95 latency threshold for automated rollback?"
  - **Response:** Added footnote clarifying thresholds are domain-specific, referenced SLO methodology
  - **Date:** 2025-01-28
  - **Impact:** Minor addition, still within Sustain (implementation detail, not contract change)

### Week 2 (2025-02-02 to 2025-02-08)

**Engagement:**
- Views dropped to 45 (normal decay pattern for evergreen content)
- 1 new comment asking about TiP in regulated industries
  - **Response:** Pointed to "When NOT to TiP" section, offered to write follow-up on compliance considerations
  - **Follow-up idea:** Captured in new project (Observe → Write transition)

**Content updates:**
- None needed

### Week 3 (2025-02-09 to 2025-02-15)

**Reader request:**
- "Can you add a section on cost implications of TiP (shadowing traffic = 2x compute)?"
  - **Analysis:** This is a valid point, but adding a new section (cost considerations) would expand scope beyond the original brief
  - **Decision:** **Regression trigger detected** — This request suggests a scope expansion (adding "Cost" as a fourth consideration alongside observability, progressive delivery, and risk management)
  - **Action:** Declined as out-of-scope for current article. Captured as seed for potential follow-up article: "The Hidden Costs of Testing in Production"
  - **Status:** Article remains in Sustain, new idea captured in separate project

### Month 2 (2025-03-01)

**Retrospective:**
- Article is stable, no further content changes needed
- Engagement has plateaued to ~10 views/week (typical for evergreen content in internal blog)
- No factual corrections required (success criteria met ✓)
- Article continues to be referenced in engineering discussions

**Potential future actions:**
- Consider updating if industry best practices shift significantly (e.g., new progressive delivery techniques become standard)
- Monitor for outdated examples (if specific tools mentioned become obsolete)

---

## Sustain vs. New Iteration — Decision Log

### What Stayed in Sustain (Implementation Extensions)

✓ Typo fixes  
✓ Minor clarifications (p95 threshold footnote)  
✓ Engagement tracking and metrics  
✓ Reader Q&A responses

### What Would Trigger New Iteration (Contract Changes)

✗ Adding "Cost" as a fourth pillar (scope expansion)  
✗ Changing the target audience from managers to developers  
✗ Restructuring the maturity model (core framework change)  
✗ Contradicting the thesis (e.g., "TiP is actually always reckless")

---

## Close Criteria (when to sunset this article)

This article will remain in Sustain until one of:
1. Industry practices shift significantly (e.g., TiP becomes universal default, making the argument moot)
2. Factual errors are discovered that undermine the core argument
3. Company policy changes make TiP guidance no longer relevant
4. Article is superseded by a v2 that addresses scope expansion (cost, compliance, etc.)

**Current status:** Healthy in Sustain, no close trigger anticipated

---

**Next stage:** Close (when sunset criteria met) or continue Sustain indefinitely
