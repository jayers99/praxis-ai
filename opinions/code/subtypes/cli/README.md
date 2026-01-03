---
domain: code
subtype: cli
version: "1.0"
status: active
author: human
---

# Code × CLI Subtype Opinions

> **Scope:** Command-line tools and utilities in the Code domain

## Quick Navigation

- [Principles](principles.md) — Cross-stage CLI principles
- Stages: *Use domain-level stage files*
- Variants: [Python](python/) | Shell | Go

## Subtype at a Glance

| Aspect | Value |
|--------|-------|
| Primary artifact | Executable CLI binary or script |
| Quality signals | Composability, predictability, stability |
| AI role | Ask before execution |
| Key risks | Breaking changes, hidden state, automation failures |

## Design Philosophy

CLI tools embody the Unix philosophy:

- **Do one thing well** — Clear, focused purpose
- **Composability** — Work in pipelines, respect stdin/stdout conventions
- **Predictability** — Deterministic behavior, stable output formats
- **Safety** — Explicit over implicit, no destructive defaults

## When to Use This Subtype

Choose `code.cli` when:

- Building command-line utilities
- Creating developer tools
- Implementing automation scripts meant for interactive or pipeline use
- Wrapping APIs or services for terminal access

## UX Patterns

Match the conventions of:
- HashiCorp tools (Terraform, Vault)
- Docker CLI
- AWS CLI
- GNU coreutils

## Key Requirements

- Safe for shell pipelines (stdout = data, stderr = diagnostics)
- Meaningful exit codes (0 = success, non-zero = specific errors)
- Help flags (`--help`, `-h`) on all commands
- Version flag (`--version`, `-v`)
- Backwards compatibility as a first-class concern

## Related Subtypes

- `code.script` — One-off automation (less rigor, shorter lifespan)
- `code.api` — If the CLI wraps or exposes a REST API

## References

- [Production CLI Tool Opinion](../../cli.md) — Legacy file (being migrated)
