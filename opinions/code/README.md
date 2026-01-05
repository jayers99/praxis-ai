---
domain: code
version: "1.0"
status: draft
---

# Code Domain Opinions

> **Scope:** Software development projects — applications, tools, infrastructure, scripts.

## Quick Navigation

- [Principles](principles.md) — Cross-stage principles for all Code projects
- [Design Patterns](design-patterns.md) — Software design patterns and architectural guidance
- [Testing](testing.md) — Testing methodology and AI-assisted test generation
- Stages:
  - [Capture](capture.md) | [Sense](sense.md) | [Explore](explore.md)
  - [Shape](shape.md) | [Formalize](formalize.md) | [Commit](commit.md)
  - [Execute](execute.md) | [Sustain](sustain.md) | [Close](close.md)
- Subtypes:
  - [CLI](subtypes/cli/) | [Library](subtypes/library/) | [API](subtypes/api/)
  - [WebApp](subtypes/webapp/) | [Infrastructure](subtypes/infrastructure/) | [Script](subtypes/script/)

## Domain at a Glance

| Aspect | Code Domain |
|--------|-------------|
| Primary artifact | Working software |
| Quality signals | Tests pass, builds succeed, reviews approved |
| AI role | Suggest/complete allowed; generate/execute ask |
| Key risks | Security, maintainability, correctness |

## When to Use This Domain

Use **Code** when the primary deliverable is software that:
- Compiles or interprets
- Has automated tests
- Ships to users or other systems

## Boundary

- **In scope:** Output is executable/runnable code
- **Out of scope:** AI-generated art (even if tooling is code), documentation-only

## Subtypes

| Subtype | Description |
|---------|-------------|
| `cli` | Command-line tools and utilities |
| `library` | Reusable packages and modules |
| `api` | HTTP/REST/GraphQL services |
| `webapp` | Web applications with UI |
| `infrastructure` | IaC, DevOps, platform tooling |
| `script` | One-off automation scripts |

## Related Domains

- **Write** for documentation accompanying code
- **Learn** for skill development related to code
- **Create** for generative art that uses code as medium

---

*Last updated: 2025-12-28*
