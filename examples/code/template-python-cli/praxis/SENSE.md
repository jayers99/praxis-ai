# Sense: template-python-cli

**Stage:** Sense
**Domain:** Code
**Privacy:** Public

---

## Purpose

Organize and summarize the patterns captured during the Capture stage into coherent themes.

---

## Themes

### 1. Project Structure

**Pattern:** src layout with Hexagonal Architecture

```
project_name/
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── __main__.py           # python -m entry
│       ├── cli.py                # Thin CLI (input adapter)
│       ├── domain/               # Core business logic
│       ├── application/          # Use cases (verbs)
│       └── infrastructure/       # External integrations (output adapters)
├── tests/
│   ├── features/                 # Gherkin scenarios (BDD)
│   ├── step_defs/                # Step implementations
│   ├── test_cli.py               # CLI integration tests
│   └── test_core.py              # Unit tests
├── praxis/                       # Governance files
├── pyproject.toml
├── CLAUDE.md
└── README.md
```

---

### 2. Tooling Stack

| Category              | Tool                | Rationale                                                  |
| --------------------- | ------------------- | ---------------------------------------------------------- |
| Dependency Management | Poetry              | Works at home + Work, modern pyproject.toml native         |
| CLI Framework         | Typer               | Type hints drive behavior, built on Click, auto-completion |
| Testing               | pytest + pytest-bdd | BDD outer loop (Gherkin), TDD inner loop                   |
| Linting + Formatting  | ruff                | Replaces black, flake8, isort — single tool                |
| Type Checking         | mypy                | Static type validation                                     |

---

### 3. Development Approach

**Outside-in development flow:**

```
BDD (What?) → TDD (How?) → DDD (Where?)
     │              │              │
     ▼              ▼              ▼
  Gherkin      Red-Green      Domain Model
  Scenarios    Refactor       Hexagonal Layers
```

1. **BDD** — Write Gherkin scenario (acceptance criteria)
2. **TDD** — Write failing test, implement, refactor
3. **DDD** — Structure code in domain/application/infrastructure layers

---

### 4. Architecture Pattern

**Hexagonal Architecture (Ports and Adapters)**

- **Core principle:** Domain at center, dependencies point inward
- **CLI is an input adapter** — thin, delegates to application layer
- **Infrastructure is an output adapter** — isolates external services
- **Benefits:** Testability, swappable adapters, clear boundaries

---

### 5. Praxis Governance

**Files:**

- `praxis.yaml` — Current state (domain, stage, privacy, environment)
- `{STAGE}.md` — Stage-specific artifacts (CAPTURE.md, SENSE.md, etc.)
- `CLAUDE.md` — AI context at project root

**Design principles:**

- Seamless handoff (assume context = 0)
- All decisions in files, not memory
- Stage files persist throughout lifecycle

---

## Observations

1. **Strong alignment** between BDD/TDD/DDD and Hexagonal Architecture — both emphasize separation of concerns and testability
2. **Tooling is consistent** across home and work environments (Poetry, pytest, ruff available at Work)
3. **Template complexity is moderate** — Hexagonal layers add structure but may be overkill for trivial CLIs

---

## Open Questions for Explore

1. Should the template include a minimal working example (hello command)?
2. How much scaffolding is too much? (e.g., empty domain/, application/, infrastructure/ dirs)
3. Should we include a sample Gherkin feature file?

---

## Next Stage

When patterns are clear and themes are validated, advance to **Explore** to consider options and run spikes.
