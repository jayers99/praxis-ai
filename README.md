# Praxis-AI

## The Problem

AI amplifies throughput, not coherence. You can now generate 10x faster—but you can't govern 10x faster. The bottleneck moved from production to intent-maintenance.

Without structure, AI collaboration becomes chasing your own tail at higher speed: rediscovering rejected ideas, drifting scope mid-stream, refining things that aren't defined yet.

## What Praxis Does

Praxis makes human intent durable enough to survive AI's speed.

Your capacity for intent-maintenance is fixed. AI volume is not. Praxis provides leverage—canonical decisions, explicit scope boundaries, and stage gates that let fixed human intent govern unbounded AI output.

---

Praxis is a governance framework for AI-assisted work—moving ideas through a structured lifecycle into durable, governed outcomes.

Behavior is resolved deterministically by:

```text
Domain + Stage + Privacy + Environment → Behavior
```

This repo contains the core framework. Examples and extensions are separate repos managed through `praxis examples add` and `praxis extensions add`.

Praxis also includes the **Praxis Knowledge Distillation Pipeline (PKDP)**: a risk-tiered pipeline for turning raw inputs into validated, decision-grade knowledge artifacts.

## Philosophy

### Principles Guide — Contracts Bind — Formalize Arbitrates

No single artifact has universal authority.

- **Principles** are timeless and advisory; they bias decisions but are never enforced mechanically.
- **Formalization contracts** are context-specific and binding; they enable execution by freezing selected decisions.
- **Execution** is irreversible or costly to reverse; it must operate within the active contract.

Tension between principles and execution is intentional and necessary. Formalize is the explicit decision hinge where tradeoffs are made visible.

### The Three-Layer Model

Praxis separates what you believe from how you decide from how you execute.

```text
Opinions  →  Governance  →  Execution
```

- **Opinions:** Domain-specific guidance that biases decisions. Advisory, never enforced mechanically. Organized by domain, stage, and subtype with inheritance from general to specific.
- **Governance:** The mechanism by which conflicts are resolved. Procedural authority.
- **Execution:** The work itself. Governed by formalization contracts.

This separation prevents principles from becoming dogma, governance from collapsing into bureaucracy, and execution from drifting without intent.

Opinions are stored in `opinions/` and resolved through inheritance:

```text
_shared → domain/principles → domain/{stage} → subtype/principles → subtype/{stage}
```

### Formalize is the Structural Hinge

Formalize converts intent into a bounded, executable plan with explicit constraints, so work can proceed without inventing requirements.

At Formalize, the question is:

> "Given our principles, what constraints must we now accept to make progress?"

Formalize exists to reduce ambiguity, freeze selected decisions, and enable safe execution. It is not bureaucracy; it is intentional commitment.

**Formalize also marks where the nature of iteration changes:**

- **Before Formalize (Discovery):** Iteration reshapes _what_ you're building. Cheap to change. Safe to abandon.
- **After Formalize (Refinement):** Iteration improves _how well_ you're building it. Scope is locked. Changes are costly.

Recognizing which mode you're in prevents wasted effort (polishing undefined things) and expensive rework (discovering scope mid-execution).

### Privacy is a Real Constraint

Privacy defines how information may be stored, shared, processed, and externalized. It is not a domain or stage—it is an overlay that constrains artifacts, tooling, collaboration, and AI usage.

- Declared at project inception
- Enforceable through deterministic rules
- Reclassifiable mid-project with explicit migration steps

Higher privacy requires greater abstraction and tighter controls.

### Sustain is Active Governance

Sustain is not a holding pattern—it's active governance of living work.

The question in Sustain: Does this change alter the contract I formalized, or does it extend/refine the implementation of that contract?

- **Contract change** → New iteration
- **Implementation extension** → Sustain

## What Praxis Optimizes For

AI-assisted creation is fast, but it’s easy to lose what actually worked.

Praxis treats your work as a lightweight “memory engine”:

- Capture what you tried (prompts, constraints, artifacts, decisions)
- Keep what reliably produces the outcome you want
- Cut what doesn’t
- Make the workflow reusable across future projects in the same domain

## Start Here

If you're new to Praxis:

- [docs/guides/user-guide.md](docs/guides/user-guide.md) — step-by-step walkthrough with examples
- [docs/guides/ai-setup.md](docs/guides/ai-setup.md) — configure AI assistants (CLAUDE.md, .cursorrules)
- [docs/guides/stage-templates.md](docs/guides/stage-templates.md) — scaffold stage docs with deterministic templates
- [SECURITY.md](SECURITY.md) — how to report security vulnerabilities

If you want to understand the framework:

- [core/spec/sod.md](core/spec/sod.md) — main specification
- [core/spec/lifecycle.md](core/spec/lifecycle.md) — stage definitions + regressions
- [core/spec/domains.md](core/spec/domains.md) — domain → artifact types
- [core/spec/privacy.md](core/spec/privacy.md) — privacy levels + enforcement intent
- [core/governance/opinions-contract.md](core/governance/opinions-contract.md) — opinions framework specification
- [core/spec/external-constraints.md](core/spec/external-constraints.md) — environmental authority
- [core/ai/ai-guards.md](core/ai/ai-guards.md) — AI behavior governance (draft)

If you want to distill knowledge into durable research artifacts:

- [docs/guides/pkdp.md](docs/guides/pkdp.md) — Praxis Knowledge Distillation Pipeline (PKDP)

If you want to see Praxis applied in real projects:

```bash
# Install examples to your workspace
praxis examples add uat-praxis-code      # Hello-world CLI with full lifecycle docs
praxis examples add opinions-framework   # Opinions framework research (Write domain)

# Install extensions
praxis extensions add template-python-cli  # Production CLI template (Code domain)
praxis extensions add render-run           # AI image generation (Create domain)
```

## How Praxis Works (Short Version)

### Lifecycle

All work progresses through nine stages:

1. Capture
2. Sense
3. Explore
4. Shape
5. Formalize
6. Commit
7. Execute
8. Sustain
9. Close

Formalize is the structural hinge: you don’t “execute” without durable intent.

### Domains

Domains tell Praxis what kinds of artifacts are valid and what "done" looks like.

| Domain  | Intent                       | Typical formalize artifact       |
| ------- | ---------------------------- | -------------------------------- |
| Code    | Functional systems and tools | SOD (Solution Overview Document) |
| Create  | Aesthetic output             | Creative brief / prompt set      |
| Write   | Structured thought           | Writing brief                    |
| Observe | Raw capture                  | (none required)                  |
| Learn   | Skill formation              | Learning plan                    |

Each domain supports **subtypes** for more specific guidance:

| Domain  | Subtypes                                               |
| ------- | ------------------------------------------------------ |
| Code    | cli, library, api, webapp, infrastructure, script      |
| Create  | visual, audio, video, interactive, generative, design  |
| Write   | technical, business, narrative, academic, journalistic |
| Observe | notes, bookmarks, clips, logs, captures                |
| Learn   | skill, concept, practice, course, exploration          |

### Privacy

Privacy is declared in `praxis.yaml` and should be treated as a real constraint (not a note).

## Quick Start (CLI)

### 1. Create a workspace

```bash
# Create and enter workspace directory
mkdir ~/praxis-workspace
cd ~/praxis-workspace

# Clone the framework
git clone https://github.com/jayers99/praxis-ai.git

# Install dependencies
cd praxis-ai
poetry install
cd ..
```

### 2. Configure your shell

Add to your `~/.bashrc`, `~/.zshrc`, or shell config:

```bash
# Set workspace root
export PRAXIS_HOME="$HOME/praxis-workspace"

# Ensure ~/bin is in PATH
export PATH="$HOME/bin:$PATH"
```

Create a wrapper script (enables tab completion):

```bash
mkdir -p ~/bin
cat > ~/bin/praxis << 'EOF'
#!/bin/bash
exec poetry -C "$PRAXIS_HOME/praxis-ai" run praxis "$@"
EOF
chmod +x ~/bin/praxis
```

Then reload your shell:

```bash
source ~/.zshrc  # or ~/.bashrc
```

### 3. Enable tab completion (optional)

```bash
praxis --install-completion
```

Restart your shell, then use `<tab><tab>` to see available commands and options.

### 4. Verify installation

```bash
praxis --help
```

### 5. Initialize your workspace

```bash
praxis workspace init
# Creates: extensions/, examples/, projects/, workspace-config.yaml
```

### 6. Install extensions and examples (optional)

```bash
# List available extensions and examples
praxis extensions list
praxis examples list

# Install an extension
praxis extensions add template-python-cli

# Install a worked example
praxis examples add uat-praxis-code
```

### 7. Create a new project

```bash
cd $PRAXIS_HOME/projects
mkdir my-project && cd my-project
praxis init --domain code --privacy personal
# Creates: praxis.yaml, CLAUDE.md, docs/capture.md
```

### Common commands

Validate a project's governance configuration:

```bash
praxis validate                   # Validate current directory
praxis validate --strict          # Treat warnings as errors (for CI)
praxis validate --check-all       # Run tests, lint, types, coverage
```

Transition lifecycle stages:

```bash
praxis stage formalize            # Move to formalize stage
praxis stage execute              # Move to execute (requires docs/sod.md)
```

Check project status:

```bash
praxis status                     # Current state, next steps, history
```

Audit against domain best practices:

```bash
praxis audit                      # Check tooling, structure, testing
praxis audit --strict             # Fail on warnings
```

Work with domain opinions (planned):

```bash
praxis opinions                   # Show applicable opinions for project
praxis opinions --prompt          # Generate AI context with opinions
praxis opinions --check           # Validate against quality gates
praxis opinions --list            # List all available opinion files
```

## Quick Start (Using an Agent)

From a project directory, start an agentic session (Copilot, Claude Code, etc.) and prompt:

```text
Start a new Praxis project for building a Python CLI tool.
```

Expected flow:

- The agent initializes `praxis.yaml` (domain, stage, privacy, environment)
- You capture raw inputs
- The agent guides you through stages
- Formalize produces the durable artifact(s) required before Execute

## Repo Layout

```text
src/praxis/           CLI package (Typer + Pydantic)
docs/                 Specifications (SOD, lifecycle, privacy, etc.)
docs/adr/             Architecture Decision Records
docs/opinions/        Domain-specific quality guidance (advisory)
  _templates/         Templates for creating opinion files
  _shared/            Cross-domain principles
  code/               Code domain opinions
  create/             Create domain opinions
  write/              Write domain opinions
  learn/              Learn domain opinions
  observe/            Observe domain opinions
tests/                BDD tests (pytest-bdd + Gherkin)
extensions.yaml       Registry of available extensions
examples.yaml         Registry of available examples
```

**Workspace Structure:** User projects live at `$PRAXIS_HOME/projects/`, not inside this repo. See [User Guide](docs/user-guide.md) for workspace setup.

## Status

Core CLI is functional with project commands (`init`, `validate`, `stage`, `status`, `audit`) and workspace management (`workspace`, `extensions`, `examples`). Code domain is fully supported.

## License

PolyForm Noncommercial License 1.0.0
