# CLI Automation Contracts

## Overview

This document specifies the JSON output schemas and exit codes for Praxis CLI commands that support automation via the `--json` and `--quiet` flags.

**Contract stability**: These schemas follow semantic versioning. Fields will not be removed or renamed without a major version bump.

## Exit Codes

All Praxis commands use the following exit code semantics:

| Exit Code | Meaning | When Used |
|-----------|---------|-----------|
| `0` | Success | Command completed successfully |
| `1` | Validation/Command Failure | Config invalid, command failed, or tool checks failed |
| `2` | Missing Required Arguments | Required flags not provided in automation mode |
| `3` | Workspace Not Found | PRAXIS_HOME not set when required |
| `4` | Extension/Example Operation Failed | Extension or example add/remove/update failed |

### Exit Code Usage by Command

| Command | Success (0) | Failure (1) | Missing Args (2) | No Workspace (3) | Extension Fail (4) |
|---------|-------------|-------------|------------------|------------------|--------------------|
| `init` | ✓ | ✓ | — | — | — |
| `new` | ✓ | ✓ | ✓ | ✓ | — |
| `validate` | ✓ | ✓ | — | — | — |
| `status` | ✓ | ✓ | — | — | — |
| `context` | ✓ | ✓ | — | — | — |
| `audit` | ✓ | ✓ | — | — | — |
| `stage` | ✓ | ✓ | — | — | — |
| `opinions` | ✓ | ✓ | — | — | — |
| `workspace info` | ✓ | ✓ | — | ✓ | — |
| `workspace init` | ✓ | ✓ | — | ✓ | — |
| `extensions add` | ✓ | — | ✓ | ✓ | ✓ |
| `extensions remove` | ✓ | — | — | ✓ | ✓ |
| `extensions update` | ✓ | — | — | ✓ | ✓ |
| `pipeline status` | ✓ | ✓ | — | — | — |
| `pipeline init` | ✓ | ✓ | — | — | — |
| `templates render` | ✓ | ✓ | — | — | — |

## JSON Output Schemas

### `praxis status --json`

**Purpose**: Get project status, stage progress, and next steps.

**Exit codes**: 
- `0` - Config loaded successfully
- `1` - Config load failed

**Schema** (version 1.0):

```json
{
  "project_name": "string",
  "config": {
    "domain": "code|create|write|observe|learn",
    "subtype": "string|null",
    "stage": "capture|sense|explore|shape|formalize|commit|execute|sustain|close",
    "privacy_level": "public|public-trusted|personal|confidential|restricted",
    "environment": "Home|Work",
    "coverage_threshold": "number|null",
    "history": []
  },
  "stage_index": "number",
  "stage_count": "number",
  "next_stage": "string|null",
  "next_stage_requirements": ["string"],
  "artifact_path": "string|null",
  "artifact_exists": "boolean",
  "checklist_path": "string|null",
  "checklist_addendum_path": "string|null",
  "validation": {
    "valid": "boolean",
    "config": { /* same as top-level config */ },
    "issues": [
      {
        "severity": "error|warning",
        "message": "string",
        "field": "string|null"
      }
    ]
  },
  "next_steps": [
    {
      "action": "create|edit|run|review|fix",
      "priority": "number",
      "description": "string",
      "target": "string|null",
      "reason": "string",
      "command": "string|null"
    }
  ],
  "stage_history": [
    {
      "from_stage": "string",
      "to_stage": "string",
      "timestamp": "ISO 8601 string",
      "contract_id": "string|null",
      "reason": "string|null"
    }
  ],
  "errors": ["string"]
}
```

**Example**:
```bash
praxis status --json
```

---

### `praxis validate --json`

**Purpose**: Validate project configuration and optionally run tool checks.

**Exit codes**:
- `0` - Valid config, all checks pass
- `1` - Invalid config OR tool checks failed

**Schema** (version 1.0):

```json
{
  "valid": "boolean",
  "config": {
    "domain": "code|create|write|observe|learn",
    "subtype": "string|null",
    "stage": "capture|sense|explore|shape|formalize|commit|execute|sustain|close",
    "privacy_level": "public|public-trusted|personal|confidential|restricted",
    "environment": "Home|Work",
    "coverage_threshold": "number|null",
    "history": []
  },
  "issues": [
    {
      "severity": "error|warning",
      "message": "string",
      "field": "string|null"
    }
  ],
  "version": "1.0",
  "tool_checks": [
    {
      "tool": "pytest|ruff|mypy",
      "success": "boolean",
      "output": "string|null",
      "error": "string|null"
    }
  ],
  "coverage_check": {
    "success": "boolean",
    "coverage_percent": "number|null",
    "threshold": "number",
    "error": "string|null"
  }
}
```

**Example**:
```bash
praxis validate --json
praxis validate --json --check-all
praxis validate --json --strict  # Warnings become errors
```

---

### `praxis audit --json`

**Purpose**: Check project against domain-specific best practices.

**Exit codes**:
- `0` - All checks passed (or only warnings without `--strict`)
- `1` - One or more checks failed (or warnings with `--strict`)

**Schema**:

```json
{
  "project_name": "string",
  "domain": "code|create|write|observe|learn",
  "checks": [
    {
      "name": "string",
      "category": "tooling|structure|practices",
      "status": "passed|warning|failed",
      "message": "string"
    }
  ]
}
```

**Note**: Filter checks by status using `jq` or similar tools:
```bash
# Get only failed checks
praxis audit --json | jq '.checks[] | select(.status == "failed")'

# Count warnings
praxis audit --json | jq '[.checks[] | select(.status == "warning")] | length'
```

**Example**:
```bash
praxis audit --json
praxis audit --json --strict  # Warnings become failures
```

---

### `praxis context --json`

**Purpose**: Generate AI context bundle with project config and resolved opinions.

**Exit codes**:
- `0` - Context generated successfully
- `1` - Error loading config or opinions

**Schema** (version 1.0):

```json
{
  "schema_version": "1.0",
  "project_name": "string",
  "domain": "code|create|write|observe|learn",
  "stage": "capture|sense|explore|shape|formalize|commit|execute|sustain|close",
  "privacy_level": "public|public-trusted|personal|confidential|restricted",
  "environment": "Home|Work",
  "subtype": "string|null",
  "opinions": ["relative/path/to/opinion.md"],
  "formalize_artifact": {
    "path": "string|null",
    "excerpt": "string|null"
  },
  "errors": ["string"]
}
```

**Example**:
```bash
praxis context --json
```

---

### `praxis opinions --json`

**Purpose**: List resolved opinion files for current domain/stage/subtype.

**Exit codes**:
- `0` - Opinions resolved successfully
- `1` - Error loading config or resolving opinions

**Schema**:

```json
{
  "domain": "code|create|write|observe|learn",
  "stage": "string|null",
  "subtype": "string|null",
  "files": [
    {
      "path": "string",
      "exists": "boolean",
      "status": "active|draft|deprecated",
      "version": "string",
      "parse_error": "string|null"
    }
  ],
  "warnings": ["string"]
}
```

**Example**:
```bash
praxis opinions --json
praxis opinions --domain code --stage capture --json
```

---

## Automation Flags

### `--json`

Output machine-readable JSON instead of human-readable text.

**Characteristics**:
- Always outputs valid JSON (even on errors)
- Disables interactive prompts
- Writes to stdout (errors may still go to stderr)
- Schema version included where applicable

**Example**:
```bash
praxis validate --json > validation-result.json
if [ $? -eq 0 ]; then
  echo "Validation passed"
fi
```

### `--quiet` / `-q`

Suppress all non-error output.

**Characteristics**:
- Exit code still indicates success/failure
- Errors still written to stderr
- Disables interactive prompts
- Useful for scripting where only exit code matters

**Example**:
```bash
praxis validate --quiet
if [ $? -eq 0 ]; then
  echo "Valid"
else
  echo "Invalid"
fi
```

## Commands Supporting Automation

| Command | `--json` | `--quiet` | Notes |
|---------|----------|-----------|-------|
| `init` | ✓ | ✓ | Requires `--domain` and `--privacy` with automation flags |
| `new` | ✓ | ✓ | Requires `--domain` and `--privacy` with automation flags |
| `validate` | ✓ | ✓ | Use `--strict` to fail on warnings |
| `status` | ✓ | ✓ | — |
| `context` | ✓ | ✓ | — |
| `audit` | ✓ | ✓ | Use `--strict` to fail on warnings |
| `stage` | ✓ | ✓ | — |
| `opinions` | ✓ | — | Use `--prompt` for AI-ready format |
| `workspace info` | ✓ | ✓ | Requires PRAXIS_HOME |
| `workspace init` | ✓ | ✓ | — |
| `extensions list` | ✓ | — | — |
| `extensions add` | ✓ | — | — |
| `extensions remove` | ✓ | — | — |
| `extensions update` | ✓ | — | — |
| `examples list` | ✓ | — | — |
| `examples add` | ✓ | — | — |
| `pipeline status` | ✓ | ✓ | — |
| `pipeline init` | ✓ | — | — |
| `pipeline run` | ✓ | — | — |
| `pipeline accept` | ✓ | — | — |
| `pipeline reject` | ✓ | — | — |
| `pipeline refine` | ✓ | — | — |
| `templates render` | ✓ | ✓ | — |

## CI/CD Usage Examples

### GitHub Actions

```yaml
- name: Validate Praxis config
  run: |
    praxis validate --json --check-all > validation.json
    echo "exit_code=$?" >> $GITHUB_ENV

- name: Check validation
  if: env.exit_code != '0'
  run: |
    cat validation.json | jq .
    exit 1
```

### GitLab CI

```yaml
validate:
  script:
    - praxis validate --quiet --check-all
  allow_failure: false
```

### Shell Script

```bash
#!/bin/bash
set -e

# Validate in quiet mode
if ! praxis validate --quiet --check-all; then
  echo "Validation failed"
  exit 1
fi

# Get status as JSON
STATUS=$(praxis status --json)
STAGE=$(echo "$STATUS" | jq -r '.config.stage')

if [ "$STAGE" != "execute" ]; then
  echo "Not ready for deployment (stage=$STAGE)"
  exit 1
fi

echo "Ready for deployment"
```

## Schema Versioning

JSON output schemas include a version field where applicable:
- `validate`: `"version": "1.0"`
- `context`: `"schema_version": "1.0"`

**Breaking changes** (field removal/rename) will increment the version number. **Non-breaking changes** (new fields) will not.

Monitor the version field in your automation to detect schema changes.

## Error Handling

When using `--json`, errors are included in the JSON output:

```json
{
  "success": false,
  "errors": ["Error message 1", "Error message 2"]
}
```

When using `--quiet`, errors are written to stderr only:

```bash
praxis validate --quiet 2> errors.log
if [ $? -ne 0 ]; then
  cat errors.log
fi
```
