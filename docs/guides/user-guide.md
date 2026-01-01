# Praxis User Guide

This guide walks you through building a project using Praxis governance, from initial idea to maintained software.

---

## Prerequisites

1. Clone the praxis-ai repository
2. Install the Praxis CLI:

   ```bash
   cd praxis-ai
   poetry install
   ```

3. Verify installation:

   ```bash
   poetry run praxis --version
   ```

4. **(Recommended) Create a wrapper script** so you can run `praxis` from any directory with tab completion support:

   ```bash
   # Create a wrapper script (adjust path to your clone location)
   mkdir -p ~/bin
   cat > ~/bin/praxis << 'EOF'
   #!/bin/bash
   exec poetry -C "/path/to/praxis-ai" run praxis "$@"
   EOF
   chmod +x ~/bin/praxis
   ```

   Ensure `~/bin` is in your PATH (add to `~/.bashrc` or `~/.zshrc` if needed):

   ```bash
   export PATH="$HOME/bin:$PATH"
   ```

5. **(Optional) Enable tab completion** for shell autocompletion of commands and options:

   ```bash
   praxis --install-completion
   ```

   Restart your shell or source your config file. Then use `<tab><tab>` to see available completions.

6. **Configure your AI assistant** — See [AI Setup Guide](ai-setup.md) for CLAUDE.md templates and integration patterns

---

## Quick Reference

### Lifecycle Stages

| Stage         | Purpose                 | Key Question               |
| ------------- | ----------------------- | -------------------------- |
| **Capture**   | Collect raw inputs      | What is this?              |
| **Sense**     | Synthesize meaning      | What do we understand?     |
| **Explore**   | Investigate options     | What are our choices?      |
| **Shape**     | Define structure        | How will this work?        |
| **Formalize** | Lock scope (create SOD) | What are we committing to? |
| **Commit**    | Verify readiness        | Are we ready to build?     |
| **Execute**   | Build the thing         | Does it work?              |
| **Sustain**   | Maintain and evolve     | Is it healthy?             |
| **Close**     | Archive or sunset       | Is this done?              |

---

## CLI Commands

### praxis init

Initialize a new Praxis project:

```bash
praxis init [PATH] [OPTIONS]
```

| Option            | Description                                                               |
| ----------------- | ------------------------------------------------------------------------- |
| `PATH`            | Project directory (default: `.`)                                          |
| `--domain`, `-d`  | Project domain: code, create, write, observe, learn                       |
| `--privacy`, `-p` | Privacy level: public, public-trusted, personal, confidential, restricted |
| `--env`, `-e`     | Environment: Home, Work (default: Home)                                   |
| `--force`, `-f`   | Overwrite existing files                                                  |

**Creates:**

- `praxis.yaml` — Governance configuration
- `CLAUDE.md` — AI assistant instructions
- `docs/capture.md` — First stage template

### praxis validate

Validate a praxis.yaml configuration:

```bash
praxis validate [PATH] [OPTIONS]
```

| Option           | Description                       |
| ---------------- | --------------------------------- |
| `PATH`           | Project directory (default: `.`)  |
| `--strict`, `-s` | Treat warnings as errors (exit 1) |

**Exit codes:** 0 = valid, 1 = errors found

### praxis stage

Transition project to a new lifecycle stage:

```bash
praxis stage <NEW_STAGE> [PATH]
```

| Argument    | Description                                                                               |
| ----------- | ----------------------------------------------------------------------------------------- |
| `NEW_STAGE` | Target stage (capture, sense, explore, shape, formalize, commit, execute, sustain, close) |
| `PATH`      | Project directory (default: `.`)                                                          |

**Example:**

```bash
praxis stage sense
# ✓ Stage updated to 'sense'
```

**Behavior:**

- Updates `praxis.yaml` with new stage
- Updates `CLAUDE.md` stage line (if present)
- Warns if missing required artifact (e.g., SOD at commit+)
- Prompts for confirmation on non-standard regressions

### praxis status

Show project status including stage, validation, and history:

```bash
praxis status [PATH]
```

| Argument | Description                      |
| -------- | -------------------------------- |
| `PATH`   | Project directory (default: `.`) |

**Example output:**

```
Project: my-project
  Domain:  code
  Stage:   execute (7/9)
  Privacy: personal
  Env:     Home

Next Stage: sustain
  - Complete initial implementation

Artifact: ✓ docs/sod.md

Validation: ✓ Valid

Stage History:
  2025-12-27 execute    abc1234 feat: implement core feature
  2025-12-27 commit     def5678 ready to build
```

### praxis audit

Check project against domain best practices:

```bash
praxis audit [PATH] [OPTIONS]
```

| Option           | Description                          |
| ---------------- | ------------------------------------ |
| `PATH`           | Project directory (default: `.`)     |
| `--json`         | Output in JSON format for automation |
| `--strict`, `-s` | Treat warnings as failures (exit 1)  |

See [Audit Command](#audit-command) for full details.

---

## Knowledge Distillation (PKDP)

Praxis includes the **Praxis Knowledge Distillation Pipeline (PKDP)**: a risk-tiered pipeline for turning raw inputs into validated knowledge artifacts.

PKDP is exposed via `praxis pipeline`.

```bash
# Initialize a pipeline (tier 0–3) using a corpus file or directory
praxis pipeline init --tier 2 --corpus path/to/corpus

# Run a specific stage, or all remaining required stages
praxis pipeline run --stage rtc
praxis pipeline run --all

# Check progress
praxis pipeline status

# Record the HVA decision
praxis pipeline accept --rationale "ready to ingest"
praxis pipeline reject --rationale "insufficient evidence"
praxis pipeline refine --to idas --rationale "need clearer questions"
```

See [PKDP Guide](pkdp.md) for stages, tiers, and artifacts.

---

## Walkthrough: Building a Hello World CLI

This example demonstrates building a minimal Python CLI using the full Praxis lifecycle.

### Step 1: Initialize the Project

Create a new directory and initialize with `praxis init`:

```bash
mkdir hello-world
cd hello-world
praxis init --domain code --privacy personal
```

This creates:

- `praxis.yaml` — Governance configuration
- `CLAUDE.md` — AI assistant instructions
- `docs/capture.md` — First stage template

Validate:

```bash
poetry run praxis validate .
# ✓ praxis.yaml is valid
```

### Step 2: Capture

Edit `docs/capture.md` (created by `praxis init`) with your raw inputs:

```markdown
# Capture

## Intent

Build a simple Python CLI that prints "Hello, World!"

## Constraints

- Python 3.10+
- Use Typer for CLI
- Single command with optional --name argument

## Initial Ideas

hello-world → "Hello, World!"
hello-world --name X → "Hello, X!"
```

### Step 3: Sense

Update `praxis.yaml`:

```yaml
stage: sense
```

Create `docs/sense.md` — synthesize the capture inputs:

```markdown
# Sense

## Key Insights

1. Simplicity is essential — Hello World is the right scope
2. The journey matters more than the destination
3. Validate at every stage transition
```

Validate:

```bash
poetry run praxis validate .
# ✓ praxis.yaml is valid
```

### Step 4: Explore

Update `praxis.yaml`:

```yaml
stage: explore
```

Create `docs/explore.md` — investigate options:

```markdown
# Explore

## Option A: Typer CLI

Simple, matches Praxis patterns.

## Option B: Click CLI

More explicit, but not consistent with existing code.

## Decision

Use Typer for consistency.
```

### Step 5: Shape

Update `praxis.yaml`:

```yaml
stage: shape
```

Create `docs/shape.md` — define the architecture:

```markdown
# Shape

## Structure

src/hello_world/
├── **init**.py
├── **main**.py
└── cli.py

## Decisions

- No layers needed (too simple)
- Single test file
- No BDD (unit tests sufficient)
```

### Step 6: Formalize (Critical)

Update `praxis.yaml`:

```yaml
stage: formalize
```

Create `docs/sod.md` — the **Solution Overview Document**:

```markdown
# Solution Overview Document (SOD)

## Purpose

Minimal CLI that prints a greeting.

## Scope

- Single command: hello-world
- Optional --name argument (default: "World")
- Output: "Hello, {name}!"

## Out of Scope

- Multiple commands
- Configuration files
- Logging

## Technical Design

- Typer CLI
- Poetry for packaging
- pytest for testing

## Acceptance Criteria

- [ ] hello-world prints "Hello, World!"
- [ ] hello-world --name X prints "Hello, X!"
- [ ] All tests pass
```

**Important:** The SOD locks scope. This is the "hard boundary" — no execution without formalization.

### Step 7: Commit

Update `praxis.yaml`:

```yaml
stage: commit
```

Validate — the validator now checks that `docs/sod.md` exists:

```bash
poetry run praxis validate .
# ✓ praxis.yaml is valid
```

If you try to reach Commit without an SOD:

```bash
# (without docs/sod.md)
poetry run praxis validate .
# ✗ [ERROR] Stage 'commit' requires formalization artifact at 'docs/sod.md', but file not found
```

### Step 8: Execute

Update `praxis.yaml`:

```yaml
stage: execute
```

Build the actual code:

**pyproject.toml:**

```toml
[tool.poetry]
name = "hello-world"
version = "1.0.0"
packages = [{include = "hello_world", from = "src"}]

[tool.poetry.dependencies]
python = ">=3.10"
typer = ">=0.9.0"

[tool.poetry.scripts]
hello-world = "hello_world.cli:app"
```

**src/hello_world/cli.py:**

```python
import typer

app = typer.Typer()

@app.command()
def hello(name: str = typer.Option("World", "--name", "-n")) -> None:
    typer.echo(f"Hello, {name}!")
```

**tests/test_cli.py:**

```python
from typer.testing import CliRunner
from hello_world.cli import app

def test_default_greeting():
    result = CliRunner().invoke(app, [])
    assert "Hello, World!" in result.output

def test_custom_greeting():
    result = CliRunner().invoke(app, ["--name", "Praxis"])
    assert "Hello, Praxis!" in result.output
```

Install and test:

```bash
poetry install
poetry run pytest
# 2 passed

poetry run hello-world
# Hello, World!

poetry run hello-world --name Praxis
# Hello, Praxis!
```

Validate:

```bash
poetry run praxis validate .
# ✓ praxis.yaml is valid
```

### Step 9: Sustain

Update `praxis.yaml`:

```yaml
stage: sustain
```

The project is now in maintenance mode. Future changes follow the Sustain rules:

- **Bug fixes** → Stay in Sustain
- **Small enhancements** → Stay in Sustain
- **Scope changes** → Regress to Formalize (update SOD)

---

## Validation Rules

The `praxis validate` CLI checks:

| Rule                         | Severity | When                  |
| ---------------------------- | -------- | --------------------- |
| Invalid domain/stage/privacy | Error    | Always                |
| Missing SOD (Code domain)    | Error    | stage ≥ commit        |
| Invalid stage regression     | Warning  | When moving backward  |
| Privacy downgrade            | Warning  | When less restrictive |

### Example: Missing Artifact

```bash
# praxis.yaml has stage: execute, but no docs/sod.md
poetry run praxis validate .
# ✗ [ERROR] Stage 'execute' requires formalization artifact at 'docs/sod.md', but file not found
```

### Example: Invalid Regression

If you change from `execute` to `explore` (skipping allowed targets):

```bash
poetry run praxis validate .
# ⚠ [WARNING] Regression from 'execute' to 'explore' is not in allowed regression table.
#   Allowed targets from execute: commit, formalize
```

---

## Environment Override

Override the environment without editing `praxis.yaml`:

```bash
PRAXIS_ENV=Work poetry run praxis validate .
```

Useful for CI pipelines or testing different contexts.

---

## Domain Artifacts

Each domain requires a specific formalization artifact:

| Domain  | Artifact       | Path            |
| ------- | -------------- | --------------- |
| Code    | SOD            | `docs/sod.md`   |
| Create  | Creative Brief | `docs/brief.md` |
| Write   | Writing Brief  | `docs/brief.md` |
| Learn   | Learning Plan  | `docs/plan.md`  |
| Observe | (none)         | —               |

---

## Audit Command

Check your project against domain best practices with `praxis audit`:

```bash
poetry run praxis audit path/to/project/
```

### Example Output

```
Auditing: my-project (domain: code)

Tooling:
  ✓ Poetry configured (pyproject.toml exists)
  ✓ Typer CLI (typer in dependencies)
  ✓ ruff linter (in dev dependencies)
  ✓ mypy type checker (in dev dependencies)

Structure:
  ✓ Hexagonal architecture (domain/, application/, infrastructure/)
  ✓ Console script entry point configured
  ✓ __main__.py exists (python -m support)

Testing:
  ✓ BDD tests (tests/features/*.feature exists)
  ✓ pytest-bdd in dependencies

Summary: 9 passed, 0 warning(s), 0 failed
```

### Options

| Flag       | Description                              |
| ---------- | ---------------------------------------- |
| `--json`   | Output in JSON format for automation     |
| `--strict` | Treat warnings as failures (exit code 1) |

### Checks by Domain

**Code Domain** (from `docs/opinions/code/cli-python.md`):

| Category  | Check          | Description                                 |
| --------- | -------------- | ------------------------------------------- |
| Tooling   | Poetry         | pyproject.toml exists                       |
| Tooling   | Typer          | typer in dependencies                       |
| Tooling   | ruff           | ruff in dev dependencies                    |
| Tooling   | mypy           | mypy in dev dependencies                    |
| Structure | Hexagonal      | domain/, application/, infrastructure/ dirs |
| Structure | Console script | [tool.poetry.scripts] configured            |
| Structure | **main**.py    | python -m support                           |
| Testing   | BDD tests      | tests/features/\*.feature exists            |
| Testing   | pytest-bdd     | pytest-bdd in dev dependencies              |

---

## Best Practices

1. **Validate at every stage transition** — Catch governance issues early

2. **Write the SOD before coding** — The SOD forces you to think before building

3. **Keep stage docs lightweight** — Not every stage needs a full document

4. **Use Sustain properly** — Bug fixes stay in Sustain; scope changes regress to Formalize

5. **Trust the process** — The stages feel slow at first but prevent expensive rework

---

## Worked Example

For a complete worked example with all stage documents, install the `uat-praxis-code` example:

```bash
praxis examples add uat-praxis-code
```

This will clone the example to `$PRAXIS_HOME/examples/uat-praxis-code/`.
