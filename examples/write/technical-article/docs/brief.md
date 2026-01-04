# Writing Brief

**Domain:** Write

<!-- This template implements the Formalize Spine from lifecycle.md.
     All five sections are required before proceeding to Commit. -->

---

## 1. Intent & Outcome

<!-- What thesis or message are we communicating? Why now? Who reads it?
     Good example: "Article arguing that remote-first teams outperform
     hybrid setups. Target: engineering managers evaluating team structure.
     Timely: Q1 planning season when reorg decisions are made." -->

### Thesis

Testing in production (TiP) is a pragmatic necessity for modern distributed systems when implemented with proper observability, progressive delivery, and risk management practices. The question is not "should we test in prod?" but "how do we test in prod safely?"

### Project Context

- Title: "Testing in Production: A Pragmatic Approach for Modern Systems"
- Client/Stakeholder: Internal engineering blog (public)
- Occasion/Context: Part of ongoing series on engineering best practices

### Audience

**Primary:** Engineering managers and technical leads making decisions about quality practices and testing strategies

**Secondary:** Senior developers and architects implementing testing infrastructure

**What they know:** Basic CI/CD concepts, aware of staging vs. production environments, familiar with microservices architecture

**What they need:** Risk/value framing for TiP adoption, practical guidance on safe implementation, clarity on when NOT to use TiP

### Why Now

**Timing:** Engineering teams are increasingly adopting TiP practices (feature flags, canary deployments) but often lack explicit governance or understanding of the underlying principles. Article addresses this gap before practices become ad-hoc and inconsistent.

**Opportunity:** Growing industry acceptance of TiP (Google SRE, Charity Majors' observability work) creates receptive audience.

---

## 2. Scope & Boundaries

<!-- What's in, what's out, what are we assuming?
     Good example: In: Main argument + 3 supporting case studies.
     Out: Historical survey, competing frameworks. Assumption: Reader
     has basic familiarity with remote work terminology. -->

### In Scope

- Why TiP is necessary (production complexity, staging limitations)
- How to implement TiP safely (observability, progressive delivery, risk controls)
- When NOT to use TiP (maturity gates, risk scenarios)
- Maturity model for adoption (5-level progression)

### Out of Scope (Non-Goals)

- Detailed implementation guides for specific tools (Datadog, LaunchDarkly, etc.)
- Code examples or tutorials
- Historical survey of testing practices
- Comparison of TiP vs. traditional QA methodologies
- Chaos engineering (related but distinct practice)

### Assumptions

- Reader has basic understanding of CI/CD pipelines
- Reader works in a context where production deployments happen regularly (not waterfall)
- Reader's organization uses some form of staging/pre-production environment
- Reader is familiar with concepts like microservices, distributed systems

### Dependencies

- No external dependencies (no interviews, no proprietary data)
- Will cite publicly available sources (Google SRE book, Charity Majors' blog, progressive delivery papers)

---

## 3. Constraints

<!-- Boundaries that shape the writing.
     Good example: Voice: authoritative but accessible. Length: 1500-2000 words.
     Must cite at least 3 peer-reviewed sources. Platform: company blog. -->

### Voice & Tone

- **Authoritative but accessible:** Not academic, not condescending
- **Pragmatic:** Acknowledge trade-offs, avoid dogma
- **Concrete:** Use specific examples over abstractions
- **Manager-focused:** Speak to decision-maker concerns (risk, team readiness, ROI)

### Length & Format

- **Length:** 1500-2000 words (target: 1700)
- **Structure:** Hook + 3 main sections + conclusion with maturity model
- **Format:** Markdown for web publication
- **Sections:** Clear headers, scannable structure, bulleted lists where appropriate

### Source Requirements

- Cite at least 3 authoritative sources (Google SRE, observability thought leaders, progressive delivery research)
- No requirement for peer-reviewed sources (industry blog, not academic journal)
- Link to external resources where relevant

### Technical Constraints

- **Platform:** Internal engineering blog (Markdown → HTML conversion)
- **SEO:** Not a primary concern (internal audience)
- **Accessibility:** Standard web accessibility (proper heading hierarchy, alt text for any images)

### Time/Effort Cap

- **Maximum effort:** 6 hours total over 2 weeks
- **Breakdown:** 1h drafting, 2h revision, 1h editing/polish, 2h buffer
- **Deadline:** Finalized by end of month for publication

---

## 4. Execution Framing

<!-- How do we start? What could go wrong? What don't we know yet?
     Good example: First draft: outline + intro paragraph for tone check.
     Risk: Sources may not support thesis. Open question: Interview subject? -->

### First Draft Milestone

- **Deliverable:** Complete first draft following the outline from Shape stage
- **Validation:** Does the argument flow logically? Does the tone match the brief?
- **Feedback loop:** Share with 2 senior engineers for technical accuracy check

### Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Argument comes across as advocating recklessness | Medium | High | Emphasize "when NOT to TiP" section, include maturity gates |
| Too technical for manager audience | Medium | Medium | Focus on risk/value framing, limit technical jargon |
| Too long (exceeds word count) | Low | Low | Prioritize ruthlessly during revision, cut tangents |
| Reader feedback reveals flawed assumption | Low | Medium | Share draft with 2 reviewers who represent target audience |

### Open Questions

- Should we include a specific tool recommendation, or stay tool-agnostic? → **Resolved:** Stay tool-agnostic to avoid vendor bias
- Should we include diagrams (canary rollout visualization)? → **Deferred:** Start text-only, add diagram if feedback requests it

---

## 5. Commit Criteria

<!-- Unambiguous definition of success. When is this writing done? -->

### Message / Outline

- **Working headline:** "Testing in Production: A Pragmatic Approach for Modern Systems"
- **Key points:**
  1. Why TiP is necessary (can't replicate prod)
  2. How to do it safely (observability + progressive delivery + risk controls)
  3. When NOT to do it (maturity gates, irreversible operations)
  4. Adoption path (5-level maturity model)
- **Required details:** Concrete examples for each safety pillar, specific maturity levels

### Deliverables

- **Primary deliverable:** Published article on engineering blog (Markdown format)
- **Additional formats/variants:** None required (no social summary, no internal memo variant)

### Success Criteria

1. **Technical accuracy:** No factual corrections needed post-publication (2 technical reviewers approve)
2. **Tone validation:** Manager audience finds it persuasive and actionable (1 manager reviewer confirms)
3. **Length:** Final article is 1500-2000 words (within constraint)
4. **Publication:** Article published on engineering blog within 2-week timeline
5. **Engagement:** Article generates at least 3 meaningful comments or internal discussion threads (measure of resonance)

**Definition of done:** Article is published, factually accurate, and generates positive engagement from target audience.

---

<!-- Reference: See core/spec/lifecycle.md for Formalize Spine definition -->
