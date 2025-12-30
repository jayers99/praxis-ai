# Praxis Workspace Structure

**Date:** 2025-12-29  
**Status:** Proposed Architecture (with decisions)

## The Workspace Model

A "Praxis Workspace" is a parent directory that organizes everything related to Praxis usage. Users set `PRAXIS_HOME` to point to their workspace root.

```text
~/praxis-workspace/                    # PRAXIS_HOME points here
│
├── workspace-config.yaml                        # Workspace-level config
│
├── praxis-ai/                         # The framework (cloned from GitHub)
│   ├── src/praxis/                    # CLI package
│   ├── docs/                          # Specifications, opinions
│   ├── extensions.yaml                # Registry of available extensions
│   └── tests/                         # BDD tests
│
├── extensions/                        # Cloned extension repos (managed by praxis)
│   ├── render-run/                    # Create domain: AI image generation
│   ├── template-python-cli/           # Code domain: CLI scaffolding
│   └── (future extensions...)
│
├── examples/                          # Optional: cloned example repos
│   ├── uat-praxis-code/               # Hello-world with full lifecycle
│   ├── opinions-framework/            # Write domain: opinions framework research
│   └── (other examples user selected)
│
└── projects/                          # User's personal projects (your artifacts)
    ├── xmas-cards-2025/               # Create domain project (folder or repo)
    ├── bowerbird/                     # Create domain project
    ├── client-work-xyz/               # Code domain project (likely a repo)
    └── (your projects...)
```

## Decisions Made

### ✅ Examples Location

**Decision:** Examples live at the root of `praxis-workspace/examples/`, not inside `praxis-ai/`.

- Examples are separate repos (like extensions)
- `praxis workspace init` asks user which examples they want
- User selects from checkboxes, Praxis clones them

### ✅ Extension Versioning

**Decision:** Always grab latest `main` branch for now.

- Simpler during development and testing
- Future: Add `praxis extensions update` command
- **Open question:** When/how do we update? On every `praxis` invocation? Manual only?

### ✅ Extension Discovery Source

**Decision:** `extensions.yaml` inside `praxis-ai` repo contains the registry.

```yaml
# praxis-ai/extensions.yaml
extensions:
  render-run:
    repo: https://github.com/jayers99/render-run.git
    domain: create
    description: Send prompts to AI, receive images

  template-python-cli:
    repo: https://github.com/jayers99/template-python-cli.git
    domain: code
    description: Scaffold new CLI projects
```

- `praxis extensions add` launches wizard with checkboxes
- User selects which extensions to install
- Praxis clones selected repos to `$PRAXIS_HOME/extensions/`

### ✅ Examples Discovery Source

**Decision:** `examples.yaml` inside `praxis-ai` repo contains the registry.

```yaml
# praxis-ai/examples.yaml
examples:
  uat-praxis-code:
    repo: https://github.com/jayers99/uat-praxis-code.git
    domain: code
    description: Hello-world project demonstrating full Praxis lifecycle

  opinions-framework:
    repo: https://github.com/jayers99/opinions-framework.git
    domain: write
    description: Research and documentation for the Praxis opinions framework
```

- `praxis examples add` launches wizard with checkboxes
- User selects which examples to clone
- Praxis clones selected repos to `$PRAXIS_HOME/examples/`

### ✅ Workspace Configuration

**Decision:** Workspace config lives at `$PRAXIS_HOME/workspace-config.yaml`.

```yaml
# ~/praxis-workspace/workspace-config.yaml
workspace:
  projects_path: ./projects # Default location for new projects

installed_extensions:
  - render-run
  - template-python-cli

installed_examples:
  - uat-praxis-code
  - opinions-framework

defaults:
  privacy: personal
  environment: env1
```

### ✅ PRAXIS_HOME Environment Variable

**Decision:** Use `PRAXIS_HOME` env var for flexibility.

```bash
export PRAXIS_HOME=~/praxis-workspace
```

- Allows projects to live anywhere (edge case, but supported)
- CLI always knows where to find extensions, config, etc.
- Simplifies path resolution throughout codebase

### ✅ template-python-cli is an Extension

**Decision:** `template-python-cli` is an extension, not an example.

- Only some users need CLI scaffolding
- Can be used as a base starting point when installed
- **Out of scope for now:** `praxis new --template cli` (revisit during Execute stage for Code domain)

### ✅ Personal Projects Git Strategy

**Decision:** User's choice — both repos and plain folders are valid.

- Code domain projects will typically be git repos
- Create/Write/Observe projects may just be folders
- Praxis doesn't enforce either approach

### ✅ Workspace vs Project Config

**Decision:** Two levels of configuration.

**Workspace level** (`$PRAXIS_HOME/workspace-config.yaml`):

```yaml
workspace:
  projects_path: ./projects
installed_extensions:
  - render-run
defaults:
  privacy: personal
  environment: env1
```

**Project level** (`project-dir/praxis.yaml`):

```yaml
domain: create
subtype: visual
privacy: personal
stage: execute
environment: env1
```

---

## Decisions (formerly Open Questions)

### ✅ How does Praxis know what extensions the user has installed?

**Decision:** Read workspace config yaml.

Parse `$PRAXIS_HOME/workspace-config.yaml` → `installed_extensions` list.

### ✅ When do extensions get updated?

**Decision:** User runs `praxis extensions update` manually.

Manual updates give predictability and control. No auto-updates.

### ✅ Extension Integration Method

**Decision:** Hybrid approach — Subprocess with loose coupling + Entry Points for tighter integration.

- **Primary:** Extensions are standalone CLI applications (subprocess calls)
- **Optional:** Entry points for extensions that want tighter Python integration
- **Benefit:** Best of both worlds — loose coupling by default, tighter integration when needed

### ✅ Extension Development & Debugging Strategy

**Decision:** Extensions are separate applications, developed and tested independently.

- Each extension lives as its own repo with its own CLI
- Can test, debug, and develop extensions in isolation
- Wire them together with Praxis later via entry points
- Extensions are useful standalone (e.g., `render-run generate --prompt "..."`)
- Praxis orchestrates but doesn't own extension logic

---

## Extension Integration Research Report

### Option 1: Python Entry Points (via `pyproject.toml`)

**How it works:**

- Extensions declare entry points in their `pyproject.toml`
- Praxis discovers them using `importlib.metadata.entry_points()`
- Extensions must be pip-installed (even if editable)

**Example extension pyproject.toml:**

```toml
[project.entry-points."praxis.extensions"]
render-run = "render_run:PraxisExtension"
```

**Example Praxis discovery code:**

```python
from importlib.metadata import entry_points

def discover_extensions():
    eps = entry_points(group='praxis.extensions')
    return {ep.name: ep.load() for ep in eps}
```

**Pros:**

- Standard Python packaging mechanism
- Well-documented, widely used (pytest, Flask, etc.)
- Extensions can be distributed via PyPI
- Automatic discovery of installed packages

**Cons:**

- Requires extensions to be pip-installed
- Slightly more ceremony for users (can't just clone and use)
- Tighter coupling (extensions become Python dependencies)

---

### Option 2: Pluggy (Plugin Protocol)

**How it works:**

- Praxis defines "hook specifications" (the contract)
- Extensions implement "hook implementations"
- Pluggy manages registration, calling order, and results

**What is Pluggy?**
Pluggy is the plugin system extracted from pytest. It powers 1400+ pytest plugins and is also used by tox, devpi, and kedro.

**Example Praxis hook spec:**

```python
import pluggy

hookspec = pluggy.HookspecMarker("praxis")

class PraxisHookSpec:
    @hookspec
    def generate_image(self, prompt: str, output_dir: Path) -> Path:
        """Generate an image from a prompt."""

    @hookspec
    def scaffold_project(self, template: str, target_dir: Path) -> None:
        """Scaffold a new project from a template."""
```

**Example extension implementation:**

```python
import pluggy

hookimpl = pluggy.HookimplMarker("praxis")

class RenderRunPlugin:
    @hookimpl
    def generate_image(self, prompt: str, output_dir: Path) -> Path:
        # actual implementation
        return self._call_imagen_api(prompt, output_dir)
```

**Praxis registration:**

```python
pm = pluggy.PluginManager("praxis")
pm.add_hookspecs(PraxisHookSpec)
pm.load_setuptools_entrypoints("praxis")  # auto-discover installed plugins

# Call hook - all implementations are invoked
results = pm.hook.generate_image(prompt="a cat", output_dir=Path("./output"))
```

**Key Pluggy Features:**

- **Hook wrappers:** Execute code before/after all hook implementations
- **Call ordering:** Control which plugins run first/last (`tryfirst`, `trylast`)
- **First result only:** Stop at first non-None result (`@hookspec(firstresult=True)`)
- **Historic hooks:** Late-registered plugins receive past calls
- **Optional validation:** Hooks can be optional or strictly enforced

**Pros:**

- Very powerful — supports wrappers, ordering, first-result-only
- Battle-tested (powers pytest's 1400+ plugins)
- Can combine with entry points for auto-discovery
- Supports multiple implementations of same hook
- Built-in tracing/debugging

**Cons:**

- Additional dependency (`pluggy`)
- More complex mental model (hookspecs, hookimpls, markers)
- May be overkill for simple extension needs
- Learning curve for extension authors

---

### Option 3: Subprocess/CLI Calls

**How it works:**

- Extensions are standalone CLI applications
- Praxis invokes them via subprocess
- Communication via stdout/stdin or temp files

**Example:**

```python
import subprocess
import json

def invoke_render_run(prompt: str, output_dir: Path) -> Path:
    result = subprocess.run(
        ["render-run", "generate", "--prompt", prompt, "--output", str(output_dir), "--json"],
        capture_output=True,
        text=True
    )
    data = json.loads(result.stdout)
    return Path(data["output_path"])
```

**Pros:**

- Loosest coupling — extensions can be any language
- No installation required (just needs to be on PATH or in extensions/)
- Extensions are fully independent applications
- Easy to test extensions in isolation
- Users can run extensions directly without Praxis

**Cons:**

- Serialization overhead (everything goes through CLI args/stdout)
- Harder to share complex objects
- Error handling is messier (parse stderr, check exit codes)
- No type safety across boundary
- Extension must implement CLI interface

---

### Option 4: Hybrid Approach

**Combine subprocess for loose coupling with optional entry points for tighter integration:**

```python
class ExtensionManager:
    def invoke(self, extension_name: str, command: str, **kwargs):
        # First, check if extension is installed as Python package
        try:
            eps = entry_points(group='praxis.extensions')
            if extension_name in [ep.name for ep in eps]:
                ext = [ep for ep in eps if ep.name == extension_name][0].load()
                return ext.invoke(command, **kwargs)
        except:
            pass

        # Fall back to subprocess
        return self._invoke_subprocess(extension_name, command, **kwargs)
```

**Pros:**

- Best of both worlds
- Extensions can choose their integration level
- Graceful fallback

**Cons:**

- More complex implementation
- Two code paths to maintain

---

### Comparison Matrix

| Criterion                | Entry Points | Pluggy    | Subprocess | Hybrid   |
| ------------------------ | ------------ | --------- | ---------- | -------- |
| Setup complexity         | Medium       | Medium    | Low        | High     |
| Runtime coupling         | Tight        | Tight     | Loose      | Variable |
| Type safety              | Yes          | Yes       | No         | Partial  |
| Multi-language           | No           | No        | Yes        | Partial  |
| Learning curve           | Low          | Medium    | Low        | Medium   |
| Debugging                | Good         | Excellent | Poor       | Mixed    |
| Extension independence   | Low          | Low       | High       | Variable |
| Multiple implementations | Manual       | Built-in  | Manual     | Variable |

---

### Recommendation

**Start with Subprocess (Option 3)** for these reasons:

1. **Matches current reality** — `render-run` already has a CLI interface
2. **Simplest for users** — Clone and use, no pip install required
3. **Extension independence** — Extensions are useful standalone
4. **Language agnostic** — Future extensions could be in any language
5. **Testable** — Easy to test extensions without Praxis

**The workflow would be:**

```bash
# User adds extension
praxis extensions add render-run
# This clones repo to $PRAXIS_HOME/extensions/render-run/

# Praxis invokes it via subprocess
praxis render --prompt "a cat in space"
# Internally: subprocess.run(["$PRAXIS_HOME/extensions/render-run/render-run", "generate", ...])
```

**Consider Entry Points or Pluggy later** if we need:

- Tighter integration (sharing Python objects)
- Multiple extensions implementing the same capability
- Hook wrappers (before/after behavior)
- Complex orchestration between extensions

---

## CLI Commands

### Workspace Management

```bash
# Initialize a new workspace (interactive wizard)
praxis workspace init
# - Creates directory structure
# - Prompts for which examples to clone
# - Prompts for which extensions to install
# - Creates praxis.yaml

# Show workspace info
praxis workspace info
```

### Extension Management

```bash
# List available and installed extensions
praxis extensions list
# Output:
#   render-run        [installed]  Create domain: AI image generation
#   template-python-cli [not installed]  Code domain: CLI scaffolding

# Add extensions (wizard with checkboxes)
praxis extensions add
# Interactive selection UI

# Add specific extension directly
praxis extensions add render-run

# Remove an extension
praxis extensions remove render-run

# Update all extensions (future)
praxis extensions update
```

### Example Management

```bash
# List available examples
praxis examples list

# Add an example to workspace
praxis examples add uat-praxis-code
```

---

## Implementation Details

### ✅ PRAXIS_HOME Not Set Behavior

**Decision:** Error with helpful message.

```
Error: PRAXIS_HOME environment variable is not set.

Set it to your workspace root:
  export PRAXIS_HOME=~/praxis-workspace

Or run 'praxis workspace init' to create a new workspace.
```

### ✅ What `praxis workspace init` Does

**Decision:** Assumes praxis-ai already cloned; creates sibling directories.

```bash
praxis workspace init
# 1. Determines workspace location (PRAXIS_HOME if set, otherwise asks)
# 2. Creates directory structure: extensions/, examples/, projects/
# 3. Creates workspace-config.yaml with defaults
# 4. Prompts: "Which extensions do you want?" (checkboxes)
# 5. Prompts: "Which examples do you want?" (checkboxes)
# 6. Clones selected repos to appropriate directories
```

User must have already cloned `praxis-ai` — init doesn't do that.

### ✅ Where `praxis workspace init` Runs From

**Decision:** Use PRAXIS_HOME if set, otherwise ask user.

```python
if os.environ.get("PRAXIS_HOME"):
    workspace_path = Path(os.environ["PRAXIS_HOME"])
else:
    workspace_path = questionary.path(
        "Where should the workspace be created?",
        default="~/praxis-workspace"
    ).ask()
```

### ✅ Interactive Wizard vs Flags

**Decision:** Both supported. Interactive by default, flags for scripting.

```bash
# Interactive (default)
praxis extensions add
# Shows checkbox UI

# Direct (scripting/CI)
praxis extensions add render-run
praxis extensions add render-run template-python-cli
```

### ✅ Interactive Prompt Library

**Decision:** Use `questionary` for clean checkbox UI.

Add to dependencies:

```toml
[tool.poetry.dependencies]
questionary = "^2.0.0"
```

### ✅ Clone Failure Handling

**Decision:** Skip with warning, continue with others.

```
⚠ Failed to clone render-run: Connection refused
✓ Cloned template-python-cli
✓ Cloned uat-praxis-code

Workspace initialized with 2 of 3 requested items.
Run 'praxis extensions add render-run' to retry.
```

### ✅ Exit Codes (Unix Compliance)

**Decision:** Follow standard exit code conventions per `cli.md`.

| Code | Meaning             | When                                                   |
| ---- | ------------------- | ------------------------------------------------------ |
| 0    | Success             | Operation completed successfully                       |
| 1    | General error       | Unexpected failure, invalid state                      |
| 2    | Usage error         | Invalid arguments, missing required options            |
| 3    | Configuration error | Invalid YAML, missing config file, PRAXIS_HOME not set |
| 4    | External error      | Clone failed, network error, extension not found       |

### ✅ Output Behavior (Unix Compliance)

**Decision:** Separate stdout (data) from stderr (status), support scripting modes.

**Standard behavior:**

- **stdout:** Machine-readable data (JSON when `--json` flag)
- **stderr:** Human-readable status messages, progress, errors

**Flags supported:**

```bash
--quiet, -q     # Suppress progress/status messages (stderr)
--json          # Output data as JSON (stdout)
```

**Examples:**

```bash
# Human mode (default)
praxis extensions list
# stderr: "Fetching extension registry..."
# stdout: Pretty table of extensions

# Script mode
praxis extensions list --json --quiet
# stderr: (nothing)
# stdout: {"extensions": [{"name": "render-run", ...}]}

# Piping (only stdout goes through)
praxis extensions list --json | jq '.extensions[].name'
```

---

## Migration Plan

### Phase 1: Update praxis-ai repo structure

1. [ ] Create `extensions.yaml` registry file
2. [ ] Create `examples.yaml` registry file
3. [ ] Remove all project submodules (`xmas-cards-2025`, `bowerbird`, `render-run`, `template-python-cli`, `uat-praxis-code`)
4. [ ] Remove `projects/write/opinions-framework/` directory (now a separate repo)
5. [ ] Delete `projects/` directory from praxis-ai
6. [ ] Update README with new workspace model

### Phase 2: Implement workspace commands

1. [ ] Add `questionary` dependency
2. [ ] Implement `praxis workspace init`
3. [ ] Implement `praxis extensions list/add/remove/update`
4. [ ] Implement `praxis examples list/add`
5. [ ] Add PRAXIS_HOME support to CLI
6. [ ] Add BDD tests for new commands (see test scenarios below)

### Phase 3: Update documentation

1. [ ] Create workspace setup guide
2. [ ] Update user-guide.md
3. [ ] Create ADR for workspace structure decision

---

## Architecture: New Code Locations

Per `cli-python.md`, new code follows hexagonal architecture:

```text
src/praxis/
├── domain/
│   └── workspace.py              # Workspace, Extension, Example entities
│
├── application/
│   ├── workspace_service.py      # Workspace init, info orchestration
│   └── extension_service.py      # Extension add/remove/list/update logic
│
├── infrastructure/
│   ├── git_cloner.py             # Git clone/pull operations
│   ├── registry_loader.py        # Load extensions.yaml, examples.yaml
│   └── workspace_config_repo.py  # Read/write workspace-config.yaml
│
└── cli/
    ├── workspace_commands.py     # Typer commands for workspace
    └── extension_commands.py     # Typer commands for extensions
```

**Registry files (in praxis-ai root):**

- `extensions.yaml` — Available extensions registry
- `examples.yaml` — Available examples registry

---

## BDD Test Scenarios

Per `cli-python.md`, all features need BDD tests with Gherkin syntax.

**File:** `tests/features/workspace.feature`

```gherkin
Feature: Workspace Management
  As a Praxis user
  I want to initialize and manage my workspace
  So that I can organize my extensions, examples, and projects

  Scenario: Initialize workspace with PRAXIS_HOME set
    Given PRAXIS_HOME is set to "/tmp/test-workspace"
    And the praxis-ai repo exists at "/tmp/test-workspace/praxis-ai"
    When I run "praxis workspace init" with no interactive input
    Then the exit code should be 0
    And the directory "/tmp/test-workspace/extensions" should exist
    And the directory "/tmp/test-workspace/examples" should exist
    And the directory "/tmp/test-workspace/projects" should exist
    And the file "/tmp/test-workspace/workspace-config.yaml" should exist

  Scenario: Workspace init fails without PRAXIS_HOME
    Given PRAXIS_HOME is not set
    When I run "praxis workspace init" non-interactively
    Then the exit code should be 3
    And stderr should contain "PRAXIS_HOME environment variable is not set"

  Scenario: Show workspace info
    Given a valid workspace at PRAXIS_HOME
    And extension "render-run" is installed
    When I run "praxis workspace info --json"
    Then the exit code should be 0
    And stdout should be valid JSON
    And the JSON should contain "installed_extensions"
```

**File:** `tests/features/extensions.feature`

```gherkin
Feature: Extension Management
  As a Praxis user
  I want to manage extensions
  So that I can add capabilities to my workflow

  Scenario: List available extensions
    Given a valid workspace at PRAXIS_HOME
    When I run "praxis extensions list --json"
    Then the exit code should be 0
    And stdout should contain "render-run"
    And stdout should contain "template-python-cli"

  Scenario: Add extension by name
    Given a valid workspace at PRAXIS_HOME
    And extension "render-run" is not installed
    When I run "praxis extensions add render-run"
    Then the exit code should be 0
    And the directory "$PRAXIS_HOME/extensions/render-run" should exist
    And "render-run" should be in workspace-config.yaml installed_extensions

  Scenario: Add non-existent extension
    Given a valid workspace at PRAXIS_HOME
    When I run "praxis extensions add nonexistent-extension"
    Then the exit code should be 4
    And stderr should contain "Extension 'nonexistent-extension' not found"

  Scenario: Remove installed extension
    Given a valid workspace at PRAXIS_HOME
    And extension "render-run" is installed
    When I run "praxis extensions remove render-run"
    Then the exit code should be 0
    And the directory "$PRAXIS_HOME/extensions/render-run" should not exist
    And "render-run" should not be in workspace-config.yaml installed_extensions
```

---

## Ready for Implementation

All decisions finalized. Document is ready to be used as implementation spec.
