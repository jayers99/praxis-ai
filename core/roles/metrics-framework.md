# Role Metrics Framework
**Canonical Reference (v1.0)**

This document defines metrics for tracking role effectiveness and identifying improvement opportunities.

## Authority

This document is **advisory**. Metrics collection is optional but recommended for continuous improvement.

---

## Purpose

Tracking role metrics enables:
1. Identifying bottlenecks in the review process
2. Improving role definitions based on patterns
3. Balancing role workload
4. Measuring quality improvements over time

---

## Core Metrics

### Process Metrics

#### Kickback Rate by Role

**Definition:** Percentage of reviews resulting in KICKBACK vs. APPROVE.

**Formula:** `(KICKBACK count) / (Total reviews) × 100`

**Interpretation:**
- High rate (>50%): May indicate upstream quality issues or overly strict standards
- Low rate (<10%): May indicate rubber-stamping or insufficient scrutiny
- Target range: 15-35% depending on phase maturity

**Collection:** Count verdict types per role per period.

---

#### Time-to-Resolution

**Definition:** Time from KICKBACK to subsequent APPROVE.

**Formula:** `APPROVE timestamp - KICKBACK timestamp`

**Interpretation:**
- Long resolution times: Kickback criteria may be unclear
- Short resolution times: System working well
- Very short (<1 hour): May indicate superficial fixes

**Collection:** Track timestamps on review iterations.

---

#### Review Cycle Count

**Definition:** Number of review iterations before APPROVE.

**Formula:** `Count of reviews for same artifact`

**Interpretation:**
- 1 cycle: First-time approval (ideal for mature processes)
- 2 cycles: Normal for complex items
- 3+ cycles: Process friction, unclear requirements, or scope issues

**Collection:** Count reviews per artifact.

---

#### Role Invocation Frequency

**Definition:** How often each role is invoked per phase.

**Interpretation:**
- Roles not being invoked: May be overlooked or redundant
- Roles always invoked: May be overloaded or too broadly scoped
- Uneven distribution: May indicate process bottlenecks

**Collection:** Count invocations per role per phase.

---

### Quality Metrics

#### Escaped Defects by Role

**Definition:** Issues that should have been caught by a role but weren't.

**Formula:** `(Defects attributed to role gap) / (Total defects) × 100`

**Interpretation:**
- High escape rate: Role coverage or definition needs improvement
- Pattern analysis: Which kickback triggers are being missed?

**Collection:** Post-incident attribution to role gaps.

---

#### Kickback Trigger Distribution

**Definition:** Which kickback triggers are most frequently cited.

**Interpretation:**
- Concentrated triggers: Systemic upstream issues
- Distributed triggers: General quality variance
- Never-used triggers: May be obsolete or unclear

**Collection:** Categorize kickbacks by trigger type.

---

#### False Positive Rate

**Definition:** Kickbacks that were overturned or deemed unnecessary.

**Formula:** `(Overturned kickbacks) / (Total kickbacks) × 100`

**Interpretation:**
- High rate: Role may be too strict or misaligned
- Pattern analysis: Which triggers produce false positives?

**Collection:** Track kickback appeals and outcomes.

---

### Collaboration Metrics

#### Cross-Role Conflict Rate

**Definition:** How often roles disagree requiring Synthesis adjudication.

**Formula:** `(Synthesis adjudications) / (Multi-role reviews) × 100`

**Interpretation:**
- High rate: Roles may have unclear boundaries
- Low rate: Healthy collaboration or insufficient scrutiny
- Persistent conflicts: Need clearer decision precedence

**Collection:** Count Synthesis adjudications.

---

#### Collaboration Pattern Usage

**Definition:** How often composition patterns are used vs. ad-hoc combinations.

**Interpretation:**
- High pattern usage: System is mature and predictable
- Low pattern usage: May need more documented patterns
- New patterns emerging: Capture and formalize

**Collection:** Track composition pattern invocations.

---

## Role-Specific Metrics

### Research Librarian

| Metric | Target | Red Flag |
|--------|--------|----------|
| Citation completeness | 100% claims cited | >10% uncited claims |
| Research reuse rate | >50% in research-library | <20% reuse |
| Time-to-research | <30 min for standard queries | >2 hours |

### Product Owner

| Metric | Target | Red Flag |
|--------|--------|----------|
| Scope creep rate | <10% of issues | >25% scope changes |
| Decision time | <24 hours | >1 week without decision |
| Value articulation | 100% issues have value statement | >20% missing |

### Red Team

| Metric | Target | Red Flag |
|--------|--------|----------|
| Risk identification rate | >80% risks surfaced pre-release | >50% risks escaped |
| Constructive alternative rate | >90% kickbacks include alternative | <50% constructive |
| Pre-mortem accuracy | >50% identified risks validated | <20% accuracy |

### Developer

| Metric | Target | Red Flag |
|--------|--------|----------|
| First-pass acceptance | >70% | <50% |
| Estimation accuracy | ±25% | ±100% |
| Technical debt acknowledgment | 100% new debt documented | >20% undocumented |

### QA

| Metric | Target | Red Flag |
|--------|--------|----------|
| BDD format compliance | 100% | <80% |
| High-risk coverage | 100% high-risk scenarios tested | >20% gaps |
| Regression escape rate | <5% | >15% |

### Security

| Metric | Target | Red Flag |
|--------|--------|----------|
| Threat model coverage | 100% trust boundaries covered | >20% gaps |
| Vulnerability escape rate | 0 critical/high | Any critical escaped |
| Mitigation completion | 100% identified mitigations implemented | >20% incomplete |

### Architect

| Metric | Target | Red Flag |
|--------|--------|----------|
| ADR completeness | 100% significant decisions documented | >20% undocumented |
| Boundary violation rate | <5% | >15% |
| Over-design rate | <10% premature abstractions | >25% |

### SRE

| Metric | Target | Red Flag |
|--------|--------|----------|
| SLO coverage | 100% services have SLOs | >20% without SLOs |
| Runbook coverage | 100% known failures documented | >20% gaps |
| Error budget health | >25% remaining | <10% remaining |

### FinOps

| Metric | Target | Red Flag |
|--------|--------|----------|
| Cost estimate accuracy | ±20% | ±50% |
| Hidden cost discovery | >90% identified pre-commit | >30% post-commit surprises |
| ROI achievement | >80% projected ROI realized | <50% realized |

---

## Metrics Collection

### Manual Collection

For low-volume environments, collect metrics manually:

```markdown
## Role Metrics: [Period]

### Review Summary
| Role | Reviews | Approves | Kickbacks | Suggests |
|------|---------|----------|-----------|----------|
| Product Owner | X | Y | Z | W |
| ... | ... | ... | ... | ... |

### Kickback Triggers (Top 5)
1. [Trigger]: X occurrences
2. [Trigger]: Y occurrences
...

### Observations
- [Pattern observed]
- [Improvement opportunity]
```

### Automated Collection

For higher-volume environments, integrate with:
- Issue tracking systems (GitHub Issues, Jira)
- CI/CD pipelines
- Review tools (GitHub PR reviews)

Data points to capture:
- Review timestamp
- Role
- Verdict
- Triggers cited
- Resolution timestamp

---

## Using Metrics for Improvement

### Monthly Review

1. Calculate metrics for the period
2. Identify outliers and trends
3. Investigate root causes
4. Propose role definition or process changes
5. Track improvement in next period

### Quarterly Retrospective

1. Review 3-month trends
2. Identify systemic issues
3. Update role definitions if needed
4. Retire obsolete triggers
5. Add new triggers for emerging patterns

### Annual Audit

1. Comprehensive metrics review
2. Role definition refresh
3. Composition pattern updates
4. Metrics framework updates

---

## Metrics Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| Optimizing for metrics | Gaming the system | Use metrics as signals, not goals |
| Measuring everything | Analysis paralysis | Focus on actionable metrics |
| Ignoring context | Misleading conclusions | Always investigate before acting |
| Punitive metrics | Fear-based behavior | Use for improvement, not blame |
| Stale metrics | Outdated insights | Regular refresh and pruning |

---

## Metric Definitions Reference

### Calculation Templates

**Rate Metric:**
```
Rate = (Count of X) / (Count of Y) × 100
Period: [weekly/monthly/quarterly]
```

**Time Metric:**
```
Time = End timestamp - Start timestamp
Aggregation: [median/mean/p90]
Period: [weekly/monthly]
```

**Count Metric:**
```
Count = Sum of occurrences
Grouping: [by role/by phase/by trigger]
Period: [weekly/monthly]
```
