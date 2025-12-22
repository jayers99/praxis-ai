# template-python-cli

## Current State

| Dimension | Value |
|-----------|-------|
| Domain | Code |
| Stage | Capture |
| Privacy | Public |
| Environment | Home |

## Purpose

Build a reusable Python CLI project template that validates the Praxis lifecycle.

## Active Artifact

- [praxis/CAPTURE.md](praxis/CAPTURE.md) — Gathering inputs and prior art

## Project Structure

```
template-python-cli/
├── src/                # Application source code
├── tests/              # Test suite
├── docs/               # Documentation
├── praxis/             # Praxis governance files
│   ├── praxis.yaml     # Current state
│   └── CAPTURE.md      # Active stage artifact
├── CLAUDE.md           # AI context (this file)
└── README.md           # Project overview
```

## Development Approach

- **BDD** — Behavior-Driven Development (outer loop, Gherkin scenarios)
- **TDD** — Test-Driven Development (inner loop, red-green-refactor)
- **DDD** — Domain-Driven Design (structure code around domain concepts)
- **Hexagonal Architecture** — Ports and Adapters (domain at center, infrastructure at edges)

## Stage Rules

### Capture
- Collect raw inputs with minimal friction
- No commitment or structure required
- Focus on: references, prior art, preferences, constraints

### Next Stage: Sense
Advance when sufficient inputs are gathered to organize and summarize patterns.

## Constraints

- Poetry for dependency management
- pytest + pytest-bdd for testing
- ruff for linting + formatting
- mypy for type checking

## Related

- [Issue #4](https://github.com/jayers99/praxis-ai/issues/4) — Parent issue
- [Praxis SOD](../../../docs/sod.md) — System specification
- [Lifecycle](../../../docs/lifecycle.md) — Stage definitions
