# Model Selection Matrix

A 4D scoring guide for selecting the right AI agent/model combination based on Praxis domain and lifecycle stage.

---

## Dimensions

### Agents

| Agent | Strengths | Weaknesses |
|-------|-----------|------------|
| **GitHub Copilot** | IDE integration, fast completions, code context | Limited reasoning, no multi-turn memory |
| **Claude Code** | Deep reasoning, long context, multi-turn, tool use, agentic | Higher latency, cost |
| **ChatGPT** | Broad knowledge, plugins, web browsing, multimodal | Less precise for code, context limits |
| **Gemini** | Long context (1M+), multimodal, Google integration | Variable quality, newer ecosystem |

---

### Models (as of Dec 2024)

| Provider | Model | Tier | Best For | Notes |
|----------|-------|------|----------|-------|
| **Anthropic** | Claude Opus 4.5 | Premium | Complex reasoning, architecture, ambiguous problems | Top-tier reasoning |
| | Claude Sonnet 4 | Standard | Balanced tasks, code generation, analysis | Daily driver |
| | Claude Haiku 3.5 | Fast | Quick edits, simple completions, high volume | Cost-effective |
| **OpenAI** | o1 | Premium | Math, formal logic, multi-step reasoning | Chain-of-thought reasoning |
| | o3-mini | Standard+ | Code generation with reasoning | Good for algorithmic work |
| | GPT-4o | Standard | General purpose, multimodal | Solid all-rounder |
| | GPT-4o-mini | Fast | Quick tasks, cost-sensitive | Budget option |
| **Google** | Gemini 2.5 Pro | Premium | Complex reasoning, long context, code | Strong competitor to Opus |
| | Gemini 2.0 Flash | Fast | Speed, multimodal, long context | Great latency |
| | Gemini 1.5 Pro | Standard | Long documents, code analysis | 1M context window |
| | **Gemini 2.5 Flash** | Ultra-Fast | High-volume, creative tasks, summaries | ⭐ "Nano Banana" - surprisingly capable |

---

## The Matrix

### Scoring Key
- **1** = Overkill / waste of money
- **2** = Can work but suboptimal
- **3** = Good fit
- **4** = Ideal match

---

## Consolidated Domain × Stage Matrix

After analysis, domains cluster into three patterns:

### Pattern A: Structured Domains (Code, Write, Learn)

These domains share similar model requirements—Premium for formalization, Standard for active work.

| Stage | Ultra-Fast | Fast | Standard | Premium | Notes |
|-------|------------|------|----------|---------|-------|
| **Capture** | 4 | 4 | 2 | 1 | Jot ideas, notes—no reasoning needed |
| **Sense** | 3 | 3 | 4 | 2 | Organize, understand, find patterns |
| **Explore** | 2 | 2 | 4 | 3 | Generate options, brainstorm |
| **Shape** | 2 | 2 | 4 | 3 | Converge, refine approach |
| **Formalize** | 1 | 2 | 3 | **4** | SOD/brief requires deep reasoning |
| **Commit** | 2 | 3 | 4 | 2 | Validate scope, lock decisions |
| **Execute** | 2 | 3 | 4 | 2 | Implement with clear spec |
| **Sustain** | 3 | 3 | 4 | 2 | Maintenance, revisions |
| **Close** | 4 | 4 | 3 | 1 | Archive, document learnings |

**Domain-specific notes:**
- **Code:** Premium especially valuable for architecture decisions, debugging complex issues
- **Write:** Premium also valuable at Shape (argument structure) and Execute (quality prose)
- **Learn:** Premium useful for Socratic dialogue in Execute

---

### Pattern B: Create Domain

Creative work benefits from fast iteration and high-volume generation. **Gemini 2.5 Flash ("Nano Banana")** excels here.

| Stage | Ultra-Fast | Fast | Standard | Premium | Notes |
|-------|------------|------|----------|---------|-------|
| **Capture** | **4** | 4 | 2 | 1 | Collect references, inspiration |
| **Sense** | **4** | 4 | 3 | 1 | Style analysis, mood boards |
| **Explore** | **4** | 3 | 3 | 2 | ⭐ Generate many variations cheaply |
| **Shape** | 3 | **4** | 3 | 2 | Curate, select direction |
| **Formalize** | 2 | 2 | 3 | **4** | Creative brief needs precision |
| **Commit** | 3 | 4 | 3 | 2 | Lock scope |
| **Execute** | **4** | 4 | 3 | 2 | ⭐ Generate assets at volume |
| **Sustain** | **4** | 4 | 2 | 1 | Minor tweaks, variations |
| **Close** | **4** | 4 | 2 | 1 | Package, deliver |

**Why Ultra-Fast shines for Create:**
- Creative work = generate many, keep few
- Iteration speed matters more than per-item quality
- Gemini 2.5 Flash handles prompts, variations, style transfer well
- Save Premium budget for the Formalize moment (creative brief)

---

### Pattern C: Observe Domain

Lowest-ceremony domain. Almost everything is Fast/Ultra-Fast.

| Stage | Ultra-Fast | Fast | Standard | Premium | Notes |
|-------|------------|------|----------|---------|-------|
| **Capture** | **4** | 4 | 2 | 1 | Screenshots, links, raw material |
| **Sense** | **4** | 4 | 2 | 1 | Tag, minimal processing |
| **Explore** | 3 | 4 | 3 | 2 | What could this become? |
| **Shape** | 3 | 4 | 3 | 2 | Worth promoting to another domain? |
| **Formalize** | — | — | — | — | Observe rarely formalizes |
| **Commit** | — | — | — | — | N/A |
| **Execute** | — | — | — | — | N/A |
| **Sustain** | **4** | 4 | 2 | 1 | Archive maintenance |
| **Close** | **4** | 4 | 2 | 1 | Cull, archive |

---

## Model Selection by Provider

### Tier Mapping

| Tier | Anthropic | OpenAI | Google |
|------|-----------|--------|--------|
| **Premium** | Opus 4.5 | o1 | Gemini 2.5 Pro |
| **Standard** | Sonnet 4 | GPT-4o, o3-mini | Gemini 1.5 Pro |
| **Fast** | Haiku 3.5 | GPT-4o-mini | Gemini 2.0 Flash |
| **Ultra-Fast** | — | — | **Gemini 2.5 Flash** ⭐ |

### Provider Strengths

| Task Type | Best Provider | Why |
|-----------|---------------|-----|
| Deep reasoning, ambiguity | Anthropic (Opus) | Best reasoning quality |
| Math, formal logic | OpenAI (o1) | Chain-of-thought strength |
| Long context (>100k) | Google (Gemini) | 1M+ context window |
| High-volume creative work | **Google (Gemini 2.5 Flash)** | ⭐ Best cost/quality for Create |
| Code generation | Anthropic (Sonnet) or OpenAI (o3-mini) | Both strong |
| Multimodal (images) | OpenAI (GPT-4o) or Google | Native vision |

---

## Gemini 2.5 Flash ("Nano Banana"): When to Use

You've found this model punches above its weight. Best use cases:

| Use Case | Why It Works |
|----------|--------------|
| **Creative exploration** | Generate 20 variations, keep 2 |
| **Style transfer prompts** | Fast iteration on aesthetic direction |
| Summarization | Simple extraction, high volume |
| Tagging/classification | Pattern matching, not reasoning |
| Format conversion | Mechanical transformation |
| Capture-stage processing | Low stakes, speed matters |
| First-pass filtering | Triage before expensive model |
| Bulk operations | 10x cost savings add up |

**Caution:** Avoid for Formalize, complex debugging, or ambiguous requirements.

---

## Decision Heuristics

### When to use Premium (Opus, o1, Gemini 2.5 Pro)

1. **Ambiguity is high** — Requirements unclear, multiple valid interpretations
2. **Stakes are high** — Architecture decisions, public APIs, irreversible choices
3. **Formalize stage** — SODs, briefs, contracts need careful reasoning
4. **Debugging complex issues** — Multi-system, non-obvious root cause
5. **Novel problems** — No existing pattern to follow

### When to use Standard (Sonnet, GPT-4o, Gemini 1.5 Pro)

1. **Clear requirements** — Know what you want, need execution
2. **Explore → Execute** — Most active work in Code/Write/Learn
3. **Code generation** — Implement from spec
4. **Analysis** — Understand existing code/content

### When to use Fast (Haiku, GPT-4o-mini, Gemini 2.0 Flash)

1. **High volume** — Many small tasks
2. **Low ambiguity** — Completions, simple edits
3. **Bookkeeping stages** — Capture, Close
4. **Cost-sensitive** — Batch processing, automation

### When to use Ultra-Fast (Gemini 2.5 Flash)

1. **Create domain** — Most of Explore and Execute
2. **Bulk processing** — Hundreds/thousands of items
3. **Simple extraction** — Pull structured data from text
4. **Triage** — Filter before sending to better model
5. **Capture/Close stages** — Minimal reasoning required

---

## Agent Selection

### Use Copilot when:
- In IDE, need fast completions
- Context is local (current file + few imports)
- Task is "continue this pattern"
- No multi-turn reasoning needed

### Use Claude Code when:
- Need multi-turn dialogue with tool use
- Task requires file search, edits across codebase
- Need to reason about trade-offs
- Working through Formalize stage
- Agentic workflows (plan → execute → verify)

### Use ChatGPT when:
- Need web browsing for research
- Working with images/multimodal
- General knowledge queries
- Plugin ecosystem helpful

### Use Gemini when:
- Very long context (100k+ tokens)
- Google Workspace integration
- **Create domain work** (use 2.5 Flash)
- Cost-sensitive high-volume work

---

## Cost/Benefit Quick Reference

| Scenario | Recommended | Why |
|----------|-------------|-----|
| "Fix this typo" | Copilot / Haiku | Trivial task |
| "Add a function like this one" | Copilot / Haiku | Pattern completion |
| "Generate 20 logo variations" | **Gemini 2.5 Flash** | Create domain, high volume |
| "Summarize these 50 files" | Gemini 2.5 Flash | High volume, simple task |
| "Implement this feature" | Sonnet / GPT-4o | Clear spec, needs execution |
| "How should I architect this?" | Opus / o1 | High ambiguity, high stakes |
| "Debug this weird issue" | Sonnet → Opus | Start cheaper, escalate if stuck |
| "Write the SOD for this project" | Opus | Formalize = deep reasoning |
| "Write the creative brief" | Opus | Formalize = deep reasoning |
| "Refactor this file" | Sonnet | Clear goal, needs care |
| "Analyze this 500-page doc" | Gemini 1.5 Pro | Long context |
| "What are my options here?" | Sonnet | Explore stage |
| "Is this approach sound?" | Opus / Gemini 2.5 Pro | Validate architecture |

---

## Escalation Pattern

Start with the cheapest viable option, escalate when needed:

```
Gemini 2.5 Flash → Gemini 2.0 Flash: Need more nuance
Flash/Haiku → Sonnet/GPT-4o: Task needs real reasoning
Sonnet → Opus/o1: Hitting ambiguity, trade-offs, or wrong answers
Copilot → Claude Code: Need multi-turn, tools, or broader context
```

Don't start with Opus for everything. Most tasks don't need it.

---

## Version

- v0.2 — Added all providers, consolidated domains, Gemini 2.5 Flash ("Nano Banana") for Create (Dec 2024)
- v0.1 — Initial matrix (Dec 2024)
- Models and pricing change frequently; revisit quarterly
