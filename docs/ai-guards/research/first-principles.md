# AI Memory: First Principles & Best Practices

**Purpose:** Reference document for AI Guards design decisions.
**Date:** 2024-12-24

---

## TL;DR

1. **AI has no memory** — everything must be in the context window
2. **Instruction files ARE the memory** — they're loaded at session start
3. **~150-200 instructions max** — beyond that, compliance degrades
4. **Earlier > later** — order matters; put important stuff first
5. **Quality > quantity** — ruthlessly selective beats exhaustive
6. **Single source, rendered outputs** — content can be shared across tools, only file locations differ

---

## First Principles

### The Memory Model

```
┌─────────────────────────────────────────────────────────┐
│                    CONTEXT WINDOW                        │
│  (everything the AI "knows" during a session)           │
├─────────────────────────────────────────────────────────┤
│  System Prompt (~50 instructions built into Claude)     │
│  + User Instructions (CLAUDE.md, ~/.claude/CLAUDE.md)   │
│  + Conversation History                                  │
│  + Tool Outputs (file contents, command results)        │
│  + Current Request                                       │
└─────────────────────────────────────────────────────────┘
         ↓
   Limited capacity (~1M tokens, but practical limits lower)
         ↓
   When full: summarization occurs, context is lost
```

**Key Insight:** There is no persistent memory. Every session starts fresh. Instruction files are how we give AI "memory" it doesn't naturally have.

### The Fundamental Tradeoffs

| More Instructions | Fewer Instructions |
|-------------------|-------------------|
| Better guidance | Less consistent behavior |
| Less room for actual work | More room for code/conversation |
| Higher cognitive load on model | Simpler to follow |
| More conflicts possible | Fewer conflicts |

**The Answer:** Quality over quantity. A few well-crafted, high-signal rules beat many vague ones.

---

## Research Findings

### Instruction Capacity Limits

| Finding | Implication |
|---------|-------------|
| Frontier LLMs follow ~150-200 instructions consistently | Budget is limited; be selective |
| Claude Code's system prompt uses ~50 instructions | You have ~100-150 left for your files |
| Smaller models handle fewer instructions | Design for the constraint |
| Performance degrades gradually, then cliffs | Stay well under the limit |

### Order Effects

| Finding | Implication |
|---------|-------------|
| Earlier instructions get more attention | Put critical rules first |
| Later instructions may be deprioritized | Don't bury important stuff |
| This is measurable and consistent | Order is a design decision |

**For Guards:** User-level core guards should come first in rendered output, then environment, then project-specific.

### Instruction Complexity

| Type | Difficulty | Recommendation |
|------|------------|----------------|
| Simple positive ("use X") | Easy | Prefer these |
| Simple negative ("never Y") | Harder | Use sparingly |
| Conditional ("if X then Y") | Hard | Minimize |
| Complex conditional | Very hard | Avoid or simplify |

**For Guards:** Prefer simple, declarative statements. "Use TypeScript" beats "If the project has TypeScript configured, use TypeScript unless the file is a JavaScript file that imports CommonJS modules."

### What Works in Instruction Files

**Do Include:**
- Project overview (1-2 sentences)
- Tech stack and frameworks
- Key commands (build, test, lint)
- Architecture decisions affecting code generation
- Project-specific quirks and gotchas
- Pointers to detailed docs (`see docs/architecture.md`)

**Don't Include:**
- Exhaustive command lists
- Code snippets (they go stale)
- Things linters can enforce (formatting, style)
- Task-specific instructions (use separate files)
- Obvious things ("write good code", "be helpful")
- Full documentation (use pointers instead)

### The WHY-WHAT-HOW Framework

Structure instruction files around:

- **WHAT**: Tech stack, project structure, key files
- **WHY**: Purpose of the project, what components do
- **HOW**: Commands to build/test, verification steps, workflow

---

## Size Guidelines

| Metric | Recommendation | Rationale |
|--------|----------------|-----------|
| Line count | <300 lines, ideally <60 | Every line costs tokens |
| Instruction count | ~50-100 per file | Leave room for system prompt |
| Total across files | <150 user instructions | Stay under model limits |
| File size | ~13KB max for professional use | Cited as working limit |

### Progressive Disclosure Pattern

```
CLAUDE.md (main file)
├── Universal rules only (~30-50 instructions)
├── Pointers to detailed docs
└── References to domain-specific files

docs/ai-context/
├── architecture.md (read when doing architecture work)
├── testing.md (read when writing tests)
└── deployment.md (read when deploying)
```

**Benefit:** Base file stays small; detailed context loaded on-demand.

---

## Cross-Tool File Locations

### Claude Code
| Location | Scope | Notes |
|----------|-------|-------|
| `~/.claude/CLAUDE.md` | User, all projects | Personal preferences |
| `./CLAUDE.md` | Project, shared | Team conventions |
| Parent directories | Monorepo support | Inherited down |
| `.claude/commands/*.md` | Custom commands | Slash command extensions |

### GitHub Copilot
| Location | Scope | Notes |
|----------|-------|-------|
| `.github/copilot-instructions.md` | Project | Main instructions |
| `.github/instructions/*.instructions.md` | Scoped | Pattern-specific |
| Organization settings | Org-wide | Enterprise consistency |

**Key Discovery:** Copilot now reads CLAUDE.md, AGENTS.md, and GEMINI.md as alternates. This reduces the need for vendor-specific files.

### Cursor
| Location | Scope | Notes |
|----------|-------|-------|
| `.cursor/rules/` | Project | Directory of rules |
| `.cursorrules` | Project | Single file alternative |

### Google Antigravity/Gemini
| Location | Scope | Notes |
|----------|-------|-------|
| `GEMINI.md` | Project | Emerging convention |
| Format TBD | - | Still evolving |

---

## Design Implications for AI Guards

### Architecture Decision: Single Source, Rendered Outputs

```
Source Files (authored)          Rendered Files (generated)
─────────────────────           ────────────────────────────
~/.ai-guards/                   ~/.claude/CLAUDE.md
  core.md
  env/home.md
  env/work.md

project/praxis/ai-guards/       project/CLAUDE.md
  domain.md                     project/.github/copilot-instructions.md
```

**Rationale:**
- Content is mostly shareable across tools
- File locations are fixed by each tool
- Rendering allows composition and environment switching
- Single source of truth prevents drift

### Composition Order (based on order effects research)

```
1. User core guards (highest priority, earliest)
2. Environment overlay (home/work constraints)
3. Project domain guards (architecture, patterns)
4. Project-specific overrides (quirks, exceptions)
```

### Conflict Resolution Strategy

| Conflict Type | Resolution |
|---------------|------------|
| User vs Project style preferences | Project wins (you're in their codebase) |
| User vs Project security/privacy | Stricter wins |
| Environment vs Project tools | Environment wins (you have what you have) |
| Positive vs Negative instruction | Negative wins (safety) |

### Token Budget Allocation

```
Total budget: ~150 instructions

User core:        30-40  (communication style, universal preferences)
Environment:      10-20  (tool mappings, constraints)
Project domain:   40-60  (architecture, patterns, commands)
Project specific: 20-30  (quirks, exceptions, gotchas)
Buffer:           20-30  (headroom for growth)
```

---

## The Goldfish Memory Problem

### The Pain
- Productive session solving complex problems
- AI learns your patterns, architecture, decisions
- New session = all context lost
- Enterprise: branch switching breaks flow
- Team knowledge trapped in individual chat sessions

### Solutions

**Instruction Files (what we're designing):**
- Persistent across sessions
- Shared with team
- Version controlled
- But: static, not session-aware

**MCP (Model Context Protocol):**
- Cross-tool context sharing
- Dynamic context injection
- Emerging standard
- Future integration point for Guards

**LCMP Pattern (Long-Term Context Management Protocol):**
```
./context/
  state.md      # Current project state, active tasks, blockers
  schema.md     # Data structures and file locations
  decisions.md  # Technical choices and rationale
  insights.md   # Cumulative findings and discoveries
```
- Structured external memory
- Updated during/after sessions
- Read at session start
- Complements instruction files

---

## Maintenance Best Practices

### Evolving Instructions Over Time

1. **Capture during work:** Use `#` key in Claude Code to add learnings
2. **Commit with code:** Instruction changes are part of the codebase
3. **Review periodically:** Prune stale instructions
4. **Test effectiveness:** Does the AI actually follow this?

### Treating Instructions as Production Prompts

- Iterate based on observed behavior
- A/B test significant changes
- Remove instructions that aren't followed
- Consolidate redundant rules

### Team Collaboration

- Instruction files are shared documentation
- Changes should be reviewed like code
- Accumulate team knowledge over time
- Onboarding: instruction file IS the onboarding

---

## Sources

- [Anthropic: Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [HumanLayer: Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [Arize: CLAUDE.md Optimization](https://arize.com/blog/claude-md-best-practices-learned-from-optimizing-claude-code-with-prompt-learning/)
- [GitHub: 5 Tips for Custom Instructions](https://github.blog/ai-and-ml/github-copilot/5-tips-for-writing-better-custom-instructions-for-copilot/)
- [How Many Instructions Can LLMs Follow at Once?](https://arxiv.org/html/2507.11538v1)
- [MIT Press: LLM Instruction Following Survey](https://direct.mit.edu/coli/article/50/3/1053/121669/Large-Language-Model-Instruction-Following-A)
- [Building Persistent Memory for AI Assistants](https://medium.com/@linvald/building-persistent-memory-for-ai-assistants-a-model-context-protocol-implementation-80b6e6398d40)
