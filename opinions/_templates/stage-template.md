# Stage Template (Stage-Specific Opinions)

> **Purpose:** Opinions for a specific Domain × Stage combination
> **Use for:** `{domain}/{stage}.md` and `{domain}/subtypes/{subtype}/{stage}.md`

---

## Template

```markdown
---
domain: {{DOMAIN}}
stage: {{STAGE}}
version: "1.0"
status: draft
---

# {{DOMAIN_TITLE}} × {{STAGE_TITLE}} Opinions

> **Summary:** {{STAGE_SUMMARY}}

## Stage Context

| Aspect | {{STAGE_TITLE}} Stage |
|--------|------------------------|
| Entry criteria | {{ENTRY_CRITERIA}} |
| Exit criteria | {{EXIT_CRITERIA}} |
| Commitment level | {{COMMITMENT_LEVEL}} |
| AI role | {{AI_ROLE}} |

## Principles

### 1. {{STAGE_PRINCIPLE_1_NAME}}

- **Statement:** {{STAGE_PRINCIPLE_1_STATEMENT}}
- **Rationale:** {{STAGE_PRINCIPLE_1_RATIONALE}}
- **Source:** {{STAGE_PRINCIPLE_1_SOURCE}}
- **Severity:** {{SEVERITY}}

### 2. {{STAGE_PRINCIPLE_2_NAME}}

- **Statement:** {{STAGE_PRINCIPLE_2_STATEMENT}}
- **Rationale:** {{STAGE_PRINCIPLE_2_RATIONALE}}
- **Source:** {{STAGE_PRINCIPLE_2_SOURCE}}
- **Severity:** {{SEVERITY}}

## Quality Gates

Before advancing to **{{NEXT_STAGE}}**:

| Gate | Description | Severity |
|------|-------------|----------|
| G1 | {{GATE_1_DESCRIPTION}} | {{GATE_1_SEVERITY}} |
| G2 | {{GATE_2_DESCRIPTION}} | {{GATE_2_SEVERITY}} |
| G3 | {{GATE_3_DESCRIPTION}} | {{GATE_3_SEVERITY}} |

## Anti-Patterns

### {{STAGE_ANTI_PATTERN_1_NAME}}

- **What:** {{STAGE_ANTI_PATTERN_1_WHAT}}
- **Why bad:** {{STAGE_ANTI_PATTERN_1_WHY}}
- **Instead:** {{STAGE_ANTI_PATTERN_1_INSTEAD}}

### {{STAGE_ANTI_PATTERN_2_NAME}}

- **What:** {{STAGE_ANTI_PATTERN_2_WHAT}}
- **Why bad:** {{STAGE_ANTI_PATTERN_2_WHY}}
- **Instead:** {{STAGE_ANTI_PATTERN_2_INSTEAD}}

## Stage Transition Checklist

To advance from **{{STAGE_TITLE}}** → **{{NEXT_STAGE}}**:

- [ ] {{TRANSITION_CHECK_1}}
- [ ] {{TRANSITION_CHECK_2}}
- [ ] {{TRANSITION_CHECK_3}}
- [ ] {{TRANSITION_CHECK_4}}

## AI Guidance

### What AI Can Do

- {{AI_CAN_DO_1}}
- {{AI_CAN_DO_2}}
- {{AI_CAN_DO_3}}

### What AI Should Ask About

- {{AI_SHOULD_ASK_1}}
- {{AI_SHOULD_ASK_2}}

### What AI Should Avoid

- {{AI_SHOULD_AVOID_1}}
- {{AI_SHOULD_AVOID_2}}
- {{AI_SHOULD_AVOID_3}}

## Domain-Specific Examples (Optional)

| Input Type | Location | Notes |
|------------|----------|-------|
| {{EXAMPLE_TYPE_1}} | {{EXAMPLE_LOCATION_1}} | {{EXAMPLE_NOTES_1}} |
| {{EXAMPLE_TYPE_2}} | {{EXAMPLE_LOCATION_2}} | {{EXAMPLE_NOTES_2}} |

## References

- {{REFERENCE_1}}
- {{REFERENCE_2}}

---

*Last updated: {{DATE}}*
```

---

## Placeholders Reference

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{DOMAIN}}` | Lowercase domain | `code` |
| `{{STAGE}}` | Lowercase stage | `capture` |
| `{{DOMAIN_TITLE}}` | Title case domain | `Code` |
| `{{STAGE_TITLE}}` | Title case stage | `Capture` |
| `{{STAGE_SUMMARY}}` | One sentence purpose | "Opinions for the initial capture phase..." |
| `{{ENTRY_CRITERIA}}` | What must exist to enter | "Any input exists (idea, requirement)" |
| `{{EXIT_CRITERIA}}` | What must exist to exit | "Input stored in retrievable location" |
| `{{COMMITMENT_LEVEL}}` | Sunk cost at this stage | "None — abandonment is safe" |
| `{{AI_ROLE}}` | AI permission summary | "Suggest allowed; generation ask" |
| `{{NEXT_STAGE}}` | Stage that follows | `Sense` |
| `{{GATE_N_DESCRIPTION}}` | Quality gate | "Input has minimal metadata" |
| `{{GATE_N_SEVERITY}}` | Gate severity | `must-have`, `should-have`, `nice-to-have` |
| `{{SEVERITY}}` | Principle severity | `must-have`, `should-have`, `nice-to-have` |
| `{{DATE}}` | ISO date | `2025-12-28` |

---

## Stage Reference Table

Use this to populate stage context:

| Stage | Entry Criteria | Exit Criteria | Next Stage | Commitment |
|-------|----------------|---------------|------------|------------|
| capture | Any input exists | Input stored | sense | None |
| sense | Captured inputs | Problem articulated | explore | Low |
| explore | Sense complete | 2-3 directions exist | shape | Low |
| shape | Options exist | Direction chosen | formalize | Medium |
| formalize | Shape complete | SOD exists | commit | Medium |
| commit | SOD complete | Resources allocated | execute | High |
| execute | Commit complete | Artifact produced | sustain | High |
| sustain | Execute complete | Work retired/closed | close | Ongoing |
| close | Sustain complete | Leverage captured | (end) | Complete |

---

## Severity Definitions (Quality Gates)

| Severity | Meaning |
|----------|---------|
| `must-have` | Blocks stage advancement; cannot proceed without |
| `should-have` | Warning; proceed with caution and explicit acknowledgment |
| `nice-to-have` | Recommendation; no enforcement |

---

## Subtype Stage Variant

For subtype-specific stage opinions (e.g., `subtypes/cli/execute.md`):

1. Add `subtype: {{SUBTYPE}}` to frontmatter
2. Add `inherits` referencing domain stage file
3. Change title to `{{DOMAIN_TITLE}} × {{SUBTYPE_TITLE}} × {{STAGE_TITLE}} Opinions`
4. Focus on subtype-specific additions/overrides

```markdown
---
domain: {{DOMAIN}}
subtype: {{SUBTYPE}}
stage: {{STAGE}}
version: "1.0"
status: draft
inherits:
  - {{DOMAIN}}
  - {{DOMAIN}}/{{STAGE}}
---

# {{DOMAIN_TITLE}} × {{SUBTYPE_TITLE}} × {{STAGE_TITLE}} Opinions

> **Summary:** {{SUBTYPE_STAGE_SUMMARY}}

## Inherited Context

This file inherits from:
- [{{DOMAIN_TITLE}} principles](../../principles.md)
- [{{DOMAIN_TITLE}} × {{STAGE_TITLE}}](../../{{STAGE}}.md)
- [{{SUBTYPE_TITLE}} principles](../principles.md) (if exists)

The following are **additions** or **overrides** for {{SUBTYPE_TITLE}}.

## Additional Stage Context

| Aspect | {{SUBTYPE_TITLE}} at {{STAGE_TITLE}} |
|--------|---------------------------------------|
| Specific entry | {{SUBTYPE_ENTRY}} |
| Specific exit | {{SUBTYPE_EXIT}} |

## Additional Principles

{{SUBTYPE_STAGE_PRINCIPLES}}

## Additional Quality Gates

| Gate | Description | Severity |
|------|-------------|----------|
| SG1 | {{SUBTYPE_GATE_1}} | {{SEVERITY}} |

## Additional Anti-Patterns

{{SUBTYPE_ANTI_PATTERNS}}

## AI Guidance Adjustments

{{AI_ADJUSTMENTS}}

---

*Last updated: {{DATE}}*
```

---

## Notes

- Not every stage needs a file for every domain if there's nothing domain-specific to say
- Subtype stage files are optional; only create when subtype has meaningful differences
- Prefer fewer, higher-quality stage files over complete coverage with thin content
