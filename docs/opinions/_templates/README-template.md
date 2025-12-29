# README Template (Domain/Subtype Overview)

> **Purpose:** Navigation, scope definition, links to other files
> **Use for:** Domain-level READMEs and Subtype-level READMEs

---

## Template

```markdown
---
domain: {{DOMAIN}}
version: "1.0"
status: draft
---

# {{DOMAIN_TITLE}} Domain Opinions

> **Scope:** {{SCOPE_DESCRIPTION}}

## Quick Navigation

- [Principles](principles.md) — Cross-stage principles for all {{DOMAIN_TITLE}} projects
- Stages:
  - [Capture](capture.md) | [Sense](sense.md) | [Explore](explore.md)
  - [Shape](shape.md) | [Formalize](formalize.md) | [Commit](commit.md)
  - [Execute](execute.md) | [Sustain](sustain.md) | [Close](close.md)
- Subtypes:
  {{SUBTYPE_LINKS}}

## Domain at a Glance

| Aspect | {{DOMAIN_TITLE}} Domain |
|--------|-------------------------|
| Primary artifact | {{PRIMARY_ARTIFACT}} |
| Quality signals | {{QUALITY_SIGNALS}} |
| AI role | {{AI_ROLE}} |
| Key risks | {{KEY_RISKS}} |

## When to Use This Domain

Use **{{DOMAIN_TITLE}}** when the primary deliverable:
{{USE_CRITERIA}}

## Related Domains

{{RELATED_DOMAINS}}

---

*Last updated: {{DATE}}*
```

---

## Placeholders Reference

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{DOMAIN}}` | Lowercase domain name | `code` |
| `{{DOMAIN_TITLE}}` | Title case domain name | `Code` |
| `{{SCOPE_DESCRIPTION}}` | One-sentence scope | "Software development projects — applications, tools, infrastructure, scripts." |
| `{{PRIMARY_ARTIFACT}}` | What this domain produces | "Working software" |
| `{{QUALITY_SIGNALS}}` | How you know work is good | "Tests pass, builds succeed, reviews approved" |
| `{{AI_ROLE}}` | AI permission summary | "Suggest/complete allowed; generate/execute ask" |
| `{{KEY_RISKS}}` | Main risks in this domain | "Security, maintainability, correctness" |
| `{{SUBTYPE_LINKS}}` | Links to subtypes | `[CLI](subtypes/cli/) | [Library](subtypes/library/)` |
| `{{USE_CRITERIA}}` | Bullet list of when to use | "- Compiles or interprets\n- Has automated tests" |
| `{{RELATED_DOMAINS}}` | Links to related domains | "- **Write** for documentation accompanying code" |
| `{{DATE}}` | ISO date | `2025-12-28` |

---

## Subtype README Variant

For subtype READMEs (e.g., `subtypes/cli/README.md`), adjust:

1. Add `subtype: {{SUBTYPE}}` to frontmatter
2. Change title to `{{DOMAIN_TITLE}} × {{SUBTYPE_TITLE}} Opinions`
3. Remove subtype links (or add sub-subtype links if applicable)
4. Focus scope on subtype-specific concerns

```markdown
---
domain: {{DOMAIN}}
subtype: {{SUBTYPE}}
version: "1.0"
status: draft
---

# {{DOMAIN_TITLE}} × {{SUBTYPE_TITLE}} Opinions

> **Scope:** {{SUBTYPE_SCOPE_DESCRIPTION}}

## Quick Navigation

- [Domain principles](../../principles.md) — Apply to all {{DOMAIN_TITLE}}
- [Subtype principles](principles.md) — Apply to all {{SUBTYPE_TITLE}}
- Stages (if subtype-specific):
  - [Execute](execute.md) | [Sustain](sustain.md)

## Subtype at a Glance

| Aspect | {{SUBTYPE_TITLE}} |
|--------|-------------------|
| Inherits from | {{DOMAIN_TITLE}} domain |
| Primary pattern | {{PRIMARY_PATTERN}} |
| Key considerations | {{KEY_CONSIDERATIONS}} |
| Tooling examples | {{TOOLING_EXAMPLES}} |

## When to Use This Subtype

Use **{{SUBTYPE_TITLE}}** when:
{{SUBTYPE_USE_CRITERIA}}

---

*Last updated: {{DATE}}*
```
