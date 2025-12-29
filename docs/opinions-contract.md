# Praxis Opinions Contract

> **STATUS: ACTIVE — Production-ready specification**

**Version:** 1.0.0
**Date:** 2025-12-28
**Supersedes:** opinions-contract-draft.md (0.1.0-draft)

---

## 1. Overview

This document defines the contract between the Praxis opinions framework and the Praxis policy engine. It specifies:

- Where opinion files live
- What format they follow
- How inheritance works
- How projects declare their type
- CLI command interface
- AI agent integration pattern
- Error handling behavior

---

## 2. File Location Convention

**Root location:** `docs/opinions/` at the repository root

```
docs/opinions/
├── _templates/                     # Templates for creating opinion files
│   ├── GUIDE.md                    # How to use templates
│   ├── README-template.md          # Domain/subtype overview template
│   ├── principles-template.md      # Cross-stage principles template
│   └── stage-template.md           # Stage-specific opinion template
│
├── _shared/                        # Cross-domain principles (always apply)
│   └── first-principles.md
│
├── code/                           # Code domain
│   ├── README.md                   # Domain overview and navigation
│   ├── principles.md               # Domain principles (apply to ALL stages)
│   ├── capture.md                  # Stage: Capture
│   ├── sense.md                    # Stage: Sense
│   ├── explore.md                  # Stage: Explore
│   ├── shape.md                    # Stage: Shape
│   ├── formalize.md                # Stage: Formalize
│   ├── commit.md                   # Stage: Commit
│   ├── execute.md                  # Stage: Execute
│   ├── sustain.md                  # Stage: Sustain
│   ├── close.md                    # Stage: Close
│   └── subtypes/
│       ├── cli/
│       │   ├── README.md           # CLI-specific overview
│       │   ├── principles.md       # CLI principles (all CLI stages)
│       │   └── python/
│       │       └── README.md       # CLI-Python specific
│       ├── library/
│       ├── api/
│       ├── webapp/
│       ├── infrastructure/
│       └── script/
│
├── create/                         # Create domain (same structure)
├── write/                          # Write domain (same structure)
├── learn/                          # Learn domain (same structure)
└── observe/                        # Observe domain (same structure)
```

---

## 3. Opinion File Format

**Format:** Markdown with YAML frontmatter

### 3.1 Frontmatter Schema (Required Fields)

```yaml
---
domain: code                    # Required: code | create | write | learn | observe
version: "1.0"                  # Required: semver string (quoted)
status: active                  # Required: draft | active | deprecated
---
```

### 3.2 Frontmatter Schema (Optional Fields)

```yaml
---
stage: capture                  # Optional: restrict to specific stage
subtype: cli                    # Optional: restrict to subtype
inherits:                       # Optional: explicit inheritance override
  - code
  - code/subtypes/cli
author: human                   # Optional: human | ai | hybrid
last_reviewed: 2025-12-28       # Optional: ISO date, freshness indicator
---
```

### 3.3 Body Structure (README Files)

```markdown
# {Domain} Domain Opinions

> **Scope:** One-sentence scope description

## Quick Navigation

- [Principles](principles.md) — Cross-stage principles
- Stages: [Capture](capture.md) | [Sense](sense.md) | ...
- Subtypes: [CLI](subtypes/cli/) | [Library](subtypes/library/) | ...

## Domain at a Glance

| Aspect | Value |
|--------|-------|
| Primary artifact | What this domain produces |
| Quality signals | How you know work is good |
| AI role | Default AI permissions |
| Key risks | Main risks to manage |

## When to Use This Domain

Criteria for choosing this domain.

## Related Domains

Cross-references to related domains.
```

### 3.4 Body Structure (Principles Files)

```markdown
# {Domain} Domain Principles

> **Scope:** These principles apply across ALL lifecycle stages.

## Core Principles

### 1. {Principle Name}

- **Statement:** Actionable statement
- **Rationale:** Why this matters
- **Source:** Attribution (author, book, methodology)
- **Severity:** must-have | should-have | nice-to-have

## AI Guidelines (All Stages)

| Operation | Permission | Notes |
|-----------|------------|-------|
| suggest | Allowed | Context |
| complete | Allowed | Context |
| generate | Ask | Context |
| transform | Ask | Context |
| execute | Ask | Context |

## Anti-Patterns (All Stages)

### {Anti-Pattern Name}

- **What:** Description of the pattern
- **Why bad:** Why it's problematic
- **Instead:** What to do instead

## Influential Lineage (Optional)

| Author | Key Contribution |
|--------|------------------|
| Name | What they contributed |
```

### 3.5 Body Structure (Stage Files)

```markdown
# {Domain} × {Stage} Opinions

> **Summary:** One-sentence summary of this stage's focus.

## Stage Context

| Aspect | Value |
|--------|-------|
| Entry criteria | What must exist to enter |
| Exit criteria | What must exist to exit |
| Commitment level | Sunk cost at this stage |
| AI role | AI permissions for this stage |

## Principles

### 1. {Stage Principle Name}

- **Statement:** Actionable statement
- **Rationale:** Why this matters
- **Source:** Attribution
- **Severity:** must-have | should-have | nice-to-have

## Quality Gates

Before advancing to **{Next Stage}**:

| Gate | Description | Severity |
|------|-------------|----------|
| G1 | Gate description | must-have |
| G2 | Gate description | should-have |

## Anti-Patterns

### {Stage Anti-Pattern Name}

- **What:** Description
- **Why bad:** Why problematic
- **Instead:** Alternative

## Stage Transition Checklist

To advance from **{Stage}** → **{Next Stage}**:

- [ ] Criterion 1
- [ ] Criterion 2

## AI Guidance

### What AI Can Do
- List of permitted actions

### What AI Should Ask About
- List of actions requiring approval

### What AI Should Avoid
- List of prohibited actions

## Domain-Specific Examples (Optional)

| Input Type | Location | Notes |
|------------|----------|-------|
| Example | Where it goes | Context |

## References

- [Source](url) — Author
```

---

## 4. Inheritance Model

Opinions inherit from **general → specific**. More specific opinions can:
- Add new principles
- Override parent principles (same name = override)
- Add quality gates
- Refine AI guidance

### 4.1 Inheritance Chain

```
_shared → domain/principles → domain/{stage} → subtype/principles → subtype/{stage}
```

### 4.2 Resolution Algorithm

```python
def resolve_opinions(praxis_yaml: dict) -> list[str]:
    """
    Resolve applicable opinion files for a project.
    Returns ordered list of file paths from general → specific.
    Files that don't exist are excluded.
    """
    opinions = []
    domain = praxis_yaml["domain"]
    stage = praxis_yaml.get("stage")
    subtype = praxis_yaml.get("subtype")

    # 1. Shared principles (always apply)
    opinions.append("_shared/first-principles.md")

    # 2. Domain level
    opinions.append(f"{domain}/README.md")
    opinions.append(f"{domain}/principles.md")

    # 3. Domain stage (if stage defined)
    if stage:
        opinions.append(f"{domain}/{stage}.md")

    # 4. Subtype chain (if subtype defined)
    if subtype:
        # Handle nested subtypes: "cli-python" → ["cli", "python"]
        segments = subtype.replace(".", "-").split("-")
        accumulated = f"{domain}/subtypes"

        for segment in segments:
            accumulated = f"{accumulated}/{segment}"
            opinions.append(f"{accumulated}/README.md")
            opinions.append(f"{accumulated}/principles.md")
            if stage:
                opinions.append(f"{accumulated}/{stage}.md")

    # Filter to existing files only
    base_path = "docs/opinions"
    return [o for o in opinions if file_exists(f"{base_path}/{o}")]
```

### 4.3 Example Resolution

For a project with:
```yaml
domain: code
stage: capture
subtype: cli-python
```

Resolution order (if all files exist):
1. `_shared/first-principles.md`
2. `code/README.md`
3. `code/principles.md`
4. `code/capture.md`
5. `code/subtypes/cli/README.md`
6. `code/subtypes/cli/principles.md`
7. `code/subtypes/cli/capture.md`
8. `code/subtypes/cli/python/README.md`
9. `code/subtypes/cli/python/principles.md`
10. `code/subtypes/cli/python/capture.md`

### 4.4 Merge Rules

| Element | Merge Behavior |
|---------|----------------|
| Principles (same name) | Later overrides earlier |
| Principles (different names) | Concatenate |
| Quality Gates | Concatenate (all apply) |
| Anti-Patterns | Concatenate |
| AI Guidelines | Later overrides earlier for same operation |

---

## 5. praxis.yaml Extension

Projects declare their type in `praxis.yaml`:

```yaml
# Required (existing)
domain: code
stage: capture
privacy_level: public
environment: Home

# New optional field
subtype: cli                    # Enables subtype opinion resolution
```

### 5.1 Subtype Format

| Format | Example | Matches |
|--------|---------|---------|
| Simple | `cli` | `subtypes/cli/` |
| Nested (hyphen) | `cli-python` | `subtypes/cli/python/` |
| Nested (dot) | `cli.python` | `subtypes/cli/python/` |

### 5.2 Valid Subtypes by Domain

| Domain | Valid Subtypes |
|--------|----------------|
| code | cli, library, api, webapp, infrastructure, script |
| create | visual, audio, video, interactive, generative, design |
| write | technical, business, narrative, academic, journalistic |
| learn | skill, concept, practice, course, exploration |
| observe | notes, bookmarks, clips, logs, captures |

---

## 6. CLI Commands

### 6.1 List Applicable Opinions

```bash
# Show resolved opinions for current project
praxis opinions

# Output:
# Applicable opinions (in resolution order):
#   1. _shared/first-principles.md
#   2. code/README.md
#   3. code/principles.md
#   4. code/capture.md
#
# Total: 4 files
```

### 6.2 Generate AI Prompt

```bash
# Generate formatted context for AI assistants
praxis opinions --prompt

# Output: Concatenated markdown of all applicable opinions
# Suitable for copying into AI context
```

### 6.3 Validate Against Quality Gates

```bash
# Check current work against opinion quality gates
praxis opinions --check

# Output:
# Quality Gates for code × capture:
#   [PASS] G1: Input is stored in a searchable location
#   [WARN] G2: Input has minimal metadata (date, source)
#   [SKIP] G3: Similar existing items identified (nice-to-have)
#
# Result: 1 pass, 1 warning, 1 skipped
```

### 6.4 List All Available Opinions

```bash
# Show tree of all opinion files (not just applicable)
praxis opinions --list

# Output:
# docs/opinions/
# ├── _shared/
# │   └── first-principles.md
# ├── code/
# │   ├── README.md
# │   ├── principles.md
# │   ├── capture.md
# │   └── subtypes/
# │       └── cli/
# │           └── README.md
# ...
```

### 6.5 Query Without praxis.yaml

```bash
# Show opinions for specific domain/stage without praxis.yaml
praxis opinions --domain code --stage capture --subtype cli

# Useful for exploring opinions before project initialization
```

### 6.6 JSON Output

```bash
# Machine-readable output
praxis opinions --json

# Output:
# {
#   "domain": "code",
#   "stage": "capture",
#   "subtype": null,
#   "files": [
#     {"path": "_shared/first-principles.md", "exists": true},
#     {"path": "code/README.md", "exists": true},
#     ...
#   ]
# }
```

---

## 7. AI Agent Integration

### 7.1 CLAUDE.md Addition

Add to project CLAUDE.md:

```markdown
## Opinions Framework

When working on this Praxis project:

1. **Check for opinions:** Look for `docs/opinions/` directory
2. **Read praxis.yaml:** Determine domain, stage, subtype
3. **Resolve applicable opinions:** Use inheritance chain:
   - `_shared/` → `{domain}/` → `{domain}/{stage}` → `subtypes/`
4. **Apply as guidance:** Opinions are advisory, not hard rules
5. **Note conflicts:** If user instruction conflicts with opinion, follow user
6. **Reference gates:** Use quality gates when evaluating readiness

Run `praxis opinions --prompt` to get formatted context.
```

### 7.2 Agent Behavior Guidelines

| Situation | Agent Behavior |
|-----------|----------------|
| Opinion exists | Load and apply as context |
| Opinion missing | Proceed without; suggest creating one |
| Opinion conflicts with user | Follow user instruction; note the conflict |
| Quality gate fails | Warn user; don't block unless must-have |
| Unclear stage | Ask user to clarify before proceeding |

### 7.3 AI Permission Interpretation

When opinions specify AI permissions:

| Permission | Agent Interpretation |
|------------|---------------------|
| Allowed | Proceed without asking |
| Ask | Request explicit approval before action |
| Blocked | Do not perform; explain why if asked |

---

## 8. Conflict Resolution

### 8.1 Resolution Priority

When opinions conflict, resolution order is:

1. **User instruction** — Always wins
2. **Most specific opinion** — Subtype overrides domain
3. **Later in chain** — Later file overrides earlier
4. **Explicit inherits** — `inherits:` field overrides default chain

### 8.2 Conflict Detection

Tools should warn when:
- Same principle name appears with different content
- AI permissions differ between levels
- Quality gates have contradictory requirements

### 8.3 Conflict Logging

```bash
praxis opinions --check --verbose

# Output includes:
# [CONFLICT] Principle "Test Coverage" defined in:
#   - code/principles.md: "Aim for 80% coverage"
#   - code/subtypes/cli/principles.md: "Aim for 90% coverage"
#   Resolution: Using subtype definition (90%)
```

---

## 9. Error Handling

| Error | Severity | Behavior |
|-------|----------|----------|
| Missing `docs/opinions/` | Warning | No opinions applied; suggest initialization |
| Missing `praxis.yaml` | Warning | Cannot resolve; require `--domain` flag |
| Invalid frontmatter YAML | Error | Skip file with message; continue with others |
| Unknown domain in frontmatter | Error | Skip file with message |
| Unknown stage in frontmatter | Error | Skip file with message |
| Circular inheritance | Error | Fail resolution; report cycle |
| Missing inherited file | Warning | Continue with available files |
| Deprecated opinion file | Warning | Load but warn; suggest update |

### 9.1 Error Messages

```bash
# Missing opinions directory
$ praxis opinions
Warning: No opinions directory found at docs/opinions/
Run `praxis init --opinions` to create opinion structure.

# Invalid frontmatter
$ praxis opinions
Error: Invalid YAML in docs/opinions/code/capture.md
  Line 3: expected ':' but found '-'
Skipping file; continuing with 3 remaining opinions.

# Circular inheritance
$ praxis opinions
Error: Circular inheritance detected:
  code/subtypes/cli/principles.md inherits code/subtypes/cli/python/principles.md
  code/subtypes/cli/python/principles.md inherits code/subtypes/cli/principles.md
Resolution failed.
```

---

## 10. Validation Rules

### 10.1 Frontmatter Validation

| Field | Rule |
|-------|------|
| domain | Must be: code, create, write, learn, observe |
| stage | Must be: capture, sense, explore, shape, formalize, commit, execute, sustain, close |
| version | Must be valid semver (e.g., "1.0", "1.0.0") |
| status | Must be: draft, active, deprecated |
| subtype | Must be valid for domain (see section 5.2) |

### 10.2 Content Validation

```bash
praxis opinions --validate

# Checks:
# - All frontmatter fields are valid
# - All referenced files in inherits: exist
# - All internal links resolve
# - No duplicate principle names within file
# - Severity values are valid
```

---

## 11. Stage Reference

| Stage | Purpose | Entry Criteria | Exit Criteria |
|-------|---------|----------------|---------------|
| capture | Collect raw inputs | Any input exists | Input stored |
| sense | Convert to understanding | Captured inputs exist | Problem articulated |
| explore | Generate possibilities | Sense complete | 2-3 directions exist |
| shape | Converge to direction | Options exist | Direction chosen |
| formalize | Create durable artifacts | Shape complete | SOD exists |
| commit | Decide to proceed | SOD complete | Resources allocated |
| execute | Produce artifact | Commit complete | Artifact produced |
| sustain | Maintain delivered work | Execute complete | Work retired/closed |
| close | End intentionally | Sustain complete | Leverage captured |

---

## 12. AI Permissions Reference

| Operation | Code | Create | Write | Learn | Observe |
|-----------|:----:|:------:|:-----:|:-----:|:-------:|
| suggest | Allowed | Allowed | Allowed | Allowed | Allowed |
| complete | Allowed | Allowed | Allowed | Allowed | Blocked |
| generate | Ask | Allowed | Ask | Allowed | Blocked |
| transform | Ask | Allowed | Ask | Allowed | Blocked |
| execute | Ask | — | — | — | — |
| publish | Ask | Ask | Ask | Ask | Ask |

**Legend:** Allowed = proceed, Ask = request approval, Blocked = do not perform, — = N/A

*Note: Observe domain blocks AI generation to preserve raw capture authenticity.*

---

## 13. Resolved Questions

Questions from draft contract, now resolved:

### 13.1 Subtype Depth

**Decision:** Support up to 2 levels of nesting (e.g., `cli-python`).

**Rationale:** Deeper nesting adds complexity without proportional value. Two levels cover most real-world cases (subtype + technology/variant).

### 13.2 Cross-Domain Opinions

**Decision:** Each artifact belongs to exactly one domain. Projects spanning domains should have separate praxis.yaml or use primary domain.

**Rationale:** Simplifies resolution. Domain transitions are handled through explicit artifact promotion (see domain research).

### 13.3 Opinion Versioning

**Decision:** Use semver in frontmatter. Breaking changes require new version. Old versions can coexist with `deprecated` status.

**Rationale:** Allows gradual migration. Tools can warn on deprecated opinions.

### 13.4 Auto-Detection

**Decision:** Defer to future story. Initial implementation requires explicit `subtype:` declaration.

**Rationale:** Reduces scope for v1.0. Auto-detection can be added later based on file patterns (e.g., pyproject.toml → cli-python).

---

## 14. Migration from Draft

To migrate from draft contract (0.1.0-draft):

1. Opinion files created under draft are compatible (no changes needed)
2. Remove `-draft` suffix from contract reference
3. Update any tooling referencing draft schema

---

## 15. Sources

This contract synthesizes:

- `01-refine-lifecycle-research-merged.md` — Stage definitions
- `02-refine-domains-research.md` — Domain and subtype taxonomies, AI permissions
- `opinions-contract-draft.md` — Initial draft specification
- Story 04 template validation — Body structure refinements

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0-draft | 2025-12-28 | Initial draft |
| 1.0.0 | 2025-12-28 | Finalized: CLI commands, AI integration, error handling, conflict resolution |
