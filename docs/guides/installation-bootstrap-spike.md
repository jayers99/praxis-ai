# Spike: How Does a User Install and Bootstrap Praxis?

**Status:** Draft  
**Date:** 2026-01-05  
**Related Issues:** #4 (template-python-cli), #13 (Opinionated starter packs), #14 (Domain creation mode)

---

## Executive Summary

This spike documents the ideal user journey from "I want to use Praxis" to "I have a governed project," evaluates packaging/distribution approaches, and recommends a minimum viable implementation.

**Key Recommendation:** Start with **PyPI package distribution** (`pip install praxis-ai`) combined with a guided bootstrap flow that supports both technical and non-technical users.

---

## 1. User Journeys

### 1A. Technical User (Developer)

**Goal:** Get Praxis running quickly, integrate with existing dev workflow

**Journey:**
```bash
# Installation
pipx install praxis-ai          # or: pip install praxis-ai

# Configure workspace (one-time)
export PRAXIS_HOME="$HOME/praxis-workspace"
praxis workspace init

# Create first project
praxis new my-cli-tool --domain code --privacy personal
cd $PRAXIS_HOME/projects/code/my-cli-tool

# Work through lifecycle
praxis status                   # See current state and next steps
praxis stage sense              # Progress through stages
praxis validate                 # Check governance compliance
```

**Expectations:**
- Command-line familiarity
- Comfortable with environment variables
- Wants automation and scriptability
- Expects JSON output options for tooling integration

**Pain Points to Avoid:**
- Complex installation procedures
- Manual file creation/copying
- Unclear next steps after installation
- Missing workspace configuration

### 1B. Non-Technical User (Writer, Creator, Learner)

**Goal:** Use Praxis for structured thinking without deep CLI knowledge

**Journey:**
```bash
# Installation (guided by web docs or tutorial)
pip install praxis-ai

# Interactive setup (prompts for everything)
praxis workspace init
# → Where should workspace be created? [~/praxis-workspace]
# → Default privacy level? [personal]
# → Default environment? [Home]

# Create project with prompts
praxis new my-article
# → Domain? [write]
# → Privacy level? [personal]
# → Location? [~/praxis-workspace/projects/write]

cd ~/praxis-workspace/projects/write/my-article

# Work with guidance
praxis status                   # Shows what to do next
# → Next Steps:
#     + Create docs/capture.md (Capture document)
#     ▶ Run `praxis stage sense` (Advance to Sense stage)
```

**Expectations:**
- Clear, human-readable prompts
- Sensible defaults
- Helpful error messages
- Visual progress indicators

**Pain Points to Avoid:**
- Required flags without defaults
- Unclear error messages
- Cryptic technical jargon
- Missing intermediate steps

---

## 2. Installation Methods Evaluation

| Method | Pros | Cons | Recommendation |
|--------|------|------|----------------|
| **pip install praxis-ai** | Standard Python workflow, version management, dependency handling | Requires PyPI package setup, name availability | ✅ **Primary method** |
| **pipx install praxis-ai** | Isolated CLI tool, no env conflicts | User must install pipx first | ✅ **Recommended for CLI-only usage** |
| **curl \| bash script** | Zero-step install | Security concerns, platform-specific, hard to maintain | ❌ Not recommended |
| **gh repo clone** | No packaging needed, includes examples | Manual, requires git knowledge, no version management | ⚠️ Developer-only fallback |
| **copier/cookiecutter** | Template-focused | External dependency, adds complexity | ⚠️ Future enhancement for starter packs |
| **npx-style runner** | No install needed | Requires npm ecosystem, wrong tool for Python | ❌ Not applicable |

### Recommended Approach

**Primary:** PyPI package distribution
```bash
# Global install
pip install praxis-ai

# Isolated install (recommended)
pipx install praxis-ai

# Verify
praxis --version
```

**Developer Fallback:** Git clone + editable install
```bash
git clone https://github.com/jayers99/praxis-ai.git
cd praxis-ai
poetry install
poetry run praxis --version
```

---

## 3. Bootstrap Flow

### 3.1 Current State

Praxis currently has three initialization commands:

1. **`praxis workspace init`** - Creates workspace structure
   - Creates: `extensions/`, `examples/`, `projects/`, `workspace-config.yaml`
   - Location: `$PRAXIS_HOME` or prompted
   - Stores defaults: privacy, environment

2. **`praxis new <name>`** - Creates new project with governance
   - Creates project directory under workspace (if configured)
   - Generates: `praxis.yaml`, `CLAUDE.md`, `docs/capture.md`
   - Prompts for: domain, privacy, environment if not provided
   - Optional: subtype for specialized guidance

3. **`praxis init`** - Initializes existing directory
   - Similar to `new` but doesn't create parent directory
   - For adding Praxis to existing projects

### 3.2 Ideal Bootstrap Flow

```
┌─────────────────────────────────────────────────────────────┐
│ User runs: praxis workspace init                            │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ Workspace Setup                                             │
│ - Prompt for PRAXIS_HOME location (default: ~/praxis)      │
│ - Prompt for default privacy (default: personal)            │
│ - Prompt for default environment (default: Home)            │
│ - Create directory structure                                │
│ - Generate workspace-config.yaml                            │
│ - Show next steps message                                   │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ First Project Creation                                      │
│ User runs: praxis new my-first-project                      │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ Project Setup                                               │
│ - Prompt for domain (code/create/write/learn/observe)      │
│ - Prompt for subtype (optional, domain-specific)            │
│ - Use workspace defaults for privacy/environment            │
│ - Create project at $PRAXIS_HOME/projects/<domain>/<name>  │
│ - Generate praxis.yaml                                      │
│ - Generate CLAUDE.md (AI assistant instructions)           │
│ - Generate docs/capture.md (initial stage doc)             │
│ - Show next steps                                           │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ User enters project and runs: praxis status                │
│ → Shows current state, validation, next steps              │
│ → Guides user through lifecycle stages                     │
└─────────────────────────────────────────────────────────────┘
```

### 3.3 Enhanced Bootstrap: First-Run Experience

**Proposal:** Detect first run and offer guided setup

```bash
# User's first command (workspace doesn't exist)
$ praxis new my-project

⚠ PRAXIS_HOME not configured. Let's set up your workspace first.

Where should Praxis store your projects? [~/praxis-workspace]
> 

Default privacy level for new projects? [personal]
> 

Default environment? [Home]
> 

✓ Workspace initialized at ~/praxis-workspace
  Created: extensions/
  Created: examples/
  Created: projects/
  Created: workspace-config.yaml

ℹ Add to your shell config (~/.bashrc or ~/.zshrc):
  export PRAXIS_HOME="$HOME/praxis-workspace"

Now creating project: my-project
Domain? [code]
> 
```

This eliminates the need to run `workspace init` separately while preserving the explicit command for advanced users.

---

## 4. Template Selection

### 4.1 Current Capabilities

Praxis already has:
- **Stage templates** (`praxis templates render`) - Lifecycle documentation
- **Domain-specific artifacts** - SOD, brief, plan based on domain
- **Subtype opinions** - Additional guidance for subtypes (cli, api, library, etc.)

### 4.2 Template vs Starter Pack vs Opinion

| Concept | Purpose | Example |
|---------|---------|---------|
| **Template** | Scaffold lifecycle docs for a stage | `docs/capture.md`, `docs/sod.md` |
| **Starter Pack** | Pre-configured project with code/structure | `template-python-cli` (Issue #4) |
| **Opinion** | Advisory guidance for quality/practices | `opinions/code/cli/` |

### 4.3 Recommendations

**Option A: Keep Bootstrap Simple, Templates Separate**
```bash
# Bootstrap creates minimal structure
praxis new my-cli --domain code --subtype cli

# User explicitly requests templates/examples
praxis templates render          # Add lifecycle docs
praxis examples add python-cli   # Copy starter code
```

**Option B: Offer Templates During Bootstrap (Interactive)**
```bash
praxis new my-cli --domain code

Domain? [code]
> code

Subtype? (cli, library, api, webapp, script) [leave empty to skip]
> cli

Would you like to scaffold with a starter template?
  1. Minimal (praxis.yaml + CLAUDE.md only)
  2. Python CLI template (full project structure)
  3. Browse available templates
> 1
```

**Recommended:** **Option A** for MVP
- Keeps bootstrap focused and predictable
- Templates are opt-in via separate commands
- Aligns with current architecture
- Prevents decision paralysis for new users

**Future Enhancement:** Option B can be added later when starter pack ecosystem is mature (Issue #13).

---

## 5. Minimum Viable Bootstrap

### 5.1 What Currently Works

✅ **Already Implemented:**
- `praxis workspace init` - Creates workspace structure
- `praxis new <name>` - Creates governed project
- Interactive prompts for required fields
- Workspace-aware defaults
- JSON output for automation
- Stage progression with `praxis stage`
- Validation with `praxis validate`
- Status checking with `praxis status`

### 5.2 Gaps and Enhancements Needed

❌ **Missing for Smooth Bootstrap:**

1. **PyPI Package**
   - Not yet published to PyPI
   - Installation requires git clone + poetry
   - Version management not available

2. **First-Run Detection**
   - No automatic workspace setup prompt
   - Users must know to run `workspace init` first
   - Could detect missing `PRAXIS_HOME` and offer help

3. **Installation Documentation**
   - README has manual install instructions
   - No dedicated installation guide
   - Missing platform-specific guidance

4. **Post-Install Verification**
   - No built-in health check
   - Could add `praxis doctor` command to verify setup

### 5.3 Minimum Viable Implementation

**Phase 1: Package Distribution** (Prerequisite)
- [ ] Register `praxis-ai` on PyPI (or `praxis-framework`, check availability)
- [ ] Configure `pyproject.toml` for PyPI release
- [ ] Test installation: `pip install praxis-ai`
- [ ] Verify CLI availability: `praxis --version`

**Phase 2: Enhanced Bootstrap Experience**
- [ ] First-run detection in `praxis new` command
- [ ] Auto-prompt for workspace setup if missing
- [ ] Improve error messages when `PRAXIS_HOME` not set
- [ ] Add success messages with next steps

**Phase 3: Documentation**
- [ ] Create `docs/guides/installation.md` (detailed install guide)
- [ ] Update README.md with simple install flow
- [ ] Add quickstart examples
- [ ] Document troubleshooting

**Phase 4: Verification Tools**
- [ ] Add `praxis doctor` command to check setup
- [ ] Verify: Python version, PRAXIS_HOME, workspace structure
- [ ] Check for common issues (permissions, paths)

---

## 6. AI Integration

### 6.1 Current State

Praxis already generates `CLAUDE.md` at project creation:
- Contains project context (domain, stage, privacy)
- References applicable opinions
- Provides AI assistant instructions

### 6.2 Detection and Auto-Configuration

**Possible Enhancements:**

1. **Detect AI Tools**
   ```bash
   # During bootstrap, check for:
   - .claude/settings.local.json (Claude Code)
   - .cursor/ (Cursor)
   - .vscode/settings.json (GitHub Copilot)
   ```

2. **Offer Configuration**
   ```bash
   praxis new my-project
   
   ✓ Project created
   ℹ Detected: Claude Code
   
   Would you like to configure Claude Code for this project? [y/N]
   > y
   
   ✓ Updated .claude/settings.local.json with Praxis context
   ```

3. **Generate Tool-Specific Instructions**
   - `CLAUDE.md` for Claude/Claude Code
   - `.cursorrules` for Cursor
   - `.github/copilot-instructions.md` for GitHub Copilot

**Recommendation:** **Defer to Post-MVP**
- Current `CLAUDE.md` generation is sufficient
- AI tool landscape is evolving rapidly
- Focus on core bootstrap first
- Can add as enhancement once installation is stable

### 6.3 AI Context Commands (Already Implemented)

Praxis already has excellent AI integration via:
```bash
praxis opinions --prompt        # AI-ready opinion context
praxis context                  # Generate context bundle
praxis status                   # Shows next steps for AI
```

These provide everything AI assistants need without tool-specific configuration.

---

## 7. Comparison with Related Issues

### Issue #4: template-python-cli
**Purpose:** Worked example of Python CLI with full project structure

**Relationship to Bootstrap:**
- Starter pack, not bootstrap mechanism
- Shows "what a complete project looks like"
- Can be installed via `praxis examples add`
- Bootstrap creates minimal structure; starter packs add opinionated scaffolding

**Recommendation:** Keep separate. Bootstrap remains minimal, templates are opt-in.

### Issue #13: Opinionated Starter Packs
**Purpose:** Registry of reusable project templates

**Relationship to Bootstrap:**
- Extensions to the base bootstrap
- Requires `praxis extensions add <starter-pack>`
- Builds on minimal bootstrap foundation
- May integrate with `praxis new --template` in future

**Recommendation:** Bootstrap creates foundation, starter packs add structure.

### Issue #14: Domain Creation Mode
**Purpose:** Help users choose the right domain for their project

**Relationship to Bootstrap:**
- Interactive guidance during `praxis new`
- Could enhance bootstrap flow with questionnaire
- "What are you trying to do?" → Suggests domain

**Recommendation:** Good future enhancement for non-technical users.

**Possible Flow:**
```bash
praxis new my-project --guided

What are you creating?
  1. Software tool or application
  2. Visual or creative work
  3. Written document
  4. Learning material or notes
  5. Research or observation capture
> 3

Suggested domain: write
Suggested subtype: technical

Looks good? [Y/n]
```

---

## 8. Recommendations

### 8.1 Immediate Actions (MVP Bootstrap)

1. **Publish to PyPI**
   - Register `praxis-ai` package name
   - Configure release workflow
   - Enable `pip install praxis-ai`

2. **Create Installation Guide**
   - `docs/guides/installation.md` with step-by-step instructions
   - Platform-specific notes (macOS, Linux, Windows WSL)
   - Troubleshooting section

3. **Enhance Bootstrap UX**
   - Auto-detect missing workspace on first run
   - Offer to create workspace during `praxis new`
   - Improve success messages with clear next steps

4. **Add Health Check**
   - `praxis doctor` command
   - Verifies: Python version, PRAXIS_HOME, workspace structure
   - Suggests fixes for common issues

### 8.2 Future Enhancements (Post-MVP)

5. **Guided Domain Selection** (Issue #14)
   - `--guided` flag for interactive domain questionnaire
   - Helps non-technical users choose domain

6. **Template Integration** (Issue #13)
   - `praxis new --template python-cli`
   - Starter pack selection during bootstrap
   - Interactive picker if multiple templates available

7. **AI Tool Integration**
   - Auto-detect AI tools (Claude Code, Cursor, Copilot)
   - Offer to configure tool-specific files
   - Generate appropriate instruction files

8. **Shell Integration**
   - `praxis --install-completion` (already exists)
   - Shell alias suggestions
   - Environment variable setup helper

### 8.3 Documentation Priorities

**High Priority:**
1. `docs/guides/installation.md` - Comprehensive install guide
2. `README.md` - Updated with simple install flow
3. `docs/guides/quickstart.md` - 5-minute tutorial

**Medium Priority:**
4. `docs/guides/troubleshooting.md` - Common issues and fixes
5. Platform-specific guides (Windows, Docker, etc.)

**Low Priority:**
6. Video walkthrough
7. Interactive web-based tutorial

---

## 9. Proof of Concept

### 9.1 Installation Flow (PyPI)

**Current Reality (Manual):**
```bash
git clone https://github.com/jayers99/praxis-ai.git
cd praxis-ai
poetry install
export PRAXIS_HOME="$HOME/praxis-workspace"
poetry run praxis workspace init
poetry run praxis new my-project --domain code --privacy personal
cd $PRAXIS_HOME/projects/code/my-project
poetry run praxis status
```

**Proposed Future (PyPI):**
```bash
pipx install praxis-ai
export PRAXIS_HOME="$HOME/praxis-workspace"
praxis workspace init
praxis new my-project --domain code --privacy personal
cd $PRAXIS_HOME/projects/code/my-project
praxis status
```

**Future Enhanced (Auto-Workspace):**
```bash
pipx install praxis-ai
export PRAXIS_HOME="$HOME/praxis-workspace"
praxis new my-project --domain code --privacy personal
# → Detects missing workspace, prompts to create
# → Creates project
# → Shows next steps
cd $PRAXIS_HOME/projects/code/my-project
praxis status
```

### 9.2 Command Enhancement Examples

**Enhanced `praxis new` with first-run detection:**
```python
def new_cmd(...):
    workspace_path = get_praxis_home()
    
    if workspace_path is None or not workspace_path.exists():
        if json_output or quiet:
            typer.echo("Error: PRAXIS_HOME not set. Run 'praxis workspace init' first.", err=True)
            raise typer.Exit(3)
        
        # Interactive mode: offer to create workspace
        typer.echo("⚠ Workspace not found. Let's set one up first.\n")
        
        if typer.confirm("Create workspace now?", default=True):
            # Inline workspace creation
            workspace_result = init_workspace(...)
            if not workspace_result.success:
                for err in workspace_result.errors:
                    typer.echo(f"✗ {err}", err=True)
                raise typer.Exit(1)
            
            typer.echo("\n✓ Workspace created. Now creating your project...\n")
        else:
            typer.echo("Run 'praxis workspace init' when ready.")
            raise typer.Exit(0)
    
    # Continue with project creation...
```

**New `praxis doctor` command:**
```python
@app.command(name="doctor")
def doctor_cmd():
    """Check Praxis installation and configuration."""
    
    checks = []
    
    # Check Python version
    import sys
    py_version = sys.version_info
    if py_version >= (3, 10):
        checks.append(("✓", "Python version", f"{py_version.major}.{py_version.minor}"))
    else:
        checks.append(("✗", "Python version", f"{py_version.major}.{py_version.minor} (need 3.10+)"))
    
    # Check PRAXIS_HOME
    praxis_home = os.environ.get("PRAXIS_HOME")
    if praxis_home:
        checks.append(("✓", "PRAXIS_HOME", praxis_home))
    else:
        checks.append(("⚠", "PRAXIS_HOME", "not set (workspace features disabled)"))
    
    # Check workspace structure
    if praxis_home and Path(praxis_home).exists():
        workspace_config = Path(praxis_home) / "workspace-config.yaml"
        if workspace_config.exists():
            checks.append(("✓", "Workspace", "configured"))
        else:
            checks.append(("⚠", "Workspace", "directory exists but not initialized"))
    elif praxis_home:
        checks.append(("✗", "Workspace", "directory not found"))
    
    # Display results
    typer.echo("Praxis Health Check\n")
    for icon, check, status in checks:
        typer.echo(f"  {icon} {check:20} {status}")
    
    # Show fixes if needed
    has_errors = any(icon == "✗" for icon, _, _ in checks)
    if has_errors:
        typer.echo("\nRecommended fixes:")
        if not praxis_home:
            typer.echo("  export PRAXIS_HOME=\"$HOME/praxis-workspace\"")
            typer.echo("  praxis workspace init")
```

---

## 10. Success Metrics

### Definition of "User Can Bootstrap Praxis"

A user has successfully bootstrapped Praxis when they can:

1. ✅ Install Praxis CLI with a single command
2. ✅ Create a workspace
3. ✅ Create a new governed project
4. ✅ See their current status and next steps
5. ✅ Progress through lifecycle stages
6. ✅ Validate their project configuration

### Measurement

**Quantitative:**
- Install time: < 2 minutes (including dependency download)
- Bootstrap time: < 5 minutes (first workspace + project)
- Commands to first working project: ≤ 5

**Qualitative:**
- User understands what Praxis is doing at each step
- Error messages are actionable
- Success messages show clear next steps
- Documentation is discoverable and complete

---

## 11. Next Steps

### Immediate (This Sprint)
- [ ] Complete this spike document
- [ ] Review with team/maintainer
- [ ] Decide on package name (praxis-ai vs praxis-framework)
- [ ] Create installation guide draft

### Short-Term (Next Sprint)
- [ ] Configure PyPI release workflow
- [ ] Publish first PyPI release
- [ ] Update README with simple install instructions
- [ ] Add `praxis doctor` command

### Medium-Term
- [ ] Implement first-run workspace detection
- [ ] Create quickstart guide
- [ ] Add troubleshooting documentation
- [ ] Gather user feedback on bootstrap experience

### Long-Term
- [ ] Guided domain selection (Issue #14)
- [ ] Starter pack integration (Issue #13)
- [ ] AI tool auto-configuration
- [ ] Web-based interactive tutorial

---

## 12. Open Questions

1. **Package Name:** `praxis-ai` vs `praxis-framework` vs `praxis`?
   - **Recommendation:** `praxis-ai` (matches repo name, indicates AI integration focus)

2. **Should `praxis new` auto-create workspace?**
   - **Recommendation:** Yes, in interactive mode with confirmation
   - Automation modes (--json, --quiet) should fail with clear error

3. **Where should workspace default to?**
   - Current: `$PRAXIS_HOME` or prompt
   - **Recommendation:** Keep current behavior, suggest `~/praxis-workspace` as default

4. **Should we version-lock Python ≥ 3.10?**
   - Current: `python = ">=3.10"` in pyproject.toml
   - **Recommendation:** Yes, maintain this requirement (typing features needed)

5. **How to handle existing projects?**
   - Use `praxis init` to add governance to existing directories
   - **Recommendation:** Document this clearly in migration guide

---

## Appendices

### A. Current Command Matrix

| Command | Purpose | Automation Support | Interactive Prompts |
|---------|---------|-------------------|---------------------|
| `praxis workspace init` | Create workspace | ✅ --json, --quiet | ✅ Path, defaults |
| `praxis new <name>` | Create project | ✅ --json, --quiet | ✅ Domain, privacy, location |
| `praxis init` | Initialize existing dir | ✅ --json, --quiet | ✅ Domain, privacy |
| `praxis status` | Show current state | ✅ --json | N/A |
| `praxis stage <stage>` | Transition stage | ✅ --json, --quiet | ⚠️ Only for warnings |
| `praxis validate` | Check governance | ✅ --json | N/A |
| `praxis templates render` | Scaffold docs | ✅ --json, --quiet | N/A |

### B. File Structure Created by Bootstrap

**Workspace (`$PRAXIS_HOME/`):**
```
praxis-workspace/
├── extensions/              # Installed extensions
├── examples/                # Installed examples
├── projects/                # User projects (by domain)
│   ├── code/
│   ├── create/
│   ├── write/
│   ├── learn/
│   └── observe/
└── workspace-config.yaml    # Workspace configuration
```

**Project (`$PRAXIS_HOME/projects/<domain>/<name>/`):**
```
my-project/
├── praxis.yaml              # Project governance config
├── CLAUDE.md                # AI assistant instructions
└── docs/
    └── capture.md           # Initial stage document
```

### C. Sample `workspace-config.yaml`

```yaml
defaults:
  privacy: personal
  environment: Home
installed_extensions: []
installed_examples: []
```

### D. Sample `praxis.yaml` (Code domain)

```yaml
domain: code
stage: capture
privacy_level: personal
environment: Home
subtype: cli  # Optional
```

### E. Sample `CLAUDE.md` Template

```markdown
# Praxis Project Context

## Project Configuration

- **Domain:** code
- **Stage:** capture
- **Privacy:** personal
- **Environment:** Home

## Governance

This project is governed by Praxis lifecycle stages. Current stage: **Capture**.

### Current Stage: Capture
Collect raw inputs without judgment. The goal is to gather ideas, requirements, and context.

### Next Stage: Sense
Synthesize meaning from captured material. Look for patterns, themes, and structure.

## Applicable Opinions

See `praxis opinions --prompt` for full context.

## Commands

```bash
praxis status              # Current state and next steps
praxis stage sense         # Progress to next stage
praxis validate            # Check governance compliance
praxis opinions --prompt   # Get applicable opinions for AI
```

## Lifecycle Reference

1. Capture → 2. Sense → 3. Explore → 4. Shape → 5. Formalize → 6. Commit → 7. Execute → 8. Sustain → 9. Close

**Critical:** Formalize is a hard boundary. No execution without formalization artifacts (SOD for code domain).
```

---

## Conclusion

Praxis currently has a solid foundation for project governance but needs PyPI distribution and enhanced bootstrap UX to be accessible to users outside the development team.

**The path forward:**
1. Publish to PyPI (`pip install praxis-ai`)
2. Add first-run workspace detection
3. Create comprehensive installation documentation
4. Add health check command (`praxis doctor`)

This will enable both technical and non-technical users to go from "I want to use Praxis" to "I have a governed project" in under 5 minutes.

The existing commands (`workspace init`, `new`, `init`) already provide the necessary functionality—we just need to package it properly and guide users through the process.
