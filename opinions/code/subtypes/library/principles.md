---
domain: code
subtype: library
version: "1.0"
status: active
author: human
---

# Code × Library Principles

> **Scope:** These principles apply across ALL lifecycle stages for library projects.

## Core Principles

### 1. Explicit Public API

- **Statement:** All public exports must be explicitly defined
- **Rationale:** Prevents accidental API surface and breaking changes
- **Source:** Python PEP 8, Rust API Guidelines
- **Severity:** must-have

### 2. Semantic Versioning

- **Statement:** Follow semantic versioning strictly (MAJOR.MINOR.PATCH)
- **Rationale:** Users depend on predictable upgrade paths
- **Source:** [semver.org](https://semver.org/)
- **Severity:** must-have

### 3. Documentation as Contract

- **Statement:** Public API documentation is part of the contract
- **Rationale:** Undocumented APIs are unusable or misused
- **Source:** Documentation-driven development
- **Severity:** must-have

### 4. Changelog Discipline

- **Statement:** Maintain a changelog tracking all changes
- **Rationale:** Users need to understand what changed between versions
- **Source:** [Keep a Changelog](https://keepachangelog.com/)
- **Severity:** must-have

### 5. Backwards Compatibility

- **Statement:** Treat backwards compatibility as default, breaking changes as exceptional
- **Rationale:** Libraries are embedded in user code; breaks cascade
- **Source:** Hyrum's Law
- **Severity:** must-have

### 6. Minimal Dependencies

- **Statement:** Minimize external dependencies to reduce version conflicts
- **Rationale:** Dependency hell is a real problem for library users
- **Source:** Unix philosophy, Go proverbs
- **Severity:** should-have

### 7. Version Consistency

- **Statement:** Version in code (`__version__`) must match package metadata
- **Rationale:** Prevents confusion and debugging difficulties
- **Source:** Packaging best practices
- **Severity:** must-have

## AI Guidelines (All Stages)

| Operation | Permission | Notes |
|-----------|------------|-------|
| suggest | Allowed | Can suggest API design patterns |
| complete | Allowed | Can complete function signatures |
| generate | Ask | Ask before generating new public exports |
| transform | Ask | Ask before refactoring public API |
| execute | Ask | Ask before running code that modifies exports |

## Anti-Patterns (All Stages)

### Implicit Public API

- **What:** Not using explicit export lists (`__all__`, etc.)
- **Why bad:** Any function becomes part of the API by accident
- **Instead:** Always define `__all__` or equivalent export mechanism

### Version Number Inconsistency

- **What:** Version in code differs from package version
- **Rationale:** Causes confusion, debugging nightmares
- **Instead:** Single source of truth, automated sync

### Undocumented Breaking Changes

- **What:** Making breaking changes without changelog entry
- **Why bad:** Users discover breaks in production
- **Instead:** Document all changes, especially breaking ones

### Dependency Creep

- **What:** Adding dependencies without justification
- **Why bad:** Creates version conflicts for users
- **Instead:** Evaluate if functionality can be internal

### Incomplete Deprecation

- **What:** Removing APIs without deprecation warnings
- **Why bad:** Users have no migration path
- **Instead:** Deprecate in one version, remove in next major

## Library Export Conventions

| Language | Mechanism | Example |
|----------|-----------|---------|
| Python | `__all__` in `__init__.py` | `__all__ = ["func", "Class"]` |
| JavaScript | `export` keyword | `export { func, Class }` |
| Rust | `pub` keyword | `pub fn func()` |
| Go | Capitalization | `func Exported()` |

## Influential Lineage

| Author | Key Contribution |
|--------|------------------|
| Guido van Rossum | Python packaging conventions |
| Rich Hickey | Spec-ulation keynote (breaking changes) |
| Steve Klabnik | Rust API guidelines |
| Semantic Versioning authors | Version number contract |

## References

- [Hyrum's Law](https://www.hyrumslaw.com/) — Observable behavior becomes depended upon
- [API Evolution](https://www.youtube.com/watch?v=oyLBGkS5ICk) — Rich Hickey's Spec-ulation
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- [Python Packaging Guide](https://packaging.python.org/)
