# Project Structure Reorganization

**Date:** 2025-12-29  
**Status:** Research / Discovery

## The Problem

The current `projects/` folder conflates two distinct purposes:

1. **Praxis Extensions** — Sub-applications that extend Praxis functionality (e.g., `render-run`)
2. **Personal Projects** — Projects that _use_ Praxis but aren't part of the reusable framework (e.g., `xmas-cards-2025`)

This creates confusion:

- People cloning `praxis-ai` to use the framework get personal projects they don't need
- The relationship between Praxis and its extensions is unclear
- Projects that should remain private are mixed with shareable code

## Current Structure

```text
projects/
  code/
    render-run/           # Extension: image generation for Create domain
    template-python-cli/  # Extension: reusable CLI template
  create/
    bowerbird/            # Personal: digital collection management
    xmas-cards-2025/      # Personal: holiday cards project
```

## Proposed Mental Model

### Extensions (formerly "submodules")

These are **sub-applications that Praxis depends on** to provide domain-specific functionality:

| Extension              | Domain | Purpose                                       |
| ---------------------- | ------ | --------------------------------------------- |
| `render-run`           | Create | Send prompts to AI, receive images            |
| `template-python-cli`  | Code   | Scaffold new CLI projects                     |
| (future) `doc-render`  | Write  | Render markdown to various formats            |
| (future) `learn-track` | Learn  | Track learning progress and spaced repetition |

**Characteristics:**

- Praxis _uses_ these to produce artifacts
- Should be included in the main repo (or clearly documented as dependencies)
- Versioned alongside Praxis
- Shareable with anyone using Praxis

### Personal Projects

These are **projects created using Praxis** as the governance framework:

| Project                  | Domain  | Purpose                     |
| ------------------------ | ------- | --------------------------- |
| `xmas-cards-2025`        | Create  | Holiday card designs        |
| `bowerbird`              | Create  | Personal digital collection |
| (future) any client work | Various | Work products               |

**Characteristics:**

- Praxis is a _tool_ for these, not the other way around
- Should NOT be in the main Praxis repo
- May be private, confidential, or simply irrelevant to Praxis users
- Live in their own repos, possibly in a separate workspace

---

## Questions to Answer

### 1. Directory Structure

**Option A: Rename and Separate**

```text
praxis-ai/
  extensions/           # Things Praxis uses
    render-run/
    template-python-cli/
  examples/             # Reference implementations (not personal)
    uat-praxis-code/
```

Personal projects live elsewhere entirely (e.g., `~/code/praxis-projects/`)

**Option B: Keep projects/, add extensions/**

```text
praxis-ai/
  extensions/           # Things Praxis uses
    render-run/
    template-python-cli/
  projects/             # Worked examples only (not personal)
    uat-praxis-code/
```

**Option C: Use naming convention**

```text
praxis-ai/
  projects/
    _extensions/        # Underscore = framework code
      render-run/
      template-python-cli/
    examples/           # Shareable worked examples
      uat-praxis-code/
```

**Question:** Should personal projects be in the Praxis repo at all?

### 2. Submodule Strategy

Current: All projects are git submodules pointing to separate repos.

**Options:**

- **Keep submodules:** Extensions remain submodules, personal projects removed entirely
- **Inline extensions:** Move extension code directly into Praxis (monorepo style)
- **Hybrid:** Extensions inline, examples as submodules

**Question:** What's the maintenance burden of submodules vs. the benefit of separate versioning?

### 3. Personal Projects Workflow

If personal projects are removed from `praxis-ai`, how do they access Praxis?

**Option A: Symlink docs**

```bash
# In personal project
ln -s ~/code/praxis-ai/docs docs/praxis-docs
```

**Option B: Praxis as a dependency**

```yaml
# In personal project's praxis.yaml
praxis_path: ~/code/praxis-ai
```

**Option C: Praxis CLI resolves globally**

```bash
# Praxis CLI knows where its home is
praxis opinions  # Works from any project, pulls from global Praxis install
```

**Option D: Separate workspace with multi-root**

```text
~/code/praxis-workspace/
  praxis-ai/          # The framework
  xmas-cards-2025/    # Personal project
  bowerbird/          # Personal project
```

VS Code multi-root workspace provides unified view.

**Question:** How much does a personal project need to "see" Praxis docs during active work?

### 4. Extension Integration

How should Praxis invoke extensions like `render-run`?

**Option A: CLI subprocess**

```bash
praxis render --prompt "a cat in space"
# Internally calls: render-run generate --prompt "..."
```

**Option B: Python import**

```python
from praxis.extensions.render_run import generate
generate(prompt="a cat in space")
```

**Option C: Plugin discovery**

```yaml
# praxis.yaml
extensions:
  - render-run
  - template-python-cli
```

**Question:** Should extensions be tightly coupled (import) or loosely coupled (CLI)?

### 5. What Belongs in "Examples"?

If we keep an `examples/` or `projects/` folder, what should be in it?

**Candidates:**

- `uat-praxis-code` — Minimal hello-world with full lifecycle docs
- Domain-specific starters (one per domain?)
- "Golden path" reference implementations

**Question:** Are examples part of the test suite, or just documentation?

---

## Proposed Decision

Based on the analysis above, my current thinking:

### Structure

```text
praxis-ai/
  src/praxis/           # CLI package
  docs/                 # Specifications
  extensions/           # Sub-applications Praxis uses
    render-run/         # (submodule)
    template-python-cli/ # (submodule or inline?)
  examples/             # Reference implementations
    uat-praxis-code/    # (submodule)
  tests/                # BDD tests
```

### Personal Projects

- Live outside `praxis-ai` repo entirely
- Use VS Code multi-root workspace OR symlinks for doc access
- Praxis CLI works globally (installed via pip/pipx)

### Migration Steps

1. Rename `projects/` → `extensions/` and `examples/`
2. Move personal projects (`xmas-cards-2025`, `bowerbird`) out of repo
3. Update README and documentation
4. Update any CI/CD that references old paths

---

## Open Questions

1. **Where should personal projects live?** Separate workspace? Same parent directory?
2. **How do personal projects get Praxis opinions?** Global CLI? Symlinks? Copy?
3. **Should extensions be submodules or inline?** Trade-off: versioning vs. simplicity
4. **Is `uat-praxis-code` an example or a test fixture?** Maybe both?
5. **What happens when someone forks Praxis?** Do they get examples? Extensions?

---

## Next Steps

- [ ] Decide on directory naming (`extensions/` vs `plugins/` vs `tools/`)
- [ ] Decide on personal project workflow
- [ ] Create migration plan
- [ ] Update README with new structure
- [ ] Test that Praxis CLI still works with new paths
