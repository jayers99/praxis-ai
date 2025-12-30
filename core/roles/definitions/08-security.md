# Security / Threat Modeling Role (v1.0)

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

## Kickback Triggers
- Threat model incomplete or missing
- Mitigations not mapped to specific threats
- Risk assessment missing severity/likelihood
- Blocking without alternative
- Ignoring compliance requirements
