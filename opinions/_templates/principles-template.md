# Principles Template (Cross-Stage Principles)

> **Purpose:** Principles that apply to ALL stages within a domain or subtype
> **Use for:** `{domain}/principles.md` and `{domain}/subtypes/{subtype}/principles.md`

---

## Template

```markdown
---
domain: {{DOMAIN}}
version: "1.0"
status: draft
---

# {{DOMAIN_TITLE}} Domain Principles

> **Scope:** These principles apply across ALL lifecycle stages for {{DOMAIN_TITLE}} projects.

## Core Principles

### 1. {{PRINCIPLE_1_NAME}}

- **Statement:** {{PRINCIPLE_1_STATEMENT}}
- **Rationale:** {{PRINCIPLE_1_RATIONALE}}
- **Source:** {{PRINCIPLE_1_SOURCE}}
- **Severity:** {{SEVERITY}}

### 2. {{PRINCIPLE_2_NAME}}

- **Statement:** {{PRINCIPLE_2_STATEMENT}}
- **Rationale:** {{PRINCIPLE_2_RATIONALE}}
- **Source:** {{PRINCIPLE_2_SOURCE}}
- **Severity:** {{SEVERITY}}

### 3. {{PRINCIPLE_3_NAME}}

- **Statement:** {{PRINCIPLE_3_STATEMENT}}
- **Rationale:** {{PRINCIPLE_3_RATIONALE}}
- **Source:** {{PRINCIPLE_3_SOURCE}}
- **Severity:** {{SEVERITY}}

## AI Guidelines (All Stages)

| Operation | Permission | Notes |
|-----------|------------|-------|
| suggest | {{SUGGEST_PERMISSION}} | {{SUGGEST_NOTES}} |
| complete | {{COMPLETE_PERMISSION}} | {{COMPLETE_NOTES}} |
| generate | {{GENERATE_PERMISSION}} | {{GENERATE_NOTES}} |
| transform | {{TRANSFORM_PERMISSION}} | {{TRANSFORM_NOTES}} |
| execute | {{EXECUTE_PERMISSION}} | {{EXECUTE_NOTES}} |

## Anti-Patterns (All Stages)

### {{ANTI_PATTERN_1_NAME}}

- **What:** {{ANTI_PATTERN_1_WHAT}}
- **Why bad:** {{ANTI_PATTERN_1_WHY}}
- **Instead:** {{ANTI_PATTERN_1_INSTEAD}}

### {{ANTI_PATTERN_2_NAME}}

- **What:** {{ANTI_PATTERN_2_WHAT}}
- **Why bad:** {{ANTI_PATTERN_2_WHY}}
- **Instead:** {{ANTI_PATTERN_2_INSTEAD}}

## Influential Lineage (Optional)

These principles draw from:

| Author | Key Contribution |
|--------|------------------|
| {{AUTHOR_1}} | {{CONTRIBUTION_1}} |
| {{AUTHOR_2}} | {{CONTRIBUTION_2}} |

---

*Last updated: {{DATE}}*
```

---

## Placeholders Reference

| Placeholder | Description | Values |
|-------------|-------------|--------|
| `{{DOMAIN}}` | Lowercase domain name | `code`, `create`, `write`, `learn`, `observe` |
| `{{DOMAIN_TITLE}}` | Title case domain name | `Code`, `Create`, etc. |
| `{{PRINCIPLE_N_NAME}}` | Short principle name | "Correctness Over Cleverness" |
| `{{PRINCIPLE_N_STATEMENT}}` | Actionable statement | "Prefer clear, correct code over clever optimizations" |
| `{{PRINCIPLE_N_RATIONALE}}` | Why it matters | "Clever code is harder to maintain and debug" |
| `{{PRINCIPLE_N_SOURCE}}` | Attribution | "Clean Code (Martin)", "Praxis philosophy" |
| `{{SEVERITY}}` | How strict | `must-have`, `should-have`, `nice-to-have` |
| `{{*_PERMISSION}}` | AI permission level | `allowed`, `ask`, `blocked` |
| `{{*_NOTES}}` | Permission context | "Always", "User approval required" |
| `{{ANTI_PATTERN_N_NAME}}` | Pattern to avoid | "Premature Optimization" |
| `{{DATE}}` | ISO date | `2025-12-28` |

---

## Severity Definitions

| Severity | Meaning |
|----------|---------|
| `must-have` | Violation is an error; blocks stage advancement |
| `should-have` | Violation is a warning; proceed with caution |
| `nice-to-have` | Suggestion only; no enforcement |

---

## AI Permission Symbols

Use in table cells for visual scanning:

- `allowed` → "Allowed" or use checkmark if supported
- `ask` → "Ask" or use question mark
- `blocked` → "Blocked" or use X

---

## Subtype Principles Variant

For subtype-level principles (e.g., `subtypes/cli/principles.md`):

1. Add `subtype: {{SUBTYPE}}` to frontmatter
2. Change title to `{{DOMAIN_TITLE}} × {{SUBTYPE_TITLE}} Principles`
3. Add inheritance note referencing domain principles
4. Focus on subtype-specific additions/overrides

```markdown
---
domain: {{DOMAIN}}
subtype: {{SUBTYPE}}
version: "1.0"
status: draft
inherits:
  - {{DOMAIN}}
---

# {{DOMAIN_TITLE}} × {{SUBTYPE_TITLE}} Principles

> **Scope:** These principles apply to {{SUBTYPE_TITLE}} projects in addition to [{{DOMAIN_TITLE}} domain principles](../../principles.md).

## Inherited Principles

This file inherits all principles from `{{DOMAIN}}/principles.md`. The following are **additions** or **overrides** specific to {{SUBTYPE_TITLE}}.

## Additional Principles

### 1. {{SUBTYPE_PRINCIPLE_NAME}}

- **Statement:** {{SUBTYPE_PRINCIPLE_STATEMENT}}
- **Rationale:** {{SUBTYPE_PRINCIPLE_RATIONALE}}
- **Source:** {{SUBTYPE_PRINCIPLE_SOURCE}}
- **Severity:** {{SEVERITY}}

## AI Guidelines Adjustments

{{AI_ADJUSTMENTS_OR_NOTE}}

## Anti-Patterns ({{SUBTYPE_TITLE}}-Specific)

### {{SUBTYPE_ANTI_PATTERN_NAME}}

- **What:** {{SUBTYPE_ANTI_PATTERN_WHAT}}
- **Why bad:** {{SUBTYPE_ANTI_PATTERN_WHY}}
- **Instead:** {{SUBTYPE_ANTI_PATTERN_INSTEAD}}

---

*Last updated: {{DATE}}*
```
