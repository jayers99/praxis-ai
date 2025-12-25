# Model Selection Matrix

A 4D scoring guide for selecting the right AI agent/model combination based on Praxis domain and lifecycle stage.

---

## Dimensions

### Agents
| Agent | Strengths | Weaknesses |
|-------|-----------|------------|
| **Copilot** | IDE integration, fast completions, code context | Limited reasoning, no multi-turn memory |
| **Claude** | Deep reasoning, long context, multi-turn, tool use | Higher latency, cost |

### Models (as of Dec 2024)

| Provider | Model | Tier | Best For |
|----------|-------|------|----------|
| **Anthropic** | Claude Opus 4.5 | Premium | Complex reasoning, architecture, ambiguous problems |
| | Claude Sonnet 4 | Standard | Balanced tasks, code generation, analysis |
| | Claude Haiku 3.5 | Fast | Quick edits, simple completions, high volume |
| **OpenAI** | o1 | Premium | Math, formal logic, multi-step reasoning |
| | o1-mini | Standard | Code generation with reasoning |
| | GPT-4o | Standard | General purpose, multimodal |
| | GPT-4o-mini | Fast | Quick tasks, cost-sensitive |
| **Google** | Gemini 2.0 Flash | Fast | Speed, multimodal, long context |
| | Gemini 1.5 Pro | Standard | Long documents, code analysis |

---

## The Matrix

### Scoring Key
- **1** = Overkill / waste of money
- **2** = Can work but suboptimal
- **3** = Good fit
- **4** = Ideal match

---

## By Domain × Stage

### Code Domain

| Stage | Haiku/Fast | Sonnet/Standard | Opus/Premium | Notes |
|-------|------------|-----------------|--------------|-------|
| Capture | 4 | 2 | 1 | Jot ideas, no reasoning needed |
| Sense | 3 | 4 | 2 | Understand codebase, patterns |
| Explore | 2 | 4 | 3 | Generate options, prototype |
| Shape | 2 | 4 | 3 | Refine approach, trade-offs |
| Formalize | 2 | 3 | 4 | SOD requires deep reasoning |
| Commit | 3 | 4 | 2 | Validate scope, check constraints |
| Execute | 3 | 4 | 2 | Implement with clear spec |
| Sustain | 3 | 4 | 2 | Bug fixes, maintenance |
| Close | 4 | 3 | 1 | Archive, document learnings |

**Code summary:** Use Premium for Formalize (architecture decisions). Standard for Explore→Execute. Fast for bookkeeping.

---

### Write Domain

| Stage | Haiku/Fast | Sonnet/Standard | Opus/Premium | Notes |
|-------|------------|-----------------|--------------|-------|
| Capture | 4 | 2 | 1 | Raw notes, brain dump |
| Sense | 3 | 4 | 2 | Organize, find themes |
| Explore | 2 | 4 | 3 | Generate angles, outlines |
| Shape | 2 | 3 | 4 | Argument structure, coherence |
| Formalize | 2 | 3 | 4 | Writing brief, thesis clarity |
| Commit | 3 | 4 | 2 | Scope the piece |
| Execute | 2 | 4 | 3 | Draft prose (quality matters) |
| Sustain | 3 | 4 | 2 | Revisions, polish |
| Close | 4 | 3 | 1 | Final format, publish |

**Write summary:** Premium for Shape/Formalize (structural thinking). Standard for drafting. Fast for capture/close.

---

### Create Domain

| Stage | Haiku/Fast | Sonnet/Standard | Opus/Premium | Notes |
|-------|------------|-----------------|--------------|-------|
| Capture | 4 | 2 | 1 | Collect references |
| Sense | 3 | 4 | 2 | Style analysis |
| Explore | 2 | 4 | 3 | Generate variations |
| Shape | 2 | 4 | 3 | Curate, select direction |
| Formalize | 2 | 3 | 4 | Creative brief |
| Commit | 3 | 4 | 2 | Lock scope |
| Execute | 3 | 4 | 2 | Generate assets |
| Sustain | 4 | 3 | 1 | Minor tweaks |
| Close | 4 | 2 | 1 | Package, deliver |

**Create summary:** Premium for Formalize (creative brief). Standard for exploration/execution. Fast for most bookkeeping.

---

### Learn Domain

| Stage | Haiku/Fast | Sonnet/Standard | Opus/Premium | Notes |
|-------|------------|-----------------|--------------|-------|
| Capture | 4 | 2 | 1 | Reading notes |
| Sense | 3 | 4 | 2 | Summarize, connect |
| Explore | 2 | 4 | 3 | Generate questions |
| Shape | 2 | 4 | 3 | Build mental models |
| Formalize | 2 | 3 | 4 | Learning plan, curriculum |
| Commit | 3 | 4 | 2 | Set goals |
| Execute | 2 | 4 | 3 | Practice, Socratic dialogue |
| Sustain | 3 | 4 | 2 | Review, reinforce |
| Close | 4 | 3 | 1 | Assess mastery |

**Learn summary:** Premium for Formalize and deep Socratic exploration. Standard for active learning. Fast for flashcards, quick review.

---

### Observe Domain

| Stage | Haiku/Fast | Sonnet/Standard | Opus/Premium | Notes |
|-------|------------|-----------------|--------------|-------|
| Capture | 4 | 2 | 1 | Screenshot, save link |
| Sense | 4 | 3 | 1 | Tag, minimal processing |
| Explore | 3 | 4 | 2 | What could this become? |
| Shape | 3 | 4 | 2 | Worth promoting to another domain? |
| Formalize | — | — | — | Observe rarely formalizes |
| Commit | — | — | — | N/A |
| Execute | — | — | — | N/A |
| Sustain | 4 | 2 | 1 | Archive maintenance |
| Close | 4 | 2 | 1 | Cull, archive |

**Observe summary:** Mostly Fast tier. Observe is low-ceremony by design.

---

## Decision Heuristics

### When to use Premium (Opus, o1)

1. **Ambiguity is high** — Requirements unclear, multiple valid interpretations
2. **Stakes are high** — Architecture decisions, public APIs, irreversible choices
3. **Formalize stage** — SODs, briefs, contracts need careful reasoning
4. **Debugging complex issues** — Multi-system, non-obvious root cause
5. **Novel problems** — No existing pattern to follow

### When to use Standard (Sonnet, GPT-4o)

1. **Clear requirements** — Know what you want, need execution
2. **Explore → Execute** — Most of the active work
3. **Code generation** — Implement from spec
4. **Analysis** — Understand existing code/content

### When to use Fast (Haiku, GPT-4o-mini, Gemini Flash)

1. **High volume** — Many small tasks
2. **Low ambiguity** — Completions, simple edits
3. **Bookkeeping stages** — Capture, Close
4. **Cost-sensitive** — Batch processing, automation

---

## Agent Selection

### Use Copilot when:
- In IDE, need fast completions
- Context is local (current file + few imports)
- Task is "continue this pattern"
- No multi-turn reasoning needed

### Use Claude (or similar chat) when:
- Need multi-turn dialogue
- Task requires tool use (file search, web, etc.)
- Context spans multiple files/concepts
- Need to reason about trade-offs
- Working through Formalize stage

---

## Cost/Benefit Quick Reference

| Scenario | Recommended | Why |
|----------|-------------|-----|
| "Fix this typo" | Copilot / Haiku | Trivial task |
| "Add a function like this one" | Copilot / Haiku | Pattern completion |
| "Implement this feature" | Sonnet | Clear spec, needs execution |
| "How should I architect this?" | Opus | High ambiguity, high stakes |
| "Debug this weird issue" | Sonnet → Opus | Start cheaper, escalate if stuck |
| "Write the SOD for this project" | Opus | Formalize = deep reasoning |
| "Refactor this file" | Sonnet | Clear goal, needs care |
| "Summarize these notes" | Haiku | Low stakes, high volume |
| "What are my options here?" | Sonnet | Explore stage |
| "Is this approach sound?" | Opus | Validate architecture |

---

## Escalation Pattern

Start with the cheapest viable option, escalate when:

```
Haiku → Sonnet: Task needs more nuance than expected
Sonnet → Opus: Hitting ambiguity, trade-offs, or getting wrong answers
Copilot → Claude: Need multi-turn, tools, or broader context
```

Don't start with Opus for everything. Most tasks don't need it.

---

## Version

- v0.1 — Initial matrix (Dec 2024)
- Models and pricing change frequently; revisit quarterly
