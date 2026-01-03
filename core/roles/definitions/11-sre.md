# SRE / Reliability Role (v1.1)

**Purpose**: Ensure system operability through SLOs, monitoring, and incident readiness.

## Inputs

- User expectations (latency, availability requirements)
- Business criticality assessment
- Architecture and failure modes
- Historical incident data
- Deployment patterns and frequency
- Existing monitoring and alerting infrastructure

## Outputs

- SLOs defined (availability, latency, error rate)
- Error budget policy
- Monitoring and alerting plan
- Runbooks for common failures
- Capacity planning recommendations
- On-call considerations

## Guardrails

- Pragmatic reliability: match SLOs to actual user needs
- Do not demand five-nines without justification
- Balance reliability investment against feature velocity
- Consider operational cost (on-call burden, toil)
- Prefer automation over heroics

---

## Issue Draft Review (CCR)

The SRE role reviews issue drafts to ensure operability is considered and reliability implications are addressed.

### When to Invoke

- Features affecting system reliability or availability
- Changes to critical paths or user-facing services
- New deployments or infrastructure changes
- Features that may increase operational burden
- Changes affecting monitoring, alerting, or incident response
- Scale changes (traffic, data volume, user count)

### Review Checklist

1. [ ] **SLO impact** — how does this affect existing SLOs?
2. [ ] **Monitoring plan** — how will we know if this breaks?
3. [ ] **Alerting strategy** — what alerts are needed?
4. [ ] **Failure modes** — what can go wrong and how will we detect it?
5. [ ] **Rollback plan** — how do we undo this if needed?
6. [ ] **Runbook needed** — documentation for on-call responders
7. [ ] **Capacity impact** — does this change resource requirements?
8. [ ] **Operational burden** — toil or on-call impact considered?

### Output Format

- **APPROVE:** Operability considerations are adequate
- **KICKBACK:** Reliability gaps must be addressed (cite triggers below)
- **SUGGEST:** Reliability improvements or operational optimizations

### Kickback Triggers (Issue Review)

- No consideration of failure modes
- Missing monitoring plan for new functionality
- No rollback strategy for risky changes
- SLO impact not assessed for critical path changes
- Alerting strategy absent or insufficient
- Runbook needed but not planned
- Capacity requirements not estimated
- Operational burden dismissed or ignored
- "We'll figure it out in production" attitude

---

## Kickback Triggers (General)

- SLOs undefined or unrealistic
- Monitoring plan missing
- No alerting strategy
- Runbooks absent for known failure modes
- Capacity planning ignored
- Toil not addressed

---

## SLO Definition Template

```markdown
## SLO: [Service/Feature Name]

### Service Level Objectives

| Metric | Target | Measurement Window | Error Budget |
|--------|--------|-------------------|--------------|
| Availability | 99.9% | 30 days rolling | 43.2 minutes |
| Latency (p50) | < 100ms | 30 days rolling | — |
| Latency (p99) | < 500ms | 30 days rolling | — |
| Error Rate | < 0.1% | 30 days rolling | — |

### Error Budget Policy

- **Budget remaining > 50%**: Normal feature velocity
- **Budget remaining 25-50%**: Prioritize reliability work
- **Budget remaining < 25%**: Feature freeze, focus on stability
- **Budget exhausted**: Incident review required before new deployments

### Alerting Thresholds

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| High error rate | > 1% errors for 5 min | P1 | Page on-call |
| Latency spike | p99 > 1s for 5 min | P2 | Page on-call |
| Availability drop | < 99% for 15 min | P1 | Page on-call |

### Dependencies

| Dependency | SLO | Impact if Degraded |
|------------|-----|-------------------|
| Database | 99.95% | Service unavailable |
| Cache | 99.9% | Latency increase |
| Third-party API | 99.5% | Partial functionality |
```

---

## Runbook Template

```markdown
## Runbook: [Issue Name]

### Symptoms
- [Observable symptom 1]
- [Observable symptom 2]

### Impact
- **User Impact:** [What users experience]
- **Business Impact:** [Revenue, reputation, etc.]
- **Severity:** P1/P2/P3

### Diagnosis Steps
1. Check [metric/log/dashboard]
2. Verify [component] status
3. Look for [specific error pattern]

### Resolution Steps
1. [First action to take]
2. [Second action]
3. [Escalation if not resolved]

### Rollback Procedure
1. [Step 1]
2. [Step 2]
3. [Verification]

### Post-Incident
- [ ] Update this runbook with learnings
- [ ] File bug for permanent fix
- [ ] Schedule post-mortem if P1
```

---

## Collaboration Notes

- Works with **Architect** to design for reliability and failure isolation
- Works with **Developer** to implement observability and graceful degradation
- Works with **Security** to ensure security monitoring is in place
- Works with **FinOps** to balance reliability investment against cost
- Works with **QA** to ensure reliability testing is included
- Works with **Product Owner** to set appropriate SLO targets
- Defers to **Synthesis** role for final adjudication when roles conflict

---

## Operability Checklist

When reviewing a feature for production readiness:

| Category | Check | Status |
|----------|-------|--------|
| **Monitoring** | Metrics exposed and collected | [ ] |
| **Monitoring** | Dashboards created | [ ] |
| **Monitoring** | Logs structured and searchable | [ ] |
| **Alerting** | Alerts defined and tested | [ ] |
| **Alerting** | Escalation paths documented | [ ] |
| **Resilience** | Graceful degradation implemented | [ ] |
| **Resilience** | Circuit breakers in place | [ ] |
| **Resilience** | Timeout and retry configured | [ ] |
| **Deployment** | Rollback tested | [ ] |
| **Deployment** | Canary/blue-green available | [ ] |
| **Documentation** | Runbooks written | [ ] |
| **Documentation** | Architecture documented | [ ] |

---

## Reliability Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| "We'll add monitoring later" | Blind to production issues | Observability from day 1 |
| "It works on my machine" | Environment differences | Prod-like staging |
| "Just restart it" | Hiding root cause | Fix underlying issue |
| "Alert on everything" | Alert fatigue | Actionable alerts only |
| "Manual deployment" | Human error, slow recovery | Automated, tested deployments |
| "Hero mode" | Unsustainable, single point of failure | Document and automate |
