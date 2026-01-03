---
domain: code
subtype: cli
version: "1.0"
status: active
author: human
---

# Code × CLI Principles

> **Scope:** These principles apply across ALL lifecycle stages for CLI projects.

## Core Principles

### 1. Unix Philosophy Compliance

- **Statement:** Follow the Unix philosophy and GNU coreutils conventions
- **Rationale:** Users expect CLI tools to behave predictably in pipelines
- **Source:** Doug McIlroy, Unix Programmer's Manual (1978)
- **Severity:** must-have

### 2. Stdout/Stderr Separation

- **Statement:** Separate stdout (data) from stderr (diagnostics)
- **Rationale:** Enables piping and redirection without log noise
- **Source:** Unix convention, POSIX standard
- **Severity:** must-have

### 3. Meaningful Exit Codes

- **Statement:** Use meaningful, documented exit codes
- **Rationale:** Enables automation and script error handling
- **Source:** GNU coding standards
- **Severity:** must-have

### 4. Explicit Behavior

- **Statement:** Prefer explicit commands over implicit behavior
- **Rationale:** Reduces surprises and debugging difficulty
- **Source:** Principle of Least Surprise
- **Severity:** should-have

### 5. Backwards Compatibility

- **Statement:** Treat backwards compatibility as a first-class concern
- **Rationale:** CLI tools embedded in automation must not break
- **Source:** Semantic versioning principles
- **Severity:** must-have

### 6. Actionable Errors

- **Statement:** Errors must be actionable and non-ambiguous
- **Rationale:** Users need to know what went wrong and how to fix it
- **Source:** UX best practices
- **Severity:** should-have

## AI Guidelines (All Stages)

| Operation | Permission | Notes |
|-----------|------------|-------|
| suggest | Allowed | Can suggest flag names, help text |
| complete | Allowed | Can complete argument parsing |
| generate | Ask | Ask before generating new commands |
| transform | Ask | Ask before refactoring CLI structure |
| execute | Ask | Always ask before running commands |

## Anti-Patterns (All Stages)

### Hidden State

- **What:** Relying on implicit state files, environment, or caches
- **Why bad:** Breaks reproducibility and debugging
- **Instead:** Accept state explicitly via flags or environment variables

### Clever but Surprising Behavior

- **What:** Auto-detecting context and changing behavior
- **Why bad:** Surprises users in automation
- **Instead:** Require explicit flags for behavior changes

### Overloaded or Ambiguous Flags

- **What:** Flags that mean different things in different contexts
- **Why bad:** Confuses users and documentation
- **Instead:** One flag, one meaning

### Implicit Destructive Actions

- **What:** Deleting or overwriting without confirmation
- **Why bad:** Data loss in automation
- **Instead:** Require `--force` or `--yes` for destructive actions

### Breaking Changes Without Migration

- **What:** Changing flag names or output format without warning
- **Why bad:** Breaks automation
- **Instead:** Deprecation warnings, semantic versioning

## CLI Flag Conventions

| Flag | Purpose | Format |
|------|---------|--------|
| `--help`, `-h` | Show usage | Required |
| `--version`, `-v` | Show version | Required |
| `--verbose` | Increase output | Optional |
| `--quiet`, `-q` | Suppress output | Optional |
| `--json` | JSON output | Recommended for automation |
| `--force`, `-f` | Skip confirmations | For destructive actions |

## Influential Lineage

| Author | Key Contribution |
|--------|------------------|
| Doug McIlroy | Unix philosophy |
| Eric Raymond | Art of Unix Programming |
| Mitchell Hashimoto | Modern CLI patterns (Terraform, Vagrant) |
| Docker team | Subcommand hierarchy patterns |

## References

- [Production CLI Tool Opinion](../../cli.md) — Original guidance
- [GNU Coding Standards](https://www.gnu.org/prep/standards/)
- [12 Factor CLI Apps](https://medium.com/@jdxcode/12-factor-cli-apps-dd3c227a0e46)
