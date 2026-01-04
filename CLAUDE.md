# Praxis AI - Claude Code Instructions

## Project Overview

Praxis is a policy-driven AI workflow system that governs how ideas evolve into maintained outcomes. It provides deterministic behavior resolution based on Domain + Stage + Privacy + Environment.

**Workspace Model:** User projects live in `$PRAXIS_HOME/projects/`, separate from this framework repo.

## Issue Workflow

**See [CONTRIBUTING.md](CONTRIBUTING.md)** for the full issue framework.

**Quick reference for batching work:**

```bash
# Find ready-to-implement issues
gh issue list --label "maturity: shaped" --label "size: small"
gh issue list --label "maturity: formalized" --label "type: feature"
```

**Labels:**

- `maturity: raw|shaped|formalized` — Issue readiness
- `size: small|medium|large` — Effort estimate
- `type: feature|spike|chore` — Work type
- `priority: high|medium|low` — Importance

**Rhythm:** Batch issues by labels → Implement → PR → Merge → Close

**Session summaries:** Save to workspace-level bench: `$PRAXIS_HOME/bench/sessions/YYYY-MM-DD.md`

## Tech Stack

- **Language:** Python 3.12+
- **CLI Framework:** Typer
- **Validation:** Pydantic v2
- **Testing:** pytest + pytest-bdd (BDD with Gherkin)
- **Package Manager:** Poetry
- **Linting:** ruff
- **Type Checking:** mypy

## CLI Commands

```bash
praxis --help                 # All commands and options

# Core project commands
praxis new <name> --domain <d> --privacy <p>  # Create new project
praxis init --domain <d>      # Initialize existing directory
praxis validate [--strict]    # Validate governance config
praxis stage <stage>          # Transition lifecycle stage
praxis status                 # Show project status
praxis audit                  # Check domain best practices

# Workspace management
praxis workspace init|info    # Initialize or show workspace
praxis extensions list|add|remove|update
praxis examples list|add

# Stage templates and pipeline
praxis templates render       # Render stage docs
praxis pipeline init|status|run|accept|reject|refine

# Opinions framework
praxis opinions [--prompt]    # Show/export applicable opinions
```

## Key Concepts

### Lifecycle Stages (in order)

1. Capture → 2. Sense → 3. Explore → 4. Shape → 5. Formalize → 6. Commit → 7. Execute → 8. Sustain → 9. Close

**Critical Rule:** Formalize is a hard boundary. No execution without formalization artifacts.

**Iteration Mode:** Formalize is where iteration changes meaning. Before: _discovery_ (what is this?). After: _refinement_ (how good can it be?). Detecting scope change during Execute means regression to Formalize.

**Lifecycle Checklists:** Each stage has a canonical checklist at `core/checklists/{stage}.md` defining entry/exit criteria and guidance. Domain-specific addenda (e.g., `formalize-code.md`) provide additional context. Use `praxis status` to see applicable checklists for your current stage.

**Allowed Regressions (from `lifecycle.md`):**

| From    | Allowed To        |
| ------- | ----------------- |
| Execute | Commit, Formalize |
| Sustain | Execute, Commit   |
| Close   | Capture           |

### Domains

| Domain  | Purpose            | Formalize Artifact |
| ------- | ------------------ | ------------------ |
| Code    | Functional systems | `docs/sod.md`      |
| Create  | Aesthetic output   | `docs/brief.md`    |
| Write   | Structured thought | `docs/brief.md`    |
| Learn   | Skill formation    | `docs/plan.md`     |
| Observe | Raw capture        | (none required)    |

### Privacy Levels (least to most restrictive)

1. Public
2. Public–Trusted Collaborators
3. Personal
4. Confidential
5. Restricted

### Validation Model (ADR-002)

| Rule                         | Severity | Trigger                                   |
| ---------------------------- | -------- | ----------------------------------------- |
| Unknown domain/stage/privacy | Error    | Value not in allowed list                 |
| Missing formalize artifact   | Error    | stage ≥ commit AND artifact not found     |
| Invalid stage regression     | Warning  | Transition not in allowed table           |
| Privacy downgrade            | Warning  | privacy_level decreased from prior commit |

### Subtypes by Domain

| Domain  | Subtypes                                               |
| ------- | ------------------------------------------------------ |
| code    | cli, library, api, webapp, infrastructure, script      |
| create  | visual, audio, video, interactive, generative, design  |
| write   | technical, business, narrative, academic, journalistic |
| learn   | skill, concept, practice, course, exploration          |
| observe | notes, bookmarks, clips, logs, captures                |

## Opinions Framework

When working on a Praxis project with opinions:

1. **Check for opinions:** Look for `docs/opinions/` directory
2. **Read praxis.yaml:** Determine domain, stage, subtype
3. **Resolve applicable opinions:** Use inheritance chain:
   - `_shared/` → `{domain}/principles.md` → `{domain}/{stage}.md` → `subtypes/`
4. **Apply as guidance:** Opinions are advisory, not hard rules
5. **Note conflicts:** If user instruction conflicts with opinion, follow user
6. **Reference gates:** Use quality gates when evaluating stage readiness

Run `praxis opinions --prompt` to get formatted context for AI assistants.

### Opinion File Types

| File            | Purpose                                      |
| --------------- | -------------------------------------------- |
| `README.md`     | Domain/subtype navigation and overview       |
| `principles.md` | Cross-stage principles (apply to ALL stages) |
| `{stage}.md`    | Stage-specific opinions and quality gates    |

### AI Permissions by Domain

| Operation |  Code   | Create  |  Write  |  Learn  | Observe |
| --------- | :-----: | :-----: | :-----: | :-----: | :-----: |
| suggest   | Allowed | Allowed | Allowed | Allowed | Allowed |
| complete  | Allowed | Allowed | Allowed | Allowed | Blocked |
| generate  |   Ask   | Allowed |   Ask   | Allowed | Blocked |
| transform |   Ask   | Allowed |   Ask   | Allowed | Blocked |
| execute   |   Ask   |    —    |    —    |    —    |    —    |

## Project Structure

```
src/praxis/
  cli.py                 # Typer CLI entry point
  domain/                # Business models (stages, domains, privacy, opinions, pipeline)
  application/           # Services (validate, init, stage, status, audit, workspace, etc.)
  infrastructure/        # External concerns (YAML, git, filesystem, tool runners)

tests/
  features/              # Gherkin feature files
  step_defs/             # pytest-bdd step definitions

core/                    # Normative specifications (binding)
  spec/                  # sod.md, lifecycle.md, domains.md, privacy.md
  governance/            # layer-model.md, opinions-contract.md, guardrails.md
  ai/                    # AI behavior controls and model configs
  roles/                 # Praxis Roles subsystem

opinions/                # Advisory guidance (non-binding, by domain)
research-library/        # Cataloged research (see CATALOG.md)
docs/guides/             # User-facing tutorials
adr/                     # Architecture Decision Records
```

## Development Rules

### Architecture

This project follows **hexagonal architecture**:

- **Domain:** Pure business logic, no external dependencies
- **Application:** Orchestration, coordinates domain + infrastructure
- **Infrastructure:** External concerns (files, git, env vars)
- **CLI:** Thin Typer layer, delegates to application services

### When Implementing

- All work must respect the lifecycle model
- Policy validation is deterministic: Domain + Stage + Privacy + Environment → Behavior
- No skipping required artifacts (e.g., SOD required before Execute in Code domain)
- Use BDD tests (Gherkin features + pytest-bdd step definitions)
- Run `poetry run pytest && poetry run ruff check . && poetry run mypy .` before committing

### praxis.yaml Schema

```yaml
domain: code|create|write|observe|learn
stage: capture|sense|explore|shape|formalize|commit|execute|sustain|close
privacy_level: public|public-trusted|personal|confidential|restricted
environment: Home|Work
subtype: cli|library|api|... # Optional: enables subtype opinion resolution
coverage_threshold: 0-100 # Optional: minimum test coverage %
```

## Commands

```bash
# Run tests
poetry run pytest

# Run linting
poetry run ruff check .

# Run type checking
poetry run mypy .

# Run the CLI
poetry run praxis --help
poetry run praxis init --help
poetry run praxis validate --help
```

## References

**Key specs:** `core/spec/` (lifecycle.md, domains.md, privacy.md, sod.md)
**Governance:** `core/governance/` (opinions-contract.md, guardrails.md)
**User guides:** `docs/guides/` (user-guide.md, ai-setup.md, pkdp.md)
**ADRs:** `adr/` (001-policy-engine.md, 002-validation-model.md)
**Research:** `research-library/CATALOG.md` — master index
