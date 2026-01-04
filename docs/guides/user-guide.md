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

### praxis new

Create a new project directory and initialize governance files:

```bash
praxis new <NAME> [OPTIONS]
```

| Option            | Description                                                               |
| ----------------- | ------------------------------------------------------------------------- |
| `NAME`            | Project name (directory will be created under the chosen location)        |
| `--domain`, `-d`  | Project domain: code, create, write, observe, learn                       |
| `--subtype`       | Optional subtype (e.g., cli, api, library)                                |
| `--privacy`, `-p` | Privacy level: public, public-trusted, personal, confidential, restricted |
| `--env`, `-e`     | Environment: Home, Work                                                   |
| `--path`          | Parent directory where the project directory will be created              |
| `--force`, `-f`   | Overwrite existing managed files                                          |
| `--json`          | Output JSON format (no prompts)                                           |
| `--quiet`, `-q`   | Suppress non-error output (no prompts)                                    |

**Defaults:**

- If `PRAXIS_HOME` is set and a `workspace-config.yaml` is present, projects default under `$PRAXIS_HOME/<projects_path>/<domain>/`.
- If `PRAXIS_HOME` is set but no workspace config is available, projects default under `$PRAXIS_HOME/projects/<domain>/`.
- Otherwise, the current directory is used (interactive mode).

**Exit codes:**

- `0` success
- `1` error
- `3` workspace context required (e.g., `--json/--quiet` without `PRAXIS_HOME` and without `--path`)

**Creates:**

- `praxis.yaml` — Governance configuration
- `CLAUDE.md` — AI assistant instructions
- `docs/capture.md` — First stage template

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

| Option              | Description                                          |
| ------------------- | ---------------------------------------------------- |
| `PATH`              | Project directory (default: `.`)                     |
| `--strict`, `-s`    | Treat warnings as errors (exit 1)                    |
| `--check-tests`     | Run pytest and fail if tests fail                    |
| `--check-lint`      | Run ruff and fail if lint errors exist               |
| `--check-types`     | Run mypy and fail if type errors exist               |
| `--check-all`       | Run all checks (tests, lint, types, coverage)        |
| `--check-coverage`  | Run coverage check (requires coverage_threshold)     |
| `--json`            | Output JSON format (includes version field)          |
| `--quiet`, `-q`     | Suppress non-error output                            |

**Exit codes:**

- `0` — Validation passed (all checks successful)
- `1` — Validation failed (errors found or tool checks failed)
- `2` — Usage error (invalid arguments)

**Validation checks:**

1. **Schema validation** — Ensures praxis.yaml has valid domain, stage, privacy_level
2. **Artifact existence** — Checks required formalization artifacts for stage ≥ formalize:
   - Code: `docs/sod.md`
   - Create: `docs/brief.md`
   - Write: `docs/brief.md`
   - Learn: `docs/plan.md`
   - Observe: (no artifact required)
3. **Regression detection** — Warns on invalid stage regressions (vs previous commit)
4. **Privacy downgrade** — Warns if privacy_level decreased from previous commit

**JSON output:**

When `--json` is specified, output includes a version field for schema stability:

```json
{
  "version": "1.0",
  "valid": true,
  "config": { ... },
  "issues": [],
  "tool_checks": []
}
```

**Examples:**

```bash
# Basic validation
praxis validate .

# Strict mode (warnings = errors)
praxis validate --strict

# Run all checks (tests, lint, types, coverage if configured)
praxis validate --check-all

# JSON output for CI/automation
praxis validate --json
```

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
- Warns if missing required artifact (e.g., SOD at formalize+)
- Prompts for confirmation on non-standard regressions

### praxis status

Show project status including stage, validation, next steps, and history:

```bash
praxis status [PATH] [OPTIONS]
```

| Argument | Description                      |
| -------- | -------------------------------- |
| `PATH`   | Project directory (default: `.`) |

| Option           | Description                          |
| ---------------- | ------------------------------------ |
| `--json`         | Output in JSON format for automation |
| `--quiet`, `-q`  | Suppress non-error output            |

**Example output:**

```
Project: my-project
  Domain:  code
  Stage:   formalize (5/9)
  Privacy: personal
  Env:     Home

Next Stage: commit
  - Create docs/sod.md
  - Verify readiness to build

Artifact: ✗ docs/sod.md

Checklist: core/checklists/formalize.md
           core/checklists/formalize-code.md

Validation: ✗ Invalid (1 error(s))
  ✗ Stage 'formalize' requires formalization artifact at 'docs/sod.md', but file not found. See checklist: core/checklists/formalize.md

Next Steps:
  ! Fix praxis.yaml (Stage 'formalize' requires formalization artifact)
  + Create docs/sod.md (Solution Overview Document)
  ? Review docs/sod.md (Review SOD completeness)

Legend: + create  ~ edit  ▶ run  ? review  ! fix

Stage History:
  2025-12-27 formalize abc1234 move to formalize stage
```

**Lifecycle Checklists:**

Each lifecycle stage has a canonical checklist at `core/checklists/{stage}.md` that defines:
- **Entry Criteria:** What must be true before entering this stage
- **Exit Criteria:** What must be complete to advance to the next stage
- **Guidance:** Stage-specific responsibilities and best practices
- **References:** Links to relevant specs and documentation

Domain-specific addenda (e.g., `formalize-code.md`, `sustain-code.md`) provide additional context for specific domains. Use `praxis status` to see applicable checklists for your current stage.

**Available Checklists:**
- `capture.md` — Collect raw inputs with minimal friction
- `sense.md` — Convert inputs into understanding
- `explore.md` — Generate possibilities without obligation
- `shape.md` — Converge toward a viable direction
- `formalize.md` — Convert shaped thinking into durable artifacts
- `commit.md` — Explicitly decide to proceed
- `execute.md` — Produce the artifact
- `sustain.md` — Maintain and govern delivered work
- `close.md` — End work intentionally and capture leverage

**Domain Addenda:**
- `formalize-code.md` — Code-specific formalization guidance (SOD creation)
- `sustain-code.md` — Code-specific sustainment guidance (maintenance, monitoring)

**Next Steps Legend:**

| Icon | Action | Description |
|------|--------|-------------|
| `+`  | create | Generate new artifact |
| `~`  | edit   | Modify existing content |
| `▶`  | run    | Execute CLI command |
| `?`  | review | Human inspection required |
| `!`  | fix    | Address blocking error |

**JSON output:**

When `--json` is specified, output includes `next_steps` array:

```json
{
  "project_name": "my-project",
  "config": { ... },
  "next_steps": [
    {
      "action": "create",
      "priority": 1,
      "description": "Solution Overview Document",
      "target": "docs/sod.md",
      "reason": "Lock intent, scope, constraints, and success criteria"
    }
  ],
  ...
}
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

## Project Subtypes

Subtypes provide domain-specific guidance for different project shapes. When you specify a subtype, Praxis provides:

- **Subtype-specific templates** — Tailored stage documents for your project type
- **Subtype-specific opinions** — Best practices and quality gates for your subtype
- **Subtype-specific audit checks** — Validation rules specific to your project shape

### Available Subtypes by Domain

| Domain | Subtypes |
|--------|----------|
| **code** | cli, library, api, webapp, infrastructure, script |
| **create** | visual, audio, video, interactive, generative, design |
| **write** | technical, business, narrative, academic, journalistic |
| **learn** | skill, concept, practice, course, exploration |
| **observe** | notes, bookmarks, clips, logs, captures |

### Using Subtypes

Specify a subtype when creating a new project:

```bash
praxis new my-cli --domain code --subtype cli
```

Or add a subtype to an existing praxis.yaml:

```yaml
domain: code
subtype: cli
stage: capture
privacy_level: personal
environment: Home
```

### Nested Subtypes

Subtypes can be nested to provide more specific guidance. Use hyphens or dots to separate levels:

```bash
# Python CLI with all CLI + Python-specific guidance
praxis new my-cli --domain code --subtype cli-python
```

Nested subtypes inherit from their parent:
- `cli-python` inherits all `cli` opinions and adds Python-specific ones
- Templates resolve most-specific-first: `cli/python/` → `cli/` → domain default

### CLI Subtype (code.cli)

The CLI subtype provides guidance for building production-quality command-line tools:

**Templates:** CLI-specific stage documents that guide you through:
- Command design (flags, subcommands, exit codes)
- Pipeline safety (stdout/stderr conventions)
- Help and version flags
- Testing strategies

**Opinions:** Advisory guidance following Unix philosophy:
- Do one thing well
- Composability in pipelines
- Predictable behavior
- Backwards compatibility

**Audit Checks:**
| Check | Description |
|-------|-------------|
| `cli_entry_point_exists` | Console script in pyproject.toml or `__main__.py` |
| `cli_help_present` | `--help` flag support detected (Typer, argparse, click) |
| `cli_version_flag` | `--version` flag support detected |

### Viewing Subtype Opinions

Use the opinions command to see applicable guidance for your subtype:

```bash
praxis opinions --domain code --stage capture --subtype cli
```

Output:
```
Applicable opinions for code × capture (cli):

  1. _shared/first-principles.md [active]
  2. code/README.md [draft]
  3. code/principles.md [draft]
  4. code/capture.md [draft]
  5. code/subtypes/cli/README.md [active]
  6. code/subtypes/cli/principles.md [active]

Total: 6 files
```

### Subtype Validation

Invalid subtypes are rejected at project creation:

```bash
praxis new my-project --domain code --subtype visual
# ✗ Invalid subtype 'visual' for domain 'code'. Valid subtypes: cli, library, api, webapp, infrastructure, script
```

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

Use Given-When-Then format for testable criteria (see [testing.md](../../opinions/code/testing.md)):

​```gherkin
Feature: Hello World CLI

  Scenario: Default greeting
    Given the CLI is installed
    When the user runs hello-world with no arguments
    Then the output should be "Hello, World!"

  Scenario: Custom greeting
    Given the CLI is installed
    When the user runs hello-world --name "Praxis"
    Then the output should be "Hello, Praxis!"

  Scenario: Invalid argument
    Given the CLI is installed
    When the user runs hello-world with an unknown flag
    Then an error message should be displayed
​```
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

Each domain requires a specific formalization artifact. All templates implement the **Formalize Spine** (see [lifecycle.md](../../core/spec/lifecycle.md)):

1. **Intent & Outcome** — Problem/thesis, audience, success criteria, why now
2. **Scope & Boundaries** — In scope, out of scope, assumptions, dependencies
3. **Constraints** — Domain constraints, environment, privacy, tooling limits
4. **Execution Framing** — First increment, risks & mitigations, open questions
5. **Commit Criteria** — Unambiguous success definition

| Domain  | Artifact       | Path            |
| ------- | -------------- | --------------- |
| Code    | SOD            | `docs/sod.md`   |
| Create  | Creative Brief | `docs/brief.md` |
| Write   | Writing Brief  | `docs/brief.md` |
| Learn   | Learning Plan  | `docs/plan.md`  |
| Observe | (none)         | —               |

Each template includes inline comments with "what good looks like" examples to guide authors.

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

Audit checks support stage-aware and subtype-aware filtering:
- **min_stage**: Check only applies at this stage or later (skipped otherwise)
- **subtypes**: Check only applies to listed subtypes (skipped for other subtypes)

**Code Domain**:

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

**Create Domain**:

| Category     | Check             | Stage      | Subtypes          | Description                          |
| ------------ | ----------------- | ---------- | ----------------- | ------------------------------------ |
| Artifact     | brief_present     | formalize+ | all               | docs/brief.md exists                 |
| Organization | assets_organized  | any        | all               | assets/ directory exists             |
| Workflow     | prompts_documented| any        | generative        | prompts/ or docs/prompts.md exists   |
| Workflow     | references_present| any        | visual, design    | references/ or inspiration/ exists   |

**Write Domain**:

| Category     | Check           | Stage      | Subtypes              | Description                          |
| ------------ | --------------- | ---------- | --------------------- | ------------------------------------ |
| Artifact     | brief_present   | formalize+ | all                   | docs/brief.md exists                 |
| Workflow     | outline_present | shape+     | all                   | docs/outline.md or outline.md exists |
| Organization | drafts_organized| any        | all                   | drafts/ directory exists             |
| Workflow     | citations_present| any       | academic, journalistic| citations/bibliography file exists   |

**Learn Domain**:

| Category     | Check               | Stage      | Subtypes           | Description                               |
| ------------ | ------------------- | ---------- | ------------------ | ----------------------------------------- |
| Artifact     | plan_present        | formalize+ | all                | docs/plan.md exists                       |
| Workflow     | resources_documented| any        | all                | docs/resources.md or reading-list.md      |
| Workflow     | practice_log_present| any        | skill, practice    | docs/practice-log.md or practice/         |
| Workflow     | progress_tracked    | any        | course, exploration| docs/progress.md or log.md exists         |

**Observe Domain**:

| Category     | Check             | Stage | Subtypes | Description                          |
| ------------ | ----------------- | ----- | -------- | ------------------------------------ |
| Organization | captures_organized| any   | all      | captures/ or inbox/ directory exists |
| Organization | index_present     | any   | all      | index.md or catalog.md exists        |

### Domain-Specific Examples

**Create domain (generative subtype)**:
```bash
$ praxis audit my-generative-art-project
Auditing: my-generative-art-project (domain: create)

Artifact:
  ⚠ Brief not found. Create docs/brief.md to formalize your creative vision.

Organization:
  ⚠ Assets not organized. Create an assets/ directory for your creative outputs.

Workflow:
  ⚠ Prompts not documented. Create prompts/ directory or docs/prompts.md...

Summary: 0 passed, 3 warning(s), 0 failed
```

**Write domain (at capture stage)**:
```bash
$ praxis audit my-writing-project
Auditing: my-writing-project (domain: write)

Organization:
  ⚠ Drafts not organized. Create a drafts/ directory for your work-in-progress.

Summary: 0 passed, 1 warning(s), 0 failed
```

Note: At capture stage, `brief_present` (min_stage: formalize) and `outline_present` (min_stage: shape) are skipped.

**Learn domain (skill subtype)**:
```bash
$ praxis audit my-skill-project
Auditing: my-skill-project (domain: learn)

Workflow:
  ⚠ Resources not documented. Create docs/resources.md or reading-list.md...
  ⚠ Practice log not found. Create docs/practice-log.md or practice/...

Summary: 0 passed, 2 warning(s), 0 failed
```

Note: `progress_tracked` is skipped because it only applies to "course" or "exploration" subtypes.

---

## Best Practices

1. **Validate at every stage transition** — Catch governance issues early

2. **Write the SOD before coding** — The SOD forces you to think before building

3. **Use BDD acceptance criteria** — Write Given-When-Then scenarios in your SOD; they become your test specifications (see [testing.md](../../opinions/code/testing.md))

4. **Write tests before implementation** — Tests provide explicit targets for AI code generation and catch regressions early

5. **Keep stage docs lightweight** — Not every stage needs a full document

6. **Use Sustain properly** — Bug fixes stay in Sustain; scope changes regress to Formalize

7. **Trust the process** — The stages feel slow at first but prevent expensive rework

---

## Worked Example

For a complete worked example with all stage documents, install the `uat-praxis-code` example:

```bash
praxis examples add uat-praxis-code
```

This will clone the example to `$PRAXIS_HOME/examples/uat-praxis-code/`.
