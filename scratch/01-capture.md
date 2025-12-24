# AI Guards — Capture

**Feature:** AI Guards Design for Multi-Environment Support
**Issue:** [#42](https://github.com/jayers99/praxis-ai/issues/42)
**Stage:** Capture
**Date:** 2024-12-24

---

## Raw Inputs

### The Problem Being Solved

Users operate AI assistants (Claude Code, Copilot, Gemini) across multiple environments (home, work) with different constraints:
- Work environments have compliance, tooling, and privacy requirements
- Home environments have different tool preferences and fewer restrictions
- Current Praxis model puts environment in `praxis.yaml` (project-level), but environment is fundamentally a user-level concern

### Where This Came From

- Tension discovered while designing how AI front-end files (CLAUDE.md, COPILOT.md) should be generated
- Current state: CLAUDE.md is manually authored per-project
- Desired state: CLAUDE.md rendered from composable guards

### Key Observations

1. **Environment doesn't belong in projects** — A project doesn't know if I'm at home or work. The user knows.

2. **AI reasoning should be invariant** — Whether I'm using Claude or Copilot, the thinking and workflow principles shouldn't change. Only the tooling translation differs.

3. **Late binding for tools** — Projects should declare abstract tool roles ("build tool", "test runner"), users map those to concrete tools per environment.

4. **Composability** — The final AI instruction file should be:
   ```
   (core user guards) + (env overlay) + (project domain guards) = AI front-end file
   ```

### Prior Art / References

- Current SOD §3.4 defines environment as a praxis.yaml dimension
- [docs/layer-model.md](../docs/layer-model.md) — Opinions → Governance → Execution
- [docs/external-constraints.md](../docs/external-constraints.md) — Environmental authority
- [docs/guardrails.md](../docs/guardrails.md) — Execution-level constraints
- Existing opinions system in `docs/opinions/{domain}/`

### Open Questions (raw, unprocessed)

- Should environment remain in praxis.yaml at all, or move entirely to user-level?
- If both, what's the precedence? User overrides project? Project overrides user?
- How does this interact with privacy levels? (Work environment might enforce stricter privacy)
- Is `~/.ai-guards/` the right location? Other options: `~/.config/praxis/`, `~/.praxis/`
- Should guards be markdown, YAML, or something else?
- How do we validate the composed output?
- What's the rendering trigger — on-demand CLI command? Git hook? IDE plugin?

### Stakeholder Needs

- **As a developer**, I want my AI assistant to automatically adapt when I switch from home to work, without me reconfiguring each project
- **As a project maintainer**, I want to define domain-specific AI guidance that applies regardless of who's working on it
- **As a user with multiple AI tools**, I want consistent behavior across Claude, Copilot, etc. even if the specific instructions differ

---

## Notes

This is a feature within an existing project (Praxis), not a new project. Using "Praxis Light" — the stages provide structure but artifacts can be lighter weight than a full SOD for v1.

The existing `docs/ai-guards.md` draft represents initial exploration that should inform the Sense stage.
