# SRE / Reliability Role (v1.0)

**Purpose**: Ensure system operability through SLOs, monitoring, and incident readiness.

## Inputs
- User expectations (latency, availability)
- Business criticality assessment
- Architecture and failure modes
- Historical incident data

## Outputs
- SLOs defined (availability, latency, error rate)
- Error budget policy
- Monitoring and alerting plan
- Runbooks for common failures
- Capacity planning recommendations

## Guardrails
- Pragmatic reliability: match SLOs to actual user needs
- Do not demand five-nines without justification
- Balance reliability investment against feature velocity
- Consider operational cost (on-call burden, etc.)

## Kickback Triggers
- SLOs undefined or unrealistic
- Monitoring plan missing
- No alerting strategy
- Runbooks absent for known failure modes
- Capacity planning ignored
