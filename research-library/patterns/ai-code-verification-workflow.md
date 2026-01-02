# AI Code Verification: A Practitioner's Framework

<!--
metadata:
  id: patterns-ai-code-verification-workflow-2026-01-01
  title: AI Code Verification Workflow
  date: 2026-01-01
  status: validated
  topic: patterns
  keywords: [ai-assisted, code-review, verification, trust-calibration, workflow, solo-developer]
  consensus: medium
  depth: comprehensive
  sources_count: 35
  ccr_status: mitigations-applied
-->

## Executive Summary

- **Verification, not review, is the new bottleneck.** AI generates code faster than humans can verify it. The constraint has shifted from "how fast can we write?" to "how well can we validate?"
- **Senior developers ship 2.5x more AI code** not because they trust it more, but because they verify better throughout the development cycle—not just at review time.
- **AI code has measurable quality gaps:** 1.7x more issues than human code, 45% security test failure rate, 1.57x more security vulnerabilities. Verification is non-optional.
- **Trust calibration is a skill, not a ruleset.** Elite practitioners have intuition that can't be fully codified. Heuristics are starting points for developing your own calibration.
- **The "70% problem" is real:** AI handles happy paths quickly but fails at edge cases, error handling, and architectural fit. The last 30% often takes longer than the first 70%.

## Consensus Rating

**Medium**: Core findings validated across 35+ sources. Key claims (METR RCT, senior developer gap, security failure rates) have strong empirical backing. Heuristic transferability and optimal verification allocation remain unvalidated assumptions.

---

## The Verification Bottleneck

### What Changed

Before AI coding assistants, the traditional constraint was code production:
- **Old constraint:** "How fast can we write code?"
- **New constraint:** "How well can we verify code?"

This is a **bottleneck inversion**. The METR randomized controlled trial found experienced developers were 19% *slower* with AI tools—while perceiving themselves 24% faster. The gap between perceived and actual productivity suggests verification overhead is underestimated.

### Why Review Alone Isn't Enough

Code review is one verification point, but treating it as THE bottleneck misses the bigger picture:

| Verification Point | When It Happens | What It Catches |
|-------------------|-----------------|-----------------|
| **Upstream** | Before code generation | Bad requirements, wrong approach |
| **Inline** | During development | Syntax errors, test failures, type mismatches |
| **Review** | Before merge | Logic errors, style issues, architectural misfit |
| **Post-merge** | After deployment | Integration bugs, production issues |

Research shows 67% of developers spend MORE time debugging AI code, and 68% spend more time on security issues. Optimizing only review while ignoring upstream and downstream verification creates false efficiency.

### The Senior Developer Advantage

Fastly's 2025 data revealed that senior developers ship 2.5x more AI-generated code to production. The key insight:

> Seniors ship more AI code **because they trust it less**, not because they trust it more.

They invest more in verification at every layer:
- Better prompts (upstream)
- Running code before review (inline)
- Deeper scrutiny of unfamiliar patterns (review)

---

## Three-Layer Verification Model

### Layer 1: Upstream Verification

**Goal:** Prevent bad code from being generated in the first place.

| Intervention | Why It Works |
|--------------|--------------|
| Clear requirements before prompting | AI can't infer what you don't specify |
| Familiar technology stack | AI hallucinates less for well-trained libraries |
| Break large tasks into small prompts | Reduces context drift and accumulated errors |
| Provide examples and constraints | Guides output toward known-good patterns |

**Failure mode:** Vague prompts → plausible-looking but subtly wrong code → expensive downstream debugging.

### Layer 2: Inline Verification

**Goal:** Catch issues during development, before formal review.

| Intervention | Why It Works |
|--------------|--------------|
| Run the code immediately | Catches obvious runtime errors |
| Write tests alongside generation | Forces specification of expected behavior |
| Type checking / linting | Catches API misuse and style drift |
| Manual spot-check of critical paths | Your intuition flags what tools miss |

**Failure mode:** "It compiles, ship it" → subtle bugs discovered in production.

### Layer 3: Review Verification

**Goal:** Final human quality gate before merge.

This is where trust calibration heuristics apply (see next section). Review is the last line of defense, not the only one.

| Intervention | Why It Works |
|--------------|--------------|
| Verification checklist | Ensures consistent coverage |
| Domain expert involvement | Catches issues generalists miss |
| Security-focused review for sensitive code | AI has 1.57x more security vulnerabilities |
| "Could I debug this?" test | If you can't maintain it, don't ship it |

**Failure mode:** Optimizing for review speed → escaped defects → debugging becomes the new bottleneck.

---

## Trust Calibration Heuristics

**Important:** These are starting points for developing your own calibration, not rules to follow blindly. The senior developer advantage comes from experience-based intuition that heuristics can only approximate.

### When to Trust More (Lighter Verification)

| Factor | Rationale |
|--------|-----------|
| **Familiar domain** | You can quickly spot when output deviates from known-good patterns |
| **Boring technology** | Stable, popular libraries have many correct examples in training data |
| **Mechanical task** | Boilerplate, data transformations, config have clear success criteria |
| **Comprehensive tests exist** | Safety net catches regressions |
| **Isolated scope** | Changes can't cascade; blast radius is small |

### When to Scrutinize (Heavier Verification)

| Factor | Rationale |
|--------|-----------|
| **Security surfaces** | 45% of AI code fails security tests; XSS 2.74x more common |
| **Outside your expertise** | You cannot validate what you don't understand |
| **Novel/recent libraries** | High hallucination risk for APIs outside training data |
| **Complex business logic** | AI lacks domain context; subtle incorrectness likely |
| **Architectural decisions** | AI doesn't understand system-wide implications |
| **Edge cases and error handling** | The "70% problem"—AI handles happy paths only |

### The Junior Developer Mental Model

A useful default for all AI code:

> Review as if this came from an enthusiastic but inexperienced team member who works fast but makes mistakes only experienced eyes catch.

This calibrates expectations appropriately without over- or under-trusting.

---

## Verification Budget Allocation

Rather than prescribing formal tiers, allocate your limited verification attention like a budget:

```
Available attention (finite) → Allocate based on risk × unfamiliarity × coverage gap
```

### Budget Allocation Matrix

|                    | High Test Coverage | Low Test Coverage |
|--------------------|-------------------|-------------------|
| **Familiar + Low Risk** | Skim (trust tests) | Write tests, then skim |
| **Familiar + High Risk** | Verify security surfaces | Deep review + tests |
| **Unfamiliar + Low Risk** | Run it, spot-check | Careful review |
| **Unfamiliar + High Risk** | Deep review, domain expert | Deep review + tests + expert |

### What Consumes Budget

- Reading unfamiliar code
- Verifying API correctness for novel libraries
- Tracing logic through multiple functions
- Security review
- Testing edge cases manually

### What Preserves Budget

- Comprehensive existing tests
- Code in your area of expertise
- Small, isolated changes
- Running code yourself before review

---

## Verification Checklist

Use before accepting any AI-generated code:

### Pre-Merge Checklist

- [ ] **Ran the code** — tested manually, not just read
- [ ] **Tests pass** — meaningful tests, not tautological assertions
- [ ] **Understand what it does** — could explain to a colleague
- [ ] **Could debug it** — would know where to look if it broke
- [ ] **Checked security surfaces** — input validation, auth, data handling
- [ ] **Verified dependencies** — all packages real, trusted, not hallucinated
- [ ] **Confirmed API correctness** — especially for novel libraries
- [ ] **Reviewed edge cases** — error handling, empty states, boundaries
- [ ] **Checked architectural fit** — matches team patterns and standards

### Red Flags (Stop and Investigate)

- [ ] Code uses APIs you don't recognize
- [ ] Error handling is missing or minimal
- [ ] Security-sensitive operations without validation
- [ ] Dependencies you've never heard of
- [ ] Code that "looks right" but you can't explain why it works

---

## Failure Modes

### What Can Go Wrong

| Failure Mode | Cause | Mitigation |
|--------------|-------|------------|
| **False confidence** | 85% "feel confident" but AI code has 1.7x more bugs | Trust behavior (tests pass), not feelings |
| **Alert fatigue** | Too many AI review comments | Configure AI tools to reduce noise |
| **Skill degradation** | Over-reliance on AI | Maintain ability to code without AI |
| **Speed over quality** | Optimizing review time | Measure escaped defects, not just velocity |
| **Misclassified risk** | High-risk code gets light review | When in doubt, scrutinize |

### The Debugging Trap

If you optimize review speed but AI code quality is lower, you've just moved the bottleneck:

```
Fast review → More code merged → More bugs in production → More debugging time
```

Net effect may be negative. Measure end-to-end cycle time, not just review time.

---

## Limitations and Open Questions

### What This Research Does Not Validate

1. **Review is THE bottleneck.** Evidence suggests verification broadly (not just review) is the constraint. Requirements, debugging, and coordination may be equally important.

2. **Formal tier systems work.** No major tech company uses explicit tiers. Meta's DRS is risk-gating (preventing SEVs), not review optimization. Implicit human judgment may outperform formal classification.

3. **These heuristics transfer to all developers.** Elite practitioner mental models may require experience to apply correctly. Codified rules without intuition may create false confidence.

4. **AI review tools save time.** Data ranges from 0.9% to 90% comment acceptance rates. Contradictory evidence suggests high context-dependence.

### Selection Bias Acknowledgment

Sources are weighted toward:
- AI tool vendors (CodeRabbit, Qodo, Greptile)
- Elite practitioners (Willison, Ball, Osmani)
- FAANG engineering blogs

Missing perspectives:
- Average developers at non-FAANG companies
- Failed tiered review implementations
- Teams that tried and abandoned AI code review

### Open Questions

1. What's the actual constraint? Value stream mapping on real teams would help.
2. Do codified heuristics improve junior developer calibration?
3. What's the misclassification cost when high-risk code gets light review?
4. Why do AI comment acceptance rates vary 0.9-90%?

---

## Sources

### Primary Sources (Empirical Studies)

1. [METR RCT: AI Impact on Experienced Developer Productivity](https://arxiv.org/abs/2507.09089) — 19% slower with AI tools (n=16, 246 tasks)
2. [Does AI Code Review Lead to Code Changes?](https://arxiv.org/html/2508.18771v1) — 0.9-19.2% AI comment acceptance rate (22,326 comments)
3. [Fastly: Senior Developers Ship 2.5x More AI Code](https://www.fastly.com/blog/senior-developers-ship-more-ai-code)
4. [Veracode GenAI Code Security Report](https://www.veracode.com/blog/genai-code-security-report/) — 45% security failure rate
5. [CodeRabbit: AI PRs Have 1.7x More Issues](https://www.theregister.com/2025/12/17/ai_code_bugs/)

### Secondary Sources (Engineering Practices)

6. [Google Engineering Practices - Speed](https://google.github.io/eng-practices/review/reviewer/speed.html)
7. [Meta Diff Risk Score](https://engineering.fb.com/2025/08/06/developer-tools/diff-risk-score-drs-ai-risk-aware-software-development-meta/)
8. [LLVM Code Review Policy](https://llvm.org/docs/CodeReview.html)
9. [GitLab Code Review Guidelines](https://docs.gitlab.com/development/code_review/)
10. [Chromium Code Reviews](https://chromium.googlesource.com/chromium/src/+/lkgr/docs/code_reviews.md)

### Practitioner Sources

11. [Simon Willison: How I Use LLMs to Help Me Write Code](https://simonw.substack.com/p/how-i-use-llms-to-help-me-write-code)
12. [Thorsten Ball: How I Use AI](https://registerspill.thorstenball.com/p/how-i-use-ai)
13. [Addy Osmani: The 70% Problem](https://addyo.substack.com/p/the-70-problem-hard-truths-about)
14. [Addy Osmani: Trust, But Verify Pattern](https://addyo.substack.com/p/the-trust-but-verify-pattern-for)
15. [Chelsea Troy: Reviewing Pull Requests](https://chelseatroy.com/2019/12/18/reviewing-pull-requests/)

### Counter-Evidence Sources

16. [LeadDev: Writing Code Was Never The Bottleneck](https://leaddev.com/velocity/writing-code-was-never-the-bottleneck)
17. [Harness 2025: 67% Spend More Time Debugging AI Code](https://thenewstack.io/is-ai-creating-a-new-code-review-bottleneck-for-senior-engineers/)
18. [Simon Willison: Normalization of Deviance](https://simonwillison.net/2025/Dec/10/normalization-of-deviance/)

### Industry Surveys

19. [Qodo State of AI Code Quality 2025](https://www.qodo.ai/reports/state-of-ai-code-quality/)
20. [Stack Overflow 2025 Developer Survey - LinearB Analysis](https://linearb.io/blog/stack-overflow-2025-developer-survey-autonomy-ai-trust)

---

_PKDP Status: CCR mitigations applied, HVA validated_
_Ingested: 2026-01-01_
