# CLI Reference

This page documents all Praxis CLI commands.

!!! note "Auto-generation Coming"
    This page will be auto-generated from the Typer CLI in a future update. For now, use `praxis --help` for the most current information.

---

## Core Commands

### `praxis new`

Create a new Praxis project.

```bash
praxis new PROJECT_NAME --domain DOMAIN --privacy PRIVACY [--environment ENV]
```

**Arguments:**

- `PROJECT_NAME` — Name of the project (required)

**Options:**

- `--domain` — Project domain: `code`, `create`, `write`, `learn`, `observe` (required)
- `--privacy` — Privacy level: `public`, `public-trusted`, `personal`, `confidential`, `restricted` (required)
- `--environment` — Environment context: `Home`, `Work` (default: `Home`)

**Example:**

```bash
praxis new my-cli-tool --domain code --privacy personal
```

---

### `praxis init`

Initialize a Praxis project in an existing directory.

```bash
praxis init --domain DOMAIN [--privacy PRIVACY] [--environment ENV]
```

**Options:**

- `--domain` — Project domain (required)
- `--privacy` — Privacy level (default: `personal`)
- `--environment` — Environment context (default: `Home`)

**Example:**

```bash
cd existing-project
praxis init --domain code --privacy personal
```

---

### `praxis status`

Display current project status, stage, and next steps.

```bash
praxis status [--json]
```

**Options:**

- `--json` — Output in JSON format

**Example:**

```bash
praxis status
# Output:
# Domain: code
# Stage: formalize
# Privacy: personal
# Environment: Home
#
# Next Steps:
#   + Create docs/sod.md (Solution Overview Document)
#   ▶ Run `praxis stage commit` (Advance to Commit stage)
```

---

### `praxis stage`

Transition to a new lifecycle stage.

```bash
praxis stage STAGE [--reason REASON]
```

**Arguments:**

- `STAGE` — Target stage: `capture`, `sense`, `explore`, `shape`, `formalize`, `commit`, `execute`, `sustain`, `close`

**Options:**

- `--reason` — Rationale for non-standard regression (required for backward transitions)

**Example:**

```bash
praxis stage formalize
praxis stage explore --reason "Scope change discovered during implementation"
```

---

### `praxis validate`

Validate project governance configuration.

```bash
praxis validate [--strict] [--check-all]
```

**Options:**

- `--strict` — Fail on warnings
- `--check-all` — Run tests, linting, and type checking

**Example:**

```bash
praxis validate --strict
```

---

### `praxis audit`

Check domain-specific best practices.

```bash
praxis audit [--strict]
```

**Options:**

- `--strict` — Fail on warnings

**Example:**

```bash
praxis audit --strict
```

---

## Workspace Commands

### `praxis workspace init`

Initialize a Praxis workspace.

```bash
praxis workspace init
```

Creates workspace structure at `$PRAXIS_HOME`:
- `extensions/` — Installed extensions
- `examples/` — Example projects
- `projects/` — User projects
- `workspace-config.yaml` — Workspace configuration

---

### `praxis workspace info`

Display workspace information.

```bash
praxis workspace info
```

---

## Extension Commands

### `praxis extensions list`

List available extensions.

```bash
praxis extensions list [--installed]
```

**Options:**

- `--installed` — Show only installed extensions

---

### `praxis extensions add`

Install an extension.

```bash
praxis extensions add EXTENSION_NAME
```

**Example:**

```bash
praxis extensions add template-python-cli
```

---

### `praxis extensions remove`

Uninstall an extension.

```bash
praxis extensions remove EXTENSION_NAME
```

---

### `praxis extensions update`

Update an installed extension.

```bash
praxis extensions update EXTENSION_NAME
```

---

## Example Commands

### `praxis examples list`

List available example projects.

```bash
praxis examples list
```

---

### `praxis examples add`

Install an example project.

```bash
praxis examples add EXAMPLE_NAME
```

**Example:**

```bash
praxis examples add uat-praxis-code
```

---

## Opinion Commands

### `praxis opinions`

Show applicable opinions for the current project.

```bash
praxis opinions [--prompt]
```

**Options:**

- `--prompt` — Generate AI-ready context

**Example:**

```bash
praxis opinions --prompt > ai-context.txt
```

---

## Template Commands

### `praxis templates render`

Generate stage documentation from templates.

```bash
praxis templates render [--stage STAGE] [--force]
```

**Options:**

- `--stage` — Specific stage to render (default: current stage)
- `--force` — Overwrite existing files

**Example:**

```bash
praxis templates render --stage formalize
```

---

## Pipeline Commands

### `praxis pipeline init`

Initialize a knowledge distillation pipeline.

```bash
praxis pipeline init --tier TIER
```

**Arguments:**

- `--tier` — Risk tier: `0`, `1`, `2`, `3`

**Example:**

```bash
praxis pipeline init --tier 2
```

---

### `praxis pipeline status`

Show pipeline status.

```bash
praxis pipeline status
```

---

### `praxis pipeline run`

Execute the next pipeline stage.

```bash
praxis pipeline run
```

---

### `praxis pipeline accept`

Accept pipeline output (HVA gate).

```bash
praxis pipeline accept
```

---

### `praxis pipeline reject`

Reject pipeline output and provide feedback.

```bash
praxis pipeline reject --feedback "Rationale for rejection"
```

---

### `praxis pipeline refine`

Refine pipeline output.

```bash
praxis pipeline refine --refinement "Specific improvements needed"
```

---

## Context Commands

### `praxis context`

Generate AI context bundle for the current project.

```bash
praxis context [--json]
```

**Options:**

- `--json` — Output in JSON format

**Example:**

```bash
praxis context --json > ai-context.json
```

---

## Global Options

All commands support:

- `--help` — Show help for the command
- `--version` — Show Praxis version

---

## Exit Codes

- `0` — Success
- `1` — Validation error
- `2` — Missing artifact
- `3` — Invalid stage transition
- `4` — Configuration error

---

## Environment Variables

- `PRAXIS_HOME` — Workspace root directory (default: `~/praxis-workspace`)
- `PRAXIS_ENV` — Override environment setting (`Home` or `Work`)

---

## See Also

- [User Guide](../guides/user-guide.md) — Step-by-step walkthrough
- [Philosophy](../core/spec/sod.md) — Core concepts and governance
- [Contributing](../CONTRIBUTING.md) — Development guidelines
