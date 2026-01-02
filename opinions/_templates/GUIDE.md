# Opinion Templates Guide

> How to use templates to create consistent, well-structured opinion files.

---

## Overview

This directory contains templates for creating Praxis opinion files. Each template serves a distinct purpose:

| Template | Purpose | Creates |
|----------|---------|---------|
| [README-template.md](README-template.md) | Domain/subtype navigation and overview | `{domain}/README.md` |
| [principles-template.md](principles-template.md) | Cross-stage principles | `{domain}/principles.md` |
| [stage-template.md](stage-template.md) | Stage-specific opinions | `{domain}/{stage}.md` |

---

## File Types Explained

### 1. README.md (Navigation)

**What it does:** Provides navigation and scope for a domain or subtype.

**When to create:**
- Once per domain (required)
- Once per subtype that has additional opinions (optional)

**Key sections:**
- Quick Navigation — links to all related files
- Domain at a Glance — summary table
- When to Use — criteria for choosing this domain
- Related Domains — cross-references

**Location:** `opinions/{domain}/README.md`

---

### 2. principles.md (Cross-Stage)

**What it does:** Defines principles that apply to ALL stages within a domain.

**When to create:**
- Once per domain (required)
- Once per subtype with additional principles (optional)

**Key sections:**
- Core Principles — named, sourced, severity-tagged
- AI Guidelines — permission table
- Anti-Patterns — things to avoid

**Location:** `opinions/{domain}/principles.md`

---

### 3. {stage}.md (Stage-Specific)

**What it does:** Defines opinions for a specific Domain × Stage combination.

**When to create:**
- For stages where the domain has specific opinions (optional per stage)
- Priority stages: capture, formalize, execute, sustain

**Key sections:**
- Stage Context — entry/exit/commitment/AI role
- Principles — stage-specific principles
- Quality Gates — conditions for advancement
- Anti-Patterns — stage-specific mistakes
- Stage Transition Checklist — practical checklist
- AI Guidance — what AI can/should/shouldn't do

**Location:** `opinions/{domain}/{stage}.md`

---

## Creation Workflow

### For a New Domain

1. **Start with README.md**
   - Copy template from `README-template.md`
   - Fill in domain scope and navigation
   - Creates: `{domain}/README.md`

2. **Create principles.md**
   - Copy template from `principles-template.md`
   - Define 3-5 core principles
   - Set AI permission table
   - Creates: `{domain}/principles.md`

3. **Create priority stage files**
   - Start with: `capture.md`, `formalize.md`, `execute.md`
   - Copy template from `stage-template.md`
   - Add stage-specific content
   - Creates: `{domain}/{stage}.md`

4. **Add remaining stages as needed**
   - Only create if there's domain-specific content
   - Empty or thin files are worse than no file

### For a New Subtype

1. **Create subtype README.md**
   - Use subtype variant from `README-template.md`
   - Creates: `{domain}/subtypes/{subtype}/README.md`

2. **Create subtype principles.md (if needed)**
   - Only if subtype has additional/different principles
   - Use subtype variant from `principles-template.md`
   - Creates: `{domain}/subtypes/{subtype}/principles.md`

3. **Create subtype stage files (if needed)**
   - Only for stages with subtype-specific content
   - Use subtype variant from `stage-template.md`
   - Creates: `{domain}/subtypes/{subtype}/{stage}.md`

---

## Frontmatter Requirements

All opinion files must have YAML frontmatter:

### Required Fields

```yaml
---
domain: code          # Required: code | create | write | learn | observe
version: "1.0"        # Required: semver string
status: draft         # Required: draft | active | deprecated
---
```

### Optional Fields

```yaml
---
stage: capture        # For stage files only
subtype: cli          # For subtype files only
inherits:             # Explicit inheritance chain
  - code
  - code/subtypes/cli
author: human         # human | ai | hybrid
last_reviewed: 2025-12-28
---
```

---

## Severity Levels

Use consistently across all files:

| Severity | Meaning | Enforcement |
|----------|---------|-------------|
| `must-have` | Required | Blocks advancement if violated |
| `should-have` | Important | Warning, requires acknowledgment |
| `nice-to-have` | Suggested | No enforcement |

---

## Quality Checklist

Before committing a new opinion file:

- [ ] Frontmatter is valid YAML with required fields
- [ ] Status is set to `draft` for new files
- [ ] Principles have Statement, Rationale, Source, Severity
- [ ] AI Guidelines table is complete
- [ ] Anti-patterns explain What, Why bad, Instead
- [ ] Date placeholder replaced with actual date
- [ ] File is in correct location per contract

---

## Common Mistakes

### 1. Thin Stage Files
**Problem:** Creating a stage file with only 1-2 sentences.
**Solution:** Only create stage files when there's substantive, stage-specific content.

### 2. Missing Sources
**Problem:** Principles without attribution.
**Solution:** Every principle needs a Source — even if it's "Praxis philosophy".

### 3. Inconsistent Severity
**Problem:** Using "required" instead of "must-have".
**Solution:** Use only: `must-have`, `should-have`, `nice-to-have`.

### 4. Placeholder Leftovers
**Problem:** `{{DATE}}` still in committed file.
**Solution:** Search for `{{` before committing.

---

## Inheritance Model

Opinions inherit from general to specific:

```
_shared/first-principles.md
    ↓
{domain}/principles.md
    ↓
{domain}/{stage}.md
    ↓
{domain}/subtypes/{subtype}/principles.md
    ↓
{domain}/subtypes/{subtype}/{stage}.md
```

**Merge rule:** Later opinions override earlier for conflicts; lists concatenate.

---

## AI Agent Instructions

When using AI to generate opinion files:

1. **Provide context:** Share this guide and the relevant template
2. **Specify domain research:** Point to research files that inform the domain
3. **Request draft status:** All AI-generated files should start as `draft`
4. **Review before commit:** Human review required before `active` status

---

## Related Files

- [opinions-contract.md](../../core/governance/opinions-contract.md) — Opinions framework specification
- [lifecycle.md](../../core/spec/lifecycle.md) — Stage definitions
- [domains.md](../../core/spec/domains.md) — Domain definitions
