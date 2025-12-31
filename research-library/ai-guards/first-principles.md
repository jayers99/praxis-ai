# AI Memory: First Principles & Best Practices

<!--
metadata:
  id: ai-guards-first-principles-2024-12-24
  title: AI Memory: First Principles & Best Practices
  date: 2024-12-24
  author: research-librarian
  status: approved
  topic: ai-guards
  also_relevant: [foundations, patterns]
  keywords: [ai-memory, context-window, instruction-files, claude-md, best-practices, token-budget]
  consensus: high
  epistemic_standard: thorough
  sources_count: 7
  supersedes: null
  related: [ai-guards-user-directives-2024-12-24, ai-guards-rules-analysis-2024-12-24]
  approved_by: human
  approved_date: 2025-12-30
-->

## Executive Summary

- **AI has no memory** — everything must be in the context window
- **Instruction files ARE the memory** — they're loaded at session start
- **~150-200 instructions max** — beyond that, compliance degrades
- **Earlier > later** — order matters; put important stuff first
- **Quality > quantity** — ruthlessly selective beats exhaustive
- **Single source, rendered outputs** — content can be shared across tools, only file locations differ

## Consensus Rating

**High**: Research from Anthropic, academic papers on LLM instruction following, and practitioner experience converge on these constraints.

## Body

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

### Research Findings

#### Instruction Capacity Limits

| Finding | Implication |
|---------|-------------|
| Frontier LLMs follow ~150-200 instructions consistently | Budget is limited; be selective |
| Claude Code's system prompt uses ~50 instructions | You have ~100-150 left for your files |
| Smaller models handle fewer instructions | Design for the constraint |
| Performance degrades gradually, then cliffs | Stay well under the limit |

#### Order Effects

| Finding | Implication |
|---------|-------------|
| Earlier instructions get more attention | Put critical rules first |
| Later instructions may be deprioritized | Don't bury important stuff |
| This is measurable and consistent | Order is a design decision |

**For Guards:** User-level core guards should come first in rendered output, then environment, then project-specific.

#### Instruction Complexity

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

## Reusable Artifacts

### Size Guidelines

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

### Token Budget Allocation

```
Total budget: ~150 instructions

User core:        30-40  (communication style, universal preferences)
Environment:      10-20  (tool mappings, constraints)
Project domain:   40-60  (architecture, patterns, commands)
Project specific: 20-30  (quirks, exceptions, gotchas)
Buffer:           20-30  (headroom for growth)
```

### Cross-Tool File Locations

| Tool | User Location | Project Location |
|------|---------------|------------------|
| Claude Code | `~/.claude/CLAUDE.md` | `./CLAUDE.md` |
| GitHub Copilot | Org settings | `.github/copilot-instructions.md` |
| Cursor | — | `.cursor/rules/` or `.cursorrules` |
| Gemini | — | `GEMINI.md` |

**Key Discovery:** Copilot now reads CLAUDE.md, AGENTS.md, and GEMINI.md as alternates.

## Dissenting Views / Caveats

- Some users report success with longer instruction files, but this may be model-specific
- The exact instruction limit varies by model and updates frequently
- Complex conditionals sometimes work well if the user needs them frequently

## Sources

1. [Anthropic: Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
2. [HumanLayer: Writing a Good CLAUDE.md](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
3. [Arize: CLAUDE.md Optimization](https://arize.com/blog/claude-md-best-practices-learned-from-optimizing-claude-code-with-prompt-learning/)
4. [GitHub: 5 Tips for Custom Instructions](https://github.blog/ai-and-ml/github-copilot/5-tips-for-writing-better-custom-instructions-for-copilot/)
5. [How Many Instructions Can LLMs Follow at Once?](https://arxiv.org/html/2507.11538v1)
6. [MIT Press: LLM Instruction Following Survey](https://direct.mit.edu/coli/article/50/3/1053/121669/Large-Language-Model-Instruction-Following-A)
7. [Building Persistent Memory for AI Assistants](https://medium.com/@linvald/building-persistent-memory-for-ai-assistants-a-model-context-protocol-implementation-80b6e6398d40)

---

_Migrated from research/ai-guards/first-principles.md_
_Approved: 2025-12-30_
