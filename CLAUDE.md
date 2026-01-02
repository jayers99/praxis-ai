# Praxis AI - Claude Code Instructions

## Project Overview

Praxis is a policy-driven AI workflow system that governs how ideas evolve into maintained outcomes. It provides deterministic behavior resolution based on Domain + Stage + Privacy + Environment.

**Current Phase:** Core CLI complete (`init`, `validate`, `stage`, `status`, `audit`) plus workspace management (`workspace`, `extensions`, `examples`), stage templates (`templates`), and knowledge distillation pipeline (`pipeline`).

**Workspace Model:** Praxis uses a workspace-based structure. User projects live in `$PRAXIS_HOME/projects/`, separate from this framework repo.

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
# Initialize a new project (run from within a project directory)
praxis init --domain code --privacy personal

# Validate governance configuration
praxis validate .
praxis validate --strict          # Treat warnings as errors
praxis validate --check-all       # Run tests, lint, types, coverage
praxis validate --check-coverage  # Check coverage threshold

# Transition lifecycle stage
praxis stage formalize
praxis stage execute --json       # JSON output for automation

# Show project status
praxis status                     # Current state, next steps, history
praxis status --json

# Audit against domain best practices
praxis audit                      # Check tooling, structure, testing
praxis audit --strict             # Fail on warnings

# Workspace management (requires PRAXIS_HOME env var)
praxis workspace init             # Initialize a new workspace
praxis workspace info             # Show workspace information

# Extension management
praxis extensions list            # List available extensions
praxis extensions add             # Interactive picker to install
praxis extensions add render-run  # Install specific extension
praxis extensions remove <name>   # Remove an extension
praxis extensions update          # Update all installed extensions

# Example management
praxis examples list              # List available examples
praxis examples add               # Interactive picker to install
praxis examples add uat-praxis-code  # Install specific example

# Template rendering
praxis templates render           # Render stage docs to current project
praxis templates render --stage formalize  # Render specific stage only
praxis templates render --force   # Overwrite existing files

# Knowledge distillation pipeline
praxis pipeline init              # Initialize a new pipeline
praxis pipeline status            # Show pipeline progress
praxis pipeline run               # Execute pipeline stage(s)
praxis pipeline accept            # Accept pipeline output (HVA stage)
praxis pipeline reject            # Reject pipeline output (HVA stage)
praxis pipeline refine            # Return to earlier stage for refinement

# Opinions framework
praxis opinions                   # Show applicable opinions for project
praxis opinions --prompt          # Generate AI context with opinions
praxis opinions --check           # Validate against quality gates
praxis opinions --list            # List all available opinion files
```

## Key Concepts

### Lifecycle Stages (in order)

1. Capture → 2. Sense → 3. Explore → 4. Shape → 5. Formalize → 6. Commit → 7. Execute → 8. Sustain → 9. Close

**Critical Rule:** Formalize is a hard boundary. No execution without formalization artifacts.

**Iteration Mode:** Formalize is where iteration changes meaning. Before: _discovery_ (what is this?). After: _refinement_ (how good can it be?). Detecting scope change during Execute means regression to Formalize.

**Allowed Regressions (from `lifecycle.md`):**

| From | Allowed To |
|------|------------|
| Execute | Commit, Formalize |
| Sustain | Execute, Commit |
| Close | Capture |

### Domains

| Domain | Purpose | Formalize Artifact |
|--------|---------|-------------------|
| Code | Functional systems | `docs/sod.md` |
| Create | Aesthetic output | `docs/brief.md` |
| Write | Structured thought | `docs/brief.md` |
| Learn | Skill formation | `docs/plan.md` |
| Observe | Raw capture | (none required) |

### Privacy Levels (least to most restrictive)

1. Public
2. Public–Trusted Collaborators
3. Personal
4. Confidential
5. Restricted

### Validation Model (ADR-002)

| Rule | Severity | Trigger |
|------|----------|---------|
| Unknown domain/stage/privacy | Error | Value not in allowed list |
| Missing formalize artifact | Error | stage ≥ commit AND artifact not found |
| Invalid stage regression | Warning | Transition not in allowed table |
| Privacy downgrade | Warning | privacy_level decreased from prior commit |

### Subtypes by Domain

| Domain | Subtypes |
|--------|----------|
| code | cli, library, api, webapp, infrastructure, script |
| create | visual, audio, video, interactive, generative, design |
| write | technical, business, narrative, academic, journalistic |
| learn | skill, concept, practice, course, exploration |
| observe | notes, bookmarks, clips, logs, captures |

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

| File | Purpose |
|------|---------|
| `README.md` | Domain/subtype navigation and overview |
| `principles.md` | Cross-stage principles (apply to ALL stages) |
| `{stage}.md` | Stage-specific opinions and quality gates |

### AI Permissions by Domain

| Operation | Code | Create | Write | Learn | Observe |
|-----------|:----:|:------:|:-----:|:-----:|:-------:|
| suggest | Allowed | Allowed | Allowed | Allowed | Allowed |
| complete | Allowed | Allowed | Allowed | Allowed | Blocked |
| generate | Ask | Allowed | Ask | Allowed | Blocked |
| transform | Ask | Allowed | Ask | Allowed | Blocked |
| execute | Ask | — | — | — | — |

## Project Structure

```
src/praxis/              # Main CLI package
  cli.py                 # Typer CLI entry point (all command groups)
  domain/                # Domain models and enums
    models.py            # Pydantic models (PraxisConfig, ValidationResult, etc.)
    stages.py            # Stage enum with comparison operators
    domains.py           # Domain enum
    privacy.py           # PrivacyLevel enum
    workspace.py         # Workspace, Extension, Example entities
    audit_checks.py      # Audit check definitions
    templates/           # Template domain models
    pipeline/            # Pipeline models, risk tiers, specialists
  application/           # Application services
    validate_service.py  # Validation orchestration
    init_service.py      # Project initialization
    stage_service.py     # Stage transition orchestration
    audit_service.py     # Audit check orchestration
    workspace_service.py # Workspace init, info orchestration
    extension_service.py # Extension add/remove/list/update logic
    templates/           # Template rendering service
    pipeline/            # Pipeline orchestration (CCR)
  infrastructure/        # External concerns
    yaml_loader.py       # YAML parsing
    yaml_writer.py       # YAML serialization
    artifact_checker.py  # File existence checks
    git_history.py       # Git operations (regression detection)
    env_resolver.py      # Environment variable handling
    templates.py         # CLAUDE.md and capture.md templates
    file_writer.py       # Safe file writes
    git_cloner.py        # Git clone/pull operations
    registry_loader.py   # Load extensions.yaml, examples.yaml
    workspace_config_repo.py  # Read/write workspace-config.yaml
    pyproject_loader.py  # pyproject.toml parsing
    claude_md_updater.py # CLAUDE.md update helper
    tool_runner.py       # Tool execution (tests, lint, etc.)
    stage_templates/     # Stage template resolution and rendering
    pipeline/            # Pipeline state persistence

tests/
  features/              # Gherkin feature files
  step_defs/             # pytest-bdd step definitions
  conftest.py            # Shared fixtures

core/                    # Normative specifications (binding)
  spec/                  # System specs (sod.md, lifecycle.md, domains.md, privacy.md)
  governance/            # Decision surfaces (layer-model.md, opinions-contract.md)
  ai/                    # AI behavior controls (ai-guards.md, models/)
  roles/                 # Praxis Roles subsystem

opinions/                # Advisory guidance (non-binding, by domain)
research-library/        # Cataloged research with structured metadata
  CATALOG.md             # Master index of all research artifacts
  ai-guards/             # AI instruction files and guard design
  domain/                # Domain-specific research
  foundations/           # Theoretical grounding, first principles
  patterns/              # Pattern library
  spec/                  # Research behind specifications
  roles/                 # Roles subsystem research
  subagents/             # Subagent research
docs/guides/             # User-facing tutorials (user-guide.md, ai-setup.md)
handoff/                 # Operational docs for agents
adr/                     # Architecture Decision Records

extensions.yaml          # Registry of available extensions
examples.yaml            # Registry of available examples
```

**Note:** User projects live at workspace level (`$PRAXIS_HOME/projects/`), not inside this repo. Examples and extensions are cloned to workspace via `praxis examples add` and `praxis extensions add`.

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
subtype: cli|library|api|...     # Optional: enables subtype opinion resolution
coverage_threshold: 0-100        # Optional: minimum test coverage %
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

**User-facing:**
- [User Guide](docs/guides/user-guide.md) — Step-by-step walkthrough
- [AI Setup](docs/guides/ai-setup.md) — CLAUDE.md templates and integration
- [Stage Templates](docs/guides/stage-templates.md) — Template system usage
- [PKDP Guide](docs/guides/pkdp.md) — Knowledge distillation pipeline

**Specification (core/):**
- [SOD](core/spec/sod.md) — Solution Overview Document
- [Lifecycle](core/spec/lifecycle.md) — Stage definitions, Formalize spine, Sustain governance
- [Domains](core/spec/domains.md) — Domain → artifact mappings
- [Privacy](core/spec/privacy.md) — Privacy levels and enforcement
- [Opinions Contract](core/governance/opinions-contract.md) — Opinions framework specification
- [Praxis Roles](core/roles/index.md) — Role definitions and lifecycle matrix

**Architecture:**
- [ADR-001](adr/001-policy-engine.md) — Policy engine decision
- [ADR-002](adr/002-validation-model.md) — Validation model specification

**Opinions:**
- [Templates Guide](opinions/_templates/GUIDE.md) — How to create opinion files
- [Code Domain](opinions/code/) — Code domain opinions and principles

**Examples (install via `praxis examples add`):**
- `uat-praxis-code` — Hello world CLI with full lifecycle docs
- `opinions-framework` — Opinions framework research and documentation

**Extensions (install via `praxis extensions add`):**
- `render-run` — AI image generation for Create domain
- `template-python-cli` — Python CLI scaffolding for Code domain

**Research Library:**
- [CATALOG.md](research-library/CATALOG.md) — Master index of all research artifacts
- [AI Guards](research-library/ai-guards/_index.md) — AI instruction files, memory, guard design
- [Foundations](research-library/foundations/_index.md) — Classical roots, library design, human-AI intent
- [Spec Research](research-library/spec/_index.md) — Lifecycle stages, domains, sustain governance
- [Roles Research](research-library/roles/_index.md) — Praxis roles architecture and rationale

## Research Workflow

When I say "research:" use subagent `researcher` with:
- Timebox: 20 minutes unless I specify otherwise
- Output: ONE report to `$PRAXIS_HOME/bench/research/` (staging area)
- Include citations + consensus strength per major claim
- Prefer primary/authoritative sources
- I may include seed links; read those first

After approval, use subagent `cataloger` to move approved research to `research-library/`.

To find existing research, use subagent `librarian` which reads from `research-library/CATALOG.md`.

