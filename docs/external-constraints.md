# External Constraints — Environmental Authority in Praxis

Version: 0.1.0  
Status: Active — Structural Artifact  
Last Updated: 2025-12-23

---

## Purpose

This document defines **External Constraints** within Praxis.

External constraints are forces that:
- Originate outside Praxis
- Are non-negotiable at execution time
- Constrain governance and execution
- Differ by environment (e.g., home vs work)

They represent **environmental reality**, not opinion or preference.

This document exists to make those forces explicit, visible, and usable.

---

## Definition

**External Constraints** are conditions imposed by law, policy, organization, platform, or environment that Praxis must comply with.

They:
- Cannot be overridden by principles
- Cannot be negotiated by governance
- Must be enforced through execution guardrails

Examples include:
- Legal and regulatory requirements
- Employer or client policies
- Security and data-handling rules
- Tooling and platform mandates

---

## Relationship to the Praxis Layer Model

External Constraints do **not** form a Praxis layer.

They sit *outside* the three-layer system and apply pressure inward.

```
        External Constraints
               ↓
Opinions  →  Governance  →  Execution
               ↑
           Learning
```

- Principles must respect external constraints
- Governance must operate within them
- Execution must comply with them

Violations are failures of compliance, not judgment.

---

## Constraint Categories (Taxonomy)

At this stage, constraints are categorized but not yet instantiated.

### Legal / Regulatory
- Laws
- Industry regulations
- Licensing requirements

### Security
- Data protection rules
- Access controls
- Threat and risk posture

### Data Handling
- Data residency
- Classification (public, internal, restricted)
- Retention and deletion rules

### Tooling / Platform
- Approved languages, libraries, and services
- Deployment environments
- Vendor and platform restrictions

### Organizational Process
- Required approvals
- Auditability
- Ticketing and change management

These categories are intentionally broad and stable.

---

## Environments

External constraints vary by **environment**.

An environment defines a constraint profile applied to execution.

Examples:
- **Home** — permissive, exploratory, low compliance
- **Work** — restrictive, audited, high compliance

Future environments may include:
- Client-specific
- Open-source
- Regulated sandbox

Specific constraints are *not* defined here.

---

## Relationship to Guardrails

External constraints are enforced through **guardrails**.

- Constraints describe *what must be true*
- Guardrails describe *how compliance is achieved during execution*

Guardrails derived from external constraints:
- Are non-negotiable in context
- Must be explicit
- Must reference their originating constraint

Governance does not arbitrate these guardrails; it only explains and routes around them.

---

## Relationship to Claude / AI Behavior

Claude behavior may vary by environment due to external constraints.

However:
- Reasoning and principles remain constant
- Only allowed actions and tooling change

This document serves as the upstream source for:
- Claude.md environment overlays
- AI behavior restrictions
- Compliance-aware automation

---

## Status

This document is intentionally minimal.

Next steps:
- Define environment-specific constraint profiles
- Reference constraints from guardrails
- Integrate with Claude.md transforms

Until then, this file defines **structure**, not rules.
