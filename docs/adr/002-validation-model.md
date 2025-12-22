# ADR-002: Validation Model

**Status:** Draft — Pending validation via worked example
**Date:** 2025-12-21
**Deciders:** TBD
**Relates to:** ADR-001 (Policy Engine Selection), Issue #4 (template-python-cli)

---

## Context

Before selecting a policy engine (ADR-001), we must define what the engine validates. This ADR establishes the validation model that any policy engine must support.

**Approach:** Rather than design in a vacuum, we're discovering the validation model by working through Issue #4 (template-python-cli). The positions below are initial hypotheses to be tested and refined during that worked example.

---

## Decisions (Draft — Subject to Revision)

### 1. Configuration Scope

**Position: One `praxis.yaml` per project, at repository root.**

Rationale:
- Matches common conventions (package.json, pyproject.toml, Cargo.toml)
- Single source of truth for project governance
- Simplifies tooling (always look in one place)

```yaml
# praxis.yaml (project root)
domain: build
stage: formalize
privacy_level: personal
environment: Home
```

**Alternative rejected:** Per-directory configs. Adds complexity without clear benefit for solo/small-team use.

---

### 2. Validation Depth

**Position: Option B — Config validation + filesystem checks for required artifacts.**

The validator will:
1. Validate `praxis.yaml` schema and field values
2. Check that required artifacts exist (by path convention)
3. NOT deeply inspect artifact contents

Example behavior:
- `stage: execute` + `domain: build` → validator checks `docs/sod.md` exists
- Validator does NOT parse SOD to verify it has all required sections

Rationale:
- Catches the most common failure mode (missing formalization)
- Avoids complexity of content parsing
- Content quality is author responsibility, not policy engine scope

**Artifact path conventions:**

| Domain | Formalize Artifact | Expected Path |
|--------|-------------------|---------------|
| Build | SOD | `docs/sod.md` |
| Create | Creative Brief | `docs/brief.md` |
| Write | Writing Brief | `docs/brief.md` |
| Learn | Learning Plan | `docs/plan.md` |
| Observe | (none) | — |

---

### 3. Stage Tracking

**Position: Explicit declaration in `praxis.yaml`, updated manually by author.**

The `stage` field is the single source of truth. The author updates it when transitioning stages.

Rationale:
- Simple and transparent
- No hidden state or event logs
- Git history provides audit trail naturally
- Aligns with "author is accountable" philosophy

**Rejected alternatives:**
- Inferred from artifacts: Too magical, hard to debug
- Event-based transitions: Over-engineered for solo use

---

### 4. Regression Enforcement

**Position: Advisory warnings, not blocking errors.**

Invalid regressions (per lifecycle.md table) produce warnings, not failures.

Rationale:
- Real work is messy; hard blocks cause friction
- Author should be informed, not prevented
- Trust the author to make intentional decisions
- Can tighten to errors later if abuse patterns emerge

Example output:
```
⚠ Warning: Regression from Execute → Explore is not in allowed regression table.
  Allowed targets from Execute: Commit, Formalize
  Proceeding anyway (author override).
```

---

### 5. Transition History

**Position: No explicit history tracking. Git is the audit log.**

The validator only sees current state. Historical transitions are visible via `git log` on `praxis.yaml`.

Rationale:
- Avoids duplicate state management
- Git already tracks changes with timestamps and authors
- Keeps the model simple

---

### 6. Multi-Domain Projects

**Position: Single primary domain per project. Secondary domains via subdirectories (future scope).**

For v1, each project has exactly one domain declared in `praxis.yaml`.

Rationale:
- Keeps resolution model simple: domain + stage + privacy → behavior
- Most real projects have a primary domain
- Multi-domain (e.g., Build + Write in one repo) is future scope

**Future extension (not v1):**
```yaml
# Hypothetical multi-domain structure
domains:
  - path: ./
    domain: build
    stage: execute
  - path: ./docs/blog/
    domain: write
    stage: shape
```

---

### 7. Privacy Composition

**Position: Single privacy level per project. Highest sensitivity wins.**

If a project contains artifacts of varying sensitivity, declare the highest level.

Rationale:
- Simple mental model
- Conservative default (protects sensitive material)
- Per-artifact privacy is future scope if needed

---

## Example `praxis.yaml`

```yaml
# Minimal valid config
domain: build
stage: formalize
privacy_level: personal

# Optional
environment: Home
```

---

## Validation Rules Summary

| Rule | Severity | Trigger |
|------|----------|---------|
| Unknown domain | Error | `domain` not in allowed list |
| Unknown stage | Error | `stage` not in allowed list |
| Unknown privacy level | Error | `privacy_level` not in allowed list |
| Missing formalize artifact | Error | `stage` ≥ commit AND artifact not found |
| Invalid stage regression | Warning | Transition not in allowed table |
| Privacy downgrade | Warning | `privacy_level` decreased from prior commit |

---

## Consequences

### Enables
- Simple CLI: `praxis validate` checks config + artifact existence
- Clear error messages for common failures
- Git-native workflow (no external state)

### Limits
- No content inspection (SOD could be empty and pass)
- No multi-domain support in v1
- No per-artifact privacy in v1

### Deferred
- Deep artifact validation
- Multi-domain projects
- Per-artifact privacy levels
- Stricter regression enforcement

---

## Next Steps

1. Work through Issue #4 (template-python-cli) using these draft positions
2. Note friction points and adjust positions as needed
3. Finalize this ADR based on real-world learnings
4. Update ADR-001 with validated assumptions
5. Implement first increment against the finalized model

## Open Questions (To Resolve During Issue #4)

- Does manual stage tracking feel natural or burdensome?
- Is `docs/sod.md` the right convention, or should artifact paths be configurable?
- What's the minimum useful validation that provides value without ceremony?
- Should `praxis validate` be run manually, or integrated into git hooks?
