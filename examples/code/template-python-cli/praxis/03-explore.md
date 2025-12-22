# Explore: template-python-cli

**Stage:** Explore
**Domain:** Code
**Privacy:** Public

---

## Purpose

Evaluate options and run spikes to validate the template design before committing to a final form.

---

## Spike: Working CLI Implementation

**Goal:** Validate that the captured patterns work together in practice.

**Outcome:** ✅ Success

We built a working CLI with:
- Poetry project with all dependencies
- Hexagonal Architecture (cli.py → application → domain)
- BDD tests (Gherkin + step definitions)
- CLI integration tests
- Domain unit tests

**Results:**
- 7 tests passing
- `ruff check` clean
- `mypy` clean
- Commands working: `--help`, `helloworld`, `helloworld <name>`

---

## Options Considered

### 1. Include Working Example vs Empty Scaffold

| Option | Pros | Cons |
|--------|------|------|
| **Working example (chosen)** | Demonstrates patterns in action, tests validate setup | Slightly more to delete when customizing |
| Empty scaffold | Cleaner starting point | No validation that structure works, no test examples |

**Decision:** Include `helloworld` command as a working example. It's trivial to remove and provides immediate validation.

---

### 2. Infrastructure Layer

| Option | Pros | Cons |
|--------|------|------|
| **Empty placeholder (chosen)** | Shows where external integrations go, minimal overhead | Might confuse beginners |
| Omit entirely | Simpler for trivial CLIs | Loses architectural guidance |
| Include example (e.g., file I/O) | More complete demonstration | Adds complexity, may not apply to all CLIs |

**Decision:** Keep empty `infrastructure/` as a placeholder with `__init__.py` docstring explaining its purpose.

---

### 3. Test Organization

| Option | Pros | Cons |
|--------|------|------|
| **Separate BDD + unit tests (chosen)** | Clear separation of concerns, BDD for behavior, unit for logic | More files |
| Single test file | Simpler structure | Mixes concerns |
| Only BDD tests | Consistent approach | Harder for fine-grained testing |

**Decision:** Three test types:
- `tests/features/` + `tests/step_defs/` — BDD (acceptance)
- `tests/test_cli.py` — CLI integration
- `tests/test_domain.py` — Domain unit tests

---

## Risks Identified

1. **pytest-bdd complexity** — Step definitions require learning curve; mitigated by simple example
2. **Hexagonal layers overkill for trivial CLIs** — Acceptable trade-off for consistency and scalability

---

## Validation Checklist

- [x] Poetry install works
- [x] CLI runs with `--help`
- [x] `helloworld` command works with default and custom name
- [x] All tests pass (pytest)
- [x] Linting passes (ruff)
- [x] Type checking passes (mypy)
- [x] README Quick Start instructions are accurate

---

## Next Stage

All options evaluated, spike successful. Ready to advance to **Shape** to define the final template form.
