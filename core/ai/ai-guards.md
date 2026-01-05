# AI Guards Design — Praxis

Version: 0.1.0  
Status: **DRAFT — Design Under Review**  
Last Updated: 2025-12-25

---

## Purpose

This document defines the **design and structure of AI guard files** within Praxis.

AI guards control how AI systems (Claude, Copilot, Gemini, etc.) operate across:

- User environments
- Project domains
- Execution contexts

The goal is to:

- Maintain **one coherent reasoning system**
- Apply **environmental and organizational constraints late**
- Prevent accidental leakage between home and work contexts
- Keep principles, governance, and execution clearly separated

This document is **design-level**, not an implementation guide.

---

## Core Design Principles

The AI guards system is built on the following decisions:

1. **Reason once, translate late**

   - AI reasoning, principles, and workflows are invariant.
   - Tooling and compliance are applied as a final translation step.

2. **Environment is a user-level concern**

   - Home vs work is an external constraint profile.
   - Projects do not redefine environments.

3. **Domain is a project-level concern**

   - Projects define domain-specific guardrails and workflows.
   - Domains do not redefine user environments.

4. **External constraints are non-negotiable**

   - They constrain governance and execution.
   - They are enforced through guardrails, not opinion.

5. **AI front-ends are delivery formats**
   - `CLAUDE.md`, `COPILOT.md`, `GEMINI.md` are rendered outputs.
   - Praxis content is the source of truth.

---

## Relationship to Praxis Layers

AI guards span all three Praxis layers but do not replace them.

- **Opinions** provide bias and intent
- **Governance** defines authority and arbitration
- **Execution** applies guardrails

AI guard files are **execution-facing artifacts** generated from upstream structure.

This document itself lives at the **governance/structure boundary**.

---

## High-Level Structure

AI guard content is divided across **user-level** and **project-level** scopes.

### User-Level (Cross-Domain, Not Committed)

User-level AI guards define:

- Active environment
- Tool availability and mappings
- Communication and compliance posture

They apply across all domains and projects.

```text
~/.ai-guards/
  core.md            # Stable user preferences and invariants
  env.md             # Active environment selector (e.g., ENV=work|home)
  tools.md           # Preferred tools + sanctioned alternatives
  env/
    work.md          # Work-only external constraints
    home.md          # Home-only external constraints
```

The active environment is resolved entirely at user scope.
AI systems must not prompt for it by default.

---

### Project-Level (Domain-Specific, Committed)

Project-level AI guards define:

- Domain workflows
- Guardrails and practices
- Abstract tool roles (issue tracker, VCS, CI)

They must **not** embed environment-specific tooling.

```text
praxis/
  ai-guards/
    build.md
    write.md
    create.md
    learn.md
    ...
```

Domains assume user-level tool mappings will be applied later.

---

## AI Front-End Files

AI tools expect specific filenames. These are treated as **rendered artifacts**.

Examples:

- `CLAUDE.md`
- `COPILOT.md`
- `GEMINI.md`

Each front-end file should:

- Include or reference Praxis AI guard content
- Remain thin and declarative
- Contain no original logic

Conceptually:

```text
(core user guards)
+ (env overlay)
+ (project domain guards)
= AI front-end file
```

---

## Environment Handling (Resolved Design)

Environment is **collapsed to user-level**, but **not merged into a single file**.

Rationale:

- Prevents monolithic user files
- Allows safe environment switching
- Enables validation and leakage detection

Environment overlays contain **only external constraints**, such as:

- Regulatory posture (e.g., FDIC-regulated)
- Communication formality
- Tool availability restrictions
- Data and PII handling severity
- AI usage restrictions

They must not contain:

- Principles
- Domain workflows
- Personal opinions

---

## Tool Mapping Strategy

User-level tool mapping is explicit.

For each preferred tool:

- At least one sanctioned alternative may be defined
- Domains refer only to abstract roles

Example:

- Preferred: GitHub Issues
- Work alternative: Jira

This enables:

- Consistent reasoning
- Late translation
- Compliance-safe execution

---

## Validation and Safety

Projects may validate AI guard consistency by:

- Reading the active user environment
- Ensuring no forbidden tooling is referenced
- Failing fast on home→work leakage

Validation is:

- Mechanical
- Deterministic
- Non-negotiable

Governance does not arbitrate external constraint violations.

---

## Explicit Non-Goals

This design intentionally avoids:

- Multiple mental models per environment
- AI personas per context
- Prompt-time environment selection
- Embedding compliance logic in principles

---

## Implementation Status

**Version:** 0.2.0  
**Status:** **PARTIALLY IMPLEMENTED**  
**Last Updated:** 2026-01-05

### Completed Features

- ✅ Project-level guard files (`praxis/ai-guards/{domain}.md`)
- ✅ Environment overlay resolution (`~/.ai-guards/env.md` + `env/{home|work}.md`)
- ✅ Multi-vendor rendering (Claude, Copilot, Gemini)
- ✅ Guard composition logic with precedence rules
- ✅ Validation tooling with environment leakage detection
- ✅ CLI commands: `praxis guards render`, `praxis guards validate`, `praxis guards list`

### Pending Features

- ⏳ User-level guard files (`~/.ai-guards/core.md`, `~/.ai-guards/tools.md`)
- ⏳ Tool mapping strategy implementation
- ⏳ Example guard files and documentation
- ⏳ Integration with `praxis init` and `praxis new` commands

### Usage

```bash
# Render AI guards for Claude
praxis guards render --vendor claude

# Render for all vendors
praxis guards render --vendor all

# Validate guard composition
praxis guards validate

# List active guards
praxis guards list
```

See `/home/runner/work/praxis-ai/praxis-ai/docs/guides/ai-guards.md` for detailed setup instructions.

---

## Status

This document has moved from **DRAFT** to **PARTIALLY IMPLEMENTED**.

Next steps:

- Complete user-level guard file implementation
- Add comprehensive examples for each domain
- Create migration guide for existing CLAUDE.md files
- Document best practices for guard file organization

Until fully implemented, this document serves as the **authoritative design reference** for AI guard structure in Praxis.
