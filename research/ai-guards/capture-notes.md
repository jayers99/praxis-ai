# AI Guards — Capture & Design Notes

**Source:** Consolidated from scratch/01-capture.md and scratch/pr-42-ai-guards.md
**Date:** 2024-12-24

---

## The Problem Being Solved

Users operate AI assistants (Claude Code, Copilot, Gemini) across multiple environments (home, work) with different constraints:
- Work environments have compliance, tooling, and privacy requirements
- Home environments have different tool preferences and fewer restrictions
- Current Praxis model puts environment in `praxis.yaml` (project-level), but environment is fundamentally a user-level concern

### Where This Came From

- Tension discovered while designing how AI front-end files (CLAUDE.md, COPILOT.md) should be generated
- Current state: CLAUDE.md is manually authored per-project
- Desired state: CLAUDE.md rendered from composable guards

---

## Key Observations

1. **Environment doesn't belong in projects** — A project doesn't know if I'm at home or work. The user knows.

2. **AI reasoning should be invariant** — Whether I'm using Claude or Copilot, the thinking and workflow principles shouldn't change. Only the tooling translation differs.

3. **Late binding for tools** — Projects should declare abstract tool roles ("build tool", "test runner"), users map those to concrete tools per environment.

4. **Composability** — The final AI instruction file should be:
   ```
   (core user guards) + (env overlay) + (project domain guards) = AI front-end file
   ```

---

## Proposed Design Principles

### 1. Reason Once, Translate Late
AI reasoning, principles, and workflows remain invariant. Tooling and compliance constraints are applied as a final translation step, not baked into the reasoning.

### 2. Environment at User Level
Environment (home vs work) is a user-level concern, not a project-level one. Projects define abstract tool roles; users map those to concrete tools per environment.

### 3. AI Front-Ends as Rendered Outputs
`CLAUDE.md`, `COPILOT.md`, etc. are conceptually rendered artifacts:
```
(core user guards) + (env overlay) + (project domain guards) = AI front-end file
```

---

## Proposed File Structure

### User-Level (~/.ai-guards/)
```
~/.ai-guards/
  core.md            # Stable user preferences
  env.md             # Active environment selector
  tools.md           # Tool mappings (preferred + alternatives)
  env/
    work.md          # Work-only constraints
    home.md          # Home-only constraints
```

### Project-Level (praxis/)
```
praxis/
  ai-guards/
    build.md         # Code domain guards
    write.md         # Write domain guards
    create.md        # Create domain guards
    learn.md         # Learn domain guards
```

---

## Stakeholder Needs

- **As a developer**, I want my AI assistant to automatically adapt when I switch from home to work, without me reconfiguring each project
- **As a project maintainer**, I want to define domain-specific AI guidance that applies regardless of who's working on it
- **As a user with multiple AI tools**, I want consistent behavior across Claude, Copilot, etc. even if the specific instructions differ

---

## Open Questions (Deferred to Future Issue)

| Question | Current State | Proposed State |
|----------|---------------|----------------|
| Where is environment defined? | `praxis.yaml` (SOD §3.4) | `~/.ai-guards/env.md` (user-level) |
| Is CLAUDE.md manually authored? | Yes (current) | Rendered output (proposed) |
| How do praxis.yaml and ~/.ai-guards interact? | Undefined | Needs specification |

Additional questions:
- Should environment remain in praxis.yaml at all, or move entirely to user-level?
- If both, what's the precedence? User overrides project? Project overrides user?
- How does this interact with privacy levels? (Work environment might enforce stricter privacy)
- Is `~/.ai-guards/` the right location? Other options: `~/.config/praxis/`, `~/.praxis/`
- Should guards be markdown, YAML, or something else?
- How do we validate the composed output?
- What's the rendering trigger — on-demand CLI command? Git hook? IDE plugin?

---

## Related Documentation

- [SOD v0.3](../../sod.md) — Section 3.4 Environment
- [Layer Model](../../layer-model.md) — Opinions → Governance → Execution
- [External Constraints](../../external-constraints.md) — Environmental authority
- [Guardrails](../../guardrails.md) — Execution-level constraints
