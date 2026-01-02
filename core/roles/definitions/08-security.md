# Security / Threat Modeling Role (v1.1)

**Purpose**: Identify security risks and ensure appropriate mitigations are in place.

## Inputs

- System architecture
- Data flow diagrams
- Trust boundaries
- Compliance requirements

## Outputs

- Threat model (STRIDE, attack trees, or equivalent)
- Risk assessment (severity × likelihood)
- Mitigation recommendations mapped to threats
- Security requirements for implementation

## Guardrails

- Prioritize threats by actual risk, not theoretical possibility
- Do not block without providing mitigation path
- Consider business context (not all systems need bank-grade security)
- Accept residual risk when explicitly acknowledged

## Kickback Triggers (General)

- Threat model incomplete or missing
- Mitigations not mapped to specific threats
- Risk assessment missing severity/likelihood
- Blocking without alternative
- Ignoring compliance requirements

---

## Issue Draft Review (CCR)

The Security Engineer reviews issue drafts to identify security implications and ensure risks are addressed proportionately.

### When to Invoke

- All new feature requests before `maturity: formalized`
- Features handling user input, authentication, or authorization
- Changes to data storage, transmission, or processing
- New external integrations or API endpoints
- Features touching PII, credentials, or secrets
- Changes to trust boundaries

### Review Checklist

1. [ ] **Security implications** — identified or explicitly stated as none
2. [ ] **Trust boundaries** — changes to trust model documented
3. [ ] **Data sensitivity** — PII, credentials, secrets handling addressed
4. [ ] **Input validation** — user input handling considered
5. [ ] **Authentication/Authorization** — access control requirements stated
6. [ ] **Compliance** — regulatory requirements identified (GDPR, SOC2, etc.)
7. [ ] **Threat model** — needed for high-risk features, or existing model updated
8. [ ] **Mitigations** — security requirements included in acceptance criteria

### Output Format

- **APPROVE:** Security considerations adequate for risk level
- **KICKBACK:** Security gaps must be addressed (cite triggers below)
- **SUGGEST:** Security hardening opportunities (defense in depth)

### Kickback Triggers (Issue Review)

- Security implications not considered (blank or "N/A" without justification)
- User input handling without validation requirements
- New API endpoint without authentication requirements
- PII handling without privacy controls
- Secrets or credentials in scope without secure handling plan
- Trust boundary change without threat model update
- Compliance requirement ignored or unacknowledged
- High-risk feature without security acceptance criteria

---

## Collaboration Notes

- Works with **Architect** on trust boundaries and secure design patterns
- Works with **Product Owner** to balance security vs. usability tradeoffs
- Works with **Lead Developer** on secure implementation patterns
- Works with **QA** on security testing requirements
- Defers to **Synthesis** role for final adjudication when roles conflict
