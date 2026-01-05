# ADR-004: Directory Structure for Prompts, Workflows, and Templates

**Status:** Accepted  
**Date:** 2026-01-05  
**Deciders:** Product Owner, Architect, Developer  
**Relates to:** ADR-003 (Extension Manifest Schema), Issue #4 (template-python-cli)

---

## Context

Praxis projects require consistent, predictable locations for reusable artifacts that support the lifecycle:

- **Templates** — Scaffolding for stage artifacts (SOD.md, CAPTURE.md, etc.) and new projects
- **Prompts** — Reusable AI prompts for specific tasks (role-based system prompts, domain-specific guidance)
- **Workflows** — Multi-step automation processes (pipeline stages, lifecycle progressions)

These artifacts exist at two levels:

1. **System-level (Praxis framework)** — Shared across all projects, bundled with the CLI
2. **Project-level** — Project-specific overrides and customizations

Without standardized locations, users cannot:
- Predict where to find or place templates
- Override system defaults reliably
- Share reusable prompts and workflows across projects
- Build extensions that contribute templates safely

This ADR establishes the canonical directory structure and precedence rules.

---

## Decision

### 1. System-Level Structure (Praxis Framework)

The Praxis framework repository (`jayers99/praxis-ai`) uses this structure:

```
praxis-ai/                          # Framework repository root
├── src/praxis/templates/           # Bundled templates (shipped with CLI)
│   ├── stage/                      # Generic stage templates (all domains)
│   │   ├── capture.md
│   │   ├── sense.md
│   │   ├── formalize.md
│   │   └── ...
│   └── domain/                     # Domain-specific templates
│       ├── code/
│       │   ├── artifact/           # Formalize artifacts
│       │   │   └── sod.md
│       │   └── subtype/            # Subtype-specific variants
│       │       ├── cli/
│       │       │   └── stage/
│       │       │       └── formalize.md
│       │       ├── library/
│       │       └── api-backend/
│       ├── create/
│       │   └── artifact/
│       │       └── brief.md
│       ├── write/
│       │   └── artifact/
│       │       └── brief.md
│       └── learn/
│           └── artifact/
│               └── plan.md
│
├── core/                           # Normative specifications
│   ├── roles/                      # AI role definitions and prompts
│   │   ├── system-prompt-bundle.md
│   │   ├── invocation-syntax.md
│   │   └── definitions/
│   ├── spec/                       # Lifecycle, domains, privacy specs
│   └── governance/                 # Decision arbitration, opinions contract
│
└── opinions/                       # Advisory guidance (see ADR-003)
```

**Workflows:** Implemented as Python domain models in `src/praxis/domain/pipeline/` and `src/praxis/application/pipeline/`. Not file-based in MVP.

**Prompts:** Stored in `core/roles/` as Markdown documentation. Role-based prompts are in `system-prompt-bundle.md`.

---

### 2. Project-Level Structure (User Projects)

User projects created with `praxis init` or `praxis new` use this structure:

```
my-project/                         # User project root
├── praxis.yaml                     # Project governance config
├── docs/                           # Rendered stage documents
│   ├── capture.md                  # Stage documents (from templates)
│   ├── formalize.md
│   ├── sod.md                      # Domain artifact (code projects)
│   └── ...
│
└── .praxis/                        # Project-local overrides (optional)
    ├── templates/                  # Override system templates
    │   ├── stage/
    │   │   └── formalize.md        # Custom formalize template
    │   └── domain/
    │       └── code/
    │           └── artifact/
    │               └── sod.md      # Custom SOD template
    │
    ├── prompts/                    # Project-specific AI prompts
    │   ├── review-checklist.md
    │   └── commit-message-guide.md
    │
    └── workflows/                  # Project-specific workflows (future)
        └── release-process.md
```

**Key principles:**

- `.praxis/` is **optional** — most projects use system defaults
- Templates in `.praxis/templates/` **override** system templates by path
- Prompts are project-specific guidance, not enforced by the system
- Workflows are documentation-only in MVP (automation is future scope)

---

### 3. Workspace-Level Structure (User Workspace)

Workspaces (typically `$PRAXIS_HOME`) organize multiple projects and extensions:

```
$PRAXIS_HOME/                       # User workspace root (default: ~/.praxis)
├── workspace-config.yaml           # Workspace settings
├── projects/                       # User projects live here
│   ├── my-cli-tool/
│   ├── my-web-app/
│   └── ...
│
├── extensions/                     # Installed extensions
│   ├── mobile-pack/
│   │   ├── praxis-extension.yaml
│   │   ├── templates/              # Extension templates
│   │   │   └── domain/code/subtype/mobile/
│   │   └── opinions/
│   └── game-dev-pack/
│
├── examples/                       # Example projects
│   └── template-python-cli/
│
└── bench/                          # Workspace-level artifacts
    ├── sessions/                   # AI session summaries
    │   └── 2026-01-05.md
    └── inbox-from-subagents/       # Subagent outputs
```

---

### 4. Template Resolution Precedence

When rendering templates (e.g., `praxis templates render`), the resolver searches in this order:

1. **Project-local** (`.praxis/templates/` in project root) — **Highest priority**
2. **Custom roots** (via `--template-root` CLI flag)
3. **Extension templates** (alphabetically by extension name, A > Z)
4. **Core templates** (`src/praxis/templates/` in framework) — **Fallback**

**First match wins.** This allows:
- Projects to override any template
- Extensions to provide domain/subtype-specific variants
- Core to provide sensible defaults

**Note:** Extension precedence for templates (A > Z) differs from opinions (Z > A, per ADR-003). This is because templates use "first match wins" with extensions sorted A-Z, while opinions merge in reverse alphabetical order. Both are deterministic but may be unified in future versions.

**Example resolution path for `formalize.md` in a `code` domain, `cli` subtype project:**

```
1. .praxis/templates/domain/code/subtype/cli/stage/formalize.md  (project)
2. <custom-root>/domain/code/subtype/cli/stage/formalize.md       (CLI arg)
3. extensions/mobile-pack/templates/domain/code/subtype/cli/stage/formalize.md (extension)
4. src/praxis/templates/domain/code/subtype/cli/stage/formalize.md (core)
5. src/praxis/templates/domain/code/stage/formalize.md             (core fallback)
6. src/praxis/templates/stage/formalize.md                         (core generic)
```

See `src/praxis/infrastructure/stage_templates/template_resolver.py` for implementation.

---

### 5. Template Path Conventions

Templates follow a hierarchical naming convention:

**Stage templates:**
```
stage/{stage}.md                                    # Generic (all domains)
domain/{domain}/stage/{stage}.md                    # Domain-specific
domain/{domain}/subtype/{subtype}/stage/{stage}.md  # Subtype-specific
```

**Artifact templates:**
```
domain/{domain}/artifact/{artifact}.md                    # Domain-specific
domain/{domain}/subtype/{subtype}/artifact/{artifact}.md  # Subtype-specific
```

**Examples:**
- `stage/formalize.md` — Generic formalize template
- `domain/code/artifact/sod.md` — Code domain SOD template
- `domain/code/subtype/cli/stage/formalize.md` — CLI-specific formalize template

---

### 6. Prompts Organization

**System-level prompts (framework):**
- **Location:** `core/roles/`
- **Purpose:** Role-based AI system prompts (Research Librarian, Product Owner, etc.)
- **Format:** Markdown documentation
- **Usage:** Reference in AI tool configurations, CLAUDE.md, or agent invocations

**Project-level prompts (optional):**
- **Location:** `.praxis/prompts/` in project root
- **Purpose:** Project-specific AI guidance (review checklists, commit message templates, etc.)
- **Format:** Markdown or plaintext
- **Usage:** Manual reference or tool integration (not enforced by Praxis)

**Design note:** Prompts are currently **documentation artifacts**, not first-class Praxis entities. Future work may add prompt management commands.

---

### 7. Workflows Organization

**System-level workflows:**
- **Location:** `src/praxis/domain/pipeline/` (Python domain models)
- **Purpose:** Lifecycle progression, CCR pipeline, stage executors
- **Format:** Python code (domain-driven design)
- **Examples:** `PipelineStage`, `RiskTier`, `CCROrchestrator`

**Project-level workflows (future):**
- **Location:** `.praxis/workflows/` in project root
- **Purpose:** Project-specific multi-step processes (release checklist, onboarding, etc.)
- **Format:** Markdown documentation (MVP) or structured YAML (future)
- **Usage:** Documentation-only in v1; automation is future scope

**Design note:** Workflows are currently **code or documentation**, not declarative automation. Future work may add workflow execution engines.

---

## Rationale

### Why Three Levels (System, Project, Workspace)?

- **System (framework):** Provides defaults for all users, versioned with the CLI
- **Project:** Enables per-project customization without forking the framework
- **Workspace:** Organizes multiple projects and shares extensions across them

This mirrors successful patterns (npm global vs local, git system vs user vs repo config).

### Why Templates in `src/praxis/templates/`?

- Bundled with the Python package (no external dependencies)
- Versioned with the CLI (templates evolve with features)
- Overridable via project-local `.praxis/templates/`
- Consistent with Python package data conventions

### Why Prompts in `core/roles/`?

- Prompts are **normative guidance** (like lifecycle specs)
- Roles are domain concepts (Research Librarian, Product Owner)
- Co-located with role definitions for discoverability
- Separates prompts from templates (different lifecycle and versioning)

### Why Workflows as Code in `domain/pipeline/`?

- Workflows encode **business logic** (stage transitions, risk assessment)
- Python domain models provide type safety and testability
- Aligns with hexagonal architecture (domain layer)
- Declarative workflows (YAML/JSON) are future scope if needed

### Why `.praxis/` for Project-Local Artifacts?

- Conventional "dot-directory" pattern (like `.git`, `.github`)
- Namespaced to avoid conflicts with project files
- Optional (most projects don't need it)
- Future-proof for additional project-local configs

### Why Different Extension Precedence for Templates vs Opinions?

**Current state:**
- **Templates:** A-named extensions win over Z-named (A > Z)
- **Opinions:** Z-named extensions win over A-named (Z > A, per ADR-003)

**Rationale:**
- Both implementations are deterministic and documented
- Templates use "first match wins" with A-Z sorted extension list
- Opinions merge in reverse alphabetical order with explicit conflict tracking
- Different precedence models reflect different use cases (files vs merged trees)

**Future consideration:** May unify precedence in v1.0 if user confusion emerges. Current approach prioritizes determinism and clarity of implementation.

---

## Consequences

### Enables

- **Predictable locations:** Users know where to find/place templates, prompts, workflows
- **Safe overrides:** Projects can customize without modifying system files
- **Extension contributions:** Extensions provide templates via manifests (ADR-003)
- **Versioned defaults:** Templates ship with the CLI, evolve with features
- **Documentation clarity:** Clear separation of system vs project vs workspace artifacts

### Limits

- **No prompt execution:** Prompts are documentation-only in v1 (no CLI integration)
- **No workflow automation:** Workflows are code or documentation, not declarative engines
- **No template variables (yet):** Templates use basic Jinja2, not full templating DSL
- **Manual override management:** No `praxis templates list-overrides` command (yet)

### Deferred

- **Prompt management CLI:** `praxis prompts list|add|remove` (future)
- **Declarative workflows:** YAML/JSON workflow definitions with execution (future)
- **Template registry:** Shareable template packs (beyond extensions)
- **Advanced templating:** Conditional includes, variables, functions (if needed)

---

## Migration Path

**Existing projects:** No migration needed. This ADR documents existing structure.

**Extensions:** Extensions using ADR-003 manifests already contribute templates to `templates/` directory. No changes required.

**Future enhancements:**
1. Add `praxis templates list` to show resolution precedence
2. Add `praxis prompts` subcommand for prompt management
3. Add `.praxis/workflows/` support with validation

---

## Implementation Status

**Already implemented:**
- ✅ Core templates in `src/praxis/templates/`
- ✅ Template resolver with precedence (project > extension > core)
- ✅ Project-local template override support (`.praxis/templates/`)
- ✅ Stage and artifact templates
- ✅ Extension template contributions (ADR-003)
- ✅ System prompts in `core/roles/`
- ✅ Pipeline workflows as domain models

**Not yet implemented:**
- ❌ `.praxis/` directory auto-creation in `praxis init`
- ❌ Tests for project-local template overrides
- ❌ `praxis templates list` command (show resolution precedence)
- ❌ `praxis prompts` CLI commands
- ❌ Declarative workflow definitions

---

## Examples

### Example 1: Override SOD Template for a CLI Project

**Scenario:** A Python CLI project wants a custom SOD template emphasizing CLI UX.

**Steps:**
1. Create `.praxis/templates/domain/code/subtype/cli/artifact/sod.md`
2. Customize SOD sections (add "CLI Design" section, etc.)
3. Run `praxis templates render` — custom template is used

**Result:** Project gets custom SOD, other projects use core default.

---

### Example 2: Share Prompts Across Team Projects

**Scenario:** A team wants a shared commit message guide.

**Steps:**
1. Create an extension: `team-standards-pack`
2. Add `prompts/commit-message-guide.md` to extension
3. Document in extension README: "Copy to `.praxis/prompts/` in your project"
4. Install extension in workspace: `praxis extensions add team-standards-pack`

**Result:** Prompts are shareable but not auto-deployed (manual copy for now).

---

### Example 3: Extension Provides Mobile App Templates

**Scenario:** A mobile developer wants iOS/Android templates.

**Steps:**
1. Create extension: `mobile-pack`
2. Add templates:
   - `templates/domain/code/subtype/mobile/stage/formalize.md`
   - `templates/domain/code/subtype/mobile/artifact/sod.md`
3. Declare in manifest:
   ```yaml
   contributions:
     templates:
       - source: templates/domain/code/subtype/mobile/stage/formalize.md
         target: code/subtype/mobile/stage/formalize.md
         subtypes: [mobile]
   ```
4. Install: `praxis extensions add mobile-pack`

**Result:** Mobile projects get custom templates, other projects unaffected.

---

## Related

- **ADR-003:** Extension Manifest Schema — Defines how extensions contribute templates
- **ADR-001:** Policy Engine Selection — Templates rendered using Pydantic models
- **ADR-002:** Validation Model — Defines artifact path conventions templates target
- **Issue #4:** template-python-cli — First project using template system
- **Core specs:** `core/spec/lifecycle.md`, `core/spec/domains.md` — Define stage and domain models
- **Opinions:** `core/governance/opinions-contract.md` — Opinions are separate from templates

---

## References

**Implementation files:**
- `src/praxis/templates/` — Core templates directory
- `src/praxis/application/templates/template_service.py` — Template rendering service
- `src/praxis/infrastructure/stage_templates/template_resolver.py` — Resolution logic
- `src/praxis/infrastructure/stage_templates/template_paths.py` — Path conventions
- `src/praxis/domain/templates/models.py` — Template domain models
- `core/roles/system-prompt-bundle.md` — System prompts
- `src/praxis/domain/pipeline/` — Workflow domain models

**User documentation:**
- `docs/guides/user-guide.md` — User-facing template usage
- `CLAUDE.md` — References to templates, prompts, workflows
