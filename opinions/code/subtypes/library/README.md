---
domain: code
subtype: library
version: "1.0"
status: active
author: human
---

# Code × Library Subtype Opinions

> **Scope:** Reusable libraries and packages in the Code domain

## Quick Navigation

- [Principles](principles.md) — Cross-stage library principles
- Stages: *Use domain-level stage files*
- Variants: Python | JavaScript | Rust | Go

## Subtype at a Glance

| Aspect | Value |
|--------|-------|
| Primary artifact | Reusable package with stable public API |
| Quality signals | API clarity, versioning discipline, documentation |
| AI role | Ask before generating exports |
| Key risks | Breaking changes, API bloat, version confusion |

## Design Philosophy

Libraries embody the principle of **contracts and stability**:

- **Clear API surface** — Explicit exports, no accidental public APIs
- **Semantic versioning** — Breaking changes only in major versions
- **Documentation-first** — API is only as good as its documentation
- **Backward compatibility** — Old code should continue to work

## When to Use This Subtype

Choose `code.library` when:

- Building reusable packages for distribution
- Creating internal company libraries
- Developing framework components
- Publishing to package registries (PyPI, npm, crates.io)

## API Design Patterns

Match the conventions of:
- Standard libraries in your language ecosystem
- Well-known libraries in your domain (requests, lodash, serde)
- Framework extension patterns (Flask extensions, React hooks)

## Key Requirements

- Explicit export list (`__all__`, `pub`, `export`)
- Semantic versioning from first release
- Changelog tracking all changes
- Public API fully documented
- Deprecation warnings before removal

## Related Subtypes

- `code.cli` — If your library has a command-line interface
- `code.api` — If your library is primarily an HTTP API client

## References

- [API Design Principles](https://python.org/dev/peps/pep-0008/)
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
