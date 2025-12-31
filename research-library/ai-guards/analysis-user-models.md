# Model File Rules Analysis

<!--
metadata:
  id: ai-guards-rules-analysis-2024-12-24
  title: Model File Rules Analysis
  date: 2024-12-24
  author: research-librarian
  status: approved
  topic: ai-guards
  also_relevant: []
  keywords: [claude-md, rules-analysis, first-principles, instruction-budget, ai-guards]
  consensus: medium
  epistemic_standard: analysis
  sources_count: 0
  supersedes: null
  related: [ai-guards-first-principles-2024-12-24, ai-guards-user-directives-2024-12-24]
  approved_by: human
  approved_date: 2025-12-30
-->

## Executive Summary

- Classification of actual CLAUDE.md rules against AI memory first principles
- 37 strong rules, 2 weak rules, 0 contrary rules after optimization
- Both user core (22 rules) and code domain (17 rules) are well under budget
- Order follows first principles (important stuff first)

## Consensus Rating

**Medium**: Analysis of specific rules against established principles. Useful as a worked example but reflects one user's rule set.

## Body

### First Principles Reference

1. **~150-200 instructions max** — budget is limited
2. **Earlier > later** — order matters
3. **Simple positive > complex/negative** — easier to follow
4. **Quality > quantity** — high-signal, no filler
5. **No obvious things** — don't waste tokens on what's implied
6. **No code snippets** — they go stale
7. **Pointers not copies** — reference docs, don't inline them

### Classification Key

- **Strong** ✓ — Follows principles, high-signal, well-formed
- **Weak** ~ — Could be improved, minor issues
- **Contrary** ✗ — Violates principles, should reconsider

### CLAUDE_model_user.md Analysis

#### Opening Statement

| Rule                                                                       | Rating   | Notes                             |
| -------------------------------------------------------------------------- | -------- | --------------------------------- |
| "I value directness, minimal changes, and working code over explanations." | ✓ Strong | Good WHY context, sets tone early |

#### Communication Preferences

| Rule                                                                          | Rating   | Notes                                                       |
| ----------------------------------------------------------------------------- | -------- | ----------------------------------------------------------- |
| Be direct and concise                                                         | ✓ Strong | Simple, positive                                            |
| Get to the point                                                              | ✓ Strong | Simple, positive (updated from "Skip unnecessary preamble") |
| Provide working code, not explanations of what you could do                   | ✓ Strong | Clear, positive contrast                                    |
| Ask clarifying questions when requirements are ambiguous                      | ✓ Strong | Simple conditional, actionable                              |
| Surface disagreements explicitly rather than silently choosing interpretation | ✓ Strong | Positive framing, high-value                                |

#### Control Signals

| Rule                                                 | Rating   | Notes              |
| ---------------------------------------------------- | -------- | ------------------ |
| "Stop" = halt immediately, wait for instructions     | ✓ Strong | Clear, actionable  |
| "Pause" = checkpoint progress, summarize state, wait | ✓ Strong | Clear, actionable  |
| "Clarify" = I need to understand before you proceed  | ✓ Strong | Clear, actionable  |
| Use Plan Mode for non-trivial implementations        | ✓ Strong | Simple conditional |

#### Epistemic Honesty

| Rule                                      | Rating   | Notes                          |
| ----------------------------------------- | -------- | ------------------------------ |
| "I don't know" beats confident guessing   | ✓ Strong | Clear preference statement     |
| Express uncertainty rather than hiding it | ✓ Strong | Positive framing               |
| Uncertain + consequential → ask first     | ✓ Strong | Simple conditional, high-value |

#### Workflow

| Rule                                                      | Rating   | Notes                        |
| --------------------------------------------------------- | -------- | ---------------------------- |
| Read before modifying — understand existing content first | ✓ Strong | Simple, positive, high-value |
| Make minimal changes to accomplish the task               | ✓ Strong | Simple, positive             |
| Incremental progress over big changes                     | ✓ Strong | Clear preference             |

#### Tools & Environment

| Rule                                                    | Rating   | Notes            |
| ------------------------------------------------------- | -------- | ---------------- |
| Use project-specified tooling over personal preferences | ✓ Strong | Clear preference |

#### Boundaries

| Rule                                                                       | Rating   | Notes                     |
| -------------------------------------------------------------------------- | -------- | ------------------------- |
| Keep solutions simple and focused on the current problem                   | ✓ Strong | Simple, positive          |
| Scope changes to the task at hand                                          | ✓ Strong | Simple, positive          |
| Mark incomplete or placeholder content clearly                             | ✓ Strong | Actionable                |
| Before significant decisions, ask: "Am I the right entity to decide this?" | ✓ Strong | High-value autonomy check |

#### Domain-Specific Rules

| Rule                                                         | Rating   | Notes                                               |
| ------------------------------------------------------------ | -------- | --------------------------------------------------- |
| If this project has a praxis.yaml, check its domain field... | ~ Weak   | Complex conditional, but necessary for architecture |
| domain: code → @~/.claude/rules/code.md                      | ✓ Strong | Pointer, not copy (follows principles)              |
| domain: write → @~/.claude/rules/write.md                    | ✓ Strong | Pointer, not copy                                   |
| domain: create → @~/.claude/rules/create.md                  | ✓ Strong | Pointer, not copy                                   |

#### Summary: CLAUDE_model_user.md

- **Strong:** 21 rules
- **Weak:** 1 rule (domain conditional — necessary complexity)
- **Contrary:** 0 rules
- **Total:** 22 rules (~22 of 30-40 budget for user core)

### CLAUDE_model_user_code.md Analysis

#### Code Style

| Rule                                             | Rating   | Notes                    |
| ------------------------------------------------ | -------- | ------------------------ |
| Follow existing project conventions when present | ✓ Strong | Simple conditional       |
| Prefer readability over cleverness               | ✓ Strong | Clear preference         |
| Keep functions focused and small                 | ✓ Strong | Simple, positive         |
| Use meaningful variable names                    | ✓ Strong | Kept per user preference |

#### Analysis & Planning

| Rule                                                                     | Rating   | Notes                 |
| ------------------------------------------------------------------------ | -------- | --------------------- |
| Trace full call stacks before drawing conclusions                        | ✓ Strong | Specific, actionable  |
| Understand before fixing — a fix you don't understand becomes a timebomb | ✓ Strong | High-value, memorable |
| List everything that reads/writes/depends on code before changing it     | ✓ Strong | Specific, high-value  |

#### Testing

| Rule                                                           | Rating   | Notes                 |
| -------------------------------------------------------------- | -------- | --------------------- |
| Run tests after changes when a test suite exists               | ✓ Strong | Simple conditional    |
| Write failing tests first, then minimal code to pass           | ✓ Strong | Clear TDD instruction |
| For legacy code: add characterization tests before refactoring | ✓ Strong | Specific, actionable  |

#### Dependencies

| Rule                                                         | Rating   | Notes                                            |
| ------------------------------------------------------------ | -------- | ------------------------------------------------ |
| Verify library availability before using                     | ✓ Strong | Simple, positive (updated from negative framing) |
| Check package.json/pyproject.toml before adding dependencies | ✓ Strong | Specific, actionable                             |
| Prefer standard library solutions when reasonable            | ✓ Strong | Clear preference                                 |
| Justify new dependencies before adding them                  | ✓ Strong | Simple, positive                                 |

#### Safety

| Rule                                                                                 | Rating   | Notes                                                         |
| ------------------------------------------------------------------------------------ | -------- | ------------------------------------------------------------- |
| Preserve public APIs; note breaking changes explicitly                               | ✓ Strong | Clear, actionable                                             |
| Three real examples before abstracting patterns                                      | ✓ Strong | Specific, memorable rule                                      |
| Cannot explain why something exists? Cannot touch it until understanding is complete | ~ Weak   | Complex negative framing, but high-value (Chesterton's fence) |

#### Git

| Rule                                                                            | Rating   | Notes          |
| ------------------------------------------------------------------------------- | -------- | -------------- |
| Commit messages should be descriptive but concise, focusing on "why" not "what" | ✓ Strong | Clear guidance |

#### Summary: CLAUDE_model_user_code.md

- **Strong:** 16 rules
- **Weak:** 1 rule (Chesterton's fence — complex but high-value)
- **Contrary:** 0 rules
- **Total:** 17 rules (~17 of 40-60 budget for domain)

## Reusable Artifacts

### Changes Applied (2024-12-24)

1. ✅ **"Skip unnecessary preamble"** → "Get to the point"
2. ✅ **"macOS environment"** → Removed (can be detected)
3. ✅ **"Match existing code style"** → Removed (redundant)
4. ✅ **"Never assume a library is available"** → "Verify library availability before using"
5. ⏸️ **"Use meaningful variable names"** → Kept per user preference
6. ⏸️ **Domain conditional** → Kept (necessary complexity)
7. ⏸️ **Chesterton's fence rule** → Kept (high-value despite complex framing)

### Budget Assessment

| File                 | Rules | Budget | Status              |
| -------------------- | ----- | ------ | ------------------- |
| User core            | 22    | 30-40  | ✓ Under budget      |
| Code domain          | 17    | 40-60  | ✓ Well under budget |
| **Total user-level** | 39    | 70-100 | ✓ Healthy headroom  |

### Order Assessment

Both files place high-priority items first:

- User: Communication → Control Signals → Epistemic Honesty (all high-impact)
- Code: Code Style → Analysis & Planning → Testing (logical flow)

✓ Order follows first principles (earlier = higher priority)

## Overall Verdict

**Strong alignment with first principles.** Both files are:

- Under budget with room to grow
- Mostly positive framing
- High-signal, minimal filler
- Properly ordered (important stuff first)
- Using pointers for domain files (not inlining)

**After applying changes:** 37 strong rules, 2 weak (both intentionally kept for value/necessity).

---

_Migrated from research/ai-guards/analysis-user-models.md_
_Approved: 2025-12-30_
