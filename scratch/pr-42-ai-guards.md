# PR: AI Guards Design for Multi-Environment Support

**Branch:** `42-ai-guards-design`
**Issue:** [#42](https://github.com/jayers99/praxis-ai/issues/42)
**Status:** Draft — Ready for Design Review

---

## Summary

This PR introduces the initial design document for the AI Guards system, which controls how AI systems (Claude, Copilot, Gemini, etc.) operate across user environments and project domains.

## What's Included

- `docs/ai-guards.md` — Draft design document covering:
  - Core design principles (reason once, translate late)
  - User-level vs project-level guard structure
  - Environment handling strategy (home/work overlays)
  - Tool mapping with abstract roles and late binding
  - AI front-end file rendering concept

## Key Design Decisions

### 1. Reason Once, Translate Late
AI reasoning, principles, and workflows remain invariant. Tooling and compliance constraints are applied as a final translation step, not baked into the reasoning.

### 2. Environment at User Level
Environment (home vs work) is a user-level concern, not a project-level one. Projects define abstract tool roles; users map those to concrete tools per environment.

### 3. AI Front-Ends as Rendered Outputs
`CLAUDE.md`, `COPILOT.md`, etc. are conceptually rendered artifacts:
```
(core user guards) + (env overlay) + (project domain guards) = AI front-end file
```

## Open Questions Requiring Resolution

Before this can be merged, the following tensions with the existing SOD need resolution:

| Question | Current State | Proposed State |
|----------|---------------|----------------|
| Where is environment defined? | `praxis.yaml` (SOD §3.4) | `~/.ai-guards/env.md` (user-level) |
| Is CLAUDE.md manually authored? | Yes (current) | Rendered output (proposed) |
| How do praxis.yaml and ~/.ai-guards interact? | Undefined | Needs specification |

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

## Acceptance Criteria (from Issue #42)

- [ ] Reconcile environment handling between ai-guards design and SOD
- [ ] Define relationship between `praxis.yaml` and `~/.ai-guards/`
- [ ] Finalize file naming conventions
- [ ] Create minimal skeletons for user and domain guard files
- [ ] Define rendering strategy for AI front-end files
- [ ] Add validation tooling concept

## Testing Plan

This is a design document. Validation will occur through:
1. Design review against existing Praxis docs
2. Worked example showing the rendering flow
3. Integration with `praxis validate` CLI (future)

## Related Documentation

- [SOD v0.3](docs/sod.md) — Section 3.4 Environment
- [Layer Model](docs/layer-model.md) — Opinions → Governance → Execution
- [External Constraints](docs/external-constraints.md) — Environmental authority
- [Guardrails](docs/guardrails.md) — Execution-level constraints

---

## Reviewer Notes

This PR is intentionally **not ready to merge**. It establishes a design proposal that requires discussion and reconciliation with the existing SOD environment model.

Key question for reviewers: **Should environment remain a praxis.yaml dimension, move entirely to user-level, or exist in both places with clear precedence rules?**
