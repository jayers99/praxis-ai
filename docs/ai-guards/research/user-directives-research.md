# CLAUDE.md Directives Research

**Purpose:** Comprehensive list of directives from Claude Code experts and power users.
**Date:** 2024-12-24
**Sources:** GitHub gists, blogs, guides, and community best practices

---

## How to Use This Document

Review these directives and consider which ones to include in your user-level CLAUDE.md. Group them by category, evaluate against first principles (simple, positive, under budget), and select the highest-signal ones.

---

## 1. Communication & Interaction Style

### Conciseness

- [ ] Be direct and concise
- [ ] Skip unnecessary preamble
- [ ] Avoid unnecessary praise or filler
- [ ] Never say "you're absolutely right"

### Clarity

- [ ] Provide working code, not explanations of what you could do
- [ ] Ask clarifying questions when requirements are ambiguous
- [ ] When confused: stop, think, present theories, get signoff
- [ ] Surface disagreements explicitly rather than silently choosing interpretation

### Control Signals

- [ ] "Stop" = halt immediately, wait for instructions
- [ ] "Pause" = checkpoint progress, summarize state, wait
- [ ] "Clarify" = I need to understand before you proceed

### Epistemic Honesty

- [ ] "I believe X" ≠ "I verified X"
- [ ] "I don't know" beats confident guessing
- [ ] One example is anecdote, three is maybe a pattern
- [ ] Uncertain + consequential → ask first
- [ ] Express uncertainty rather than hiding it
- [ ] Never use "ALL/ALWAYS/NEVER" without exhaustive proof

---

## 2. Planning & Approach

### Before Starting

- [ ] Use Plan Mode for non-trivial implementations
- [ ] Request 3-6 step proposals with confirmation before coding
- [ ] Anchor with architecture docs and task-specific brief (goal, acceptance criteria, non-goals)
- [ ] Read CLAUDE.md, README.md, then code (documentation first)

### Analysis First

- [ ] Read before modifying - understand existing code first
- [ ] Trace full call stacks before conclusions
- [ ] Understand before fixing (fix you don't understand becomes timebomb)
- [ ] Ask "why" five times for root cause analysis

### Scope Control

- [ ] Make minimal changes to accomplish the task
- [ ] Keep solutions simple and focused on the current problem
- [ ] Scope changes to the task at hand
- [ ] Incremental progress over big changes

---

## 3. Code Quality & Style

### General

- [ ] Follow existing project conventions when present
- [ ] Prefer readability over cleverness
- [ ] Keep functions focused and small
- [ ] Use meaningful variable names
- [ ] Match existing code style

### Dependencies

- [ ] Justify new dependencies before adding them
- [ ] Prefer standard library solutions when reasonable
- [ ] Never assume a library is available - check first
- [ ] Check package.json before adding dependencies

### Safety

- [ ] Preserve public APIs; note breaking changes explicitly
- [ ] Don't alter runtime behavior without proof of safety
- [ ] Flag edge cases and add covering tests
- [ ] Silent fallbacks convert hard failures into corruption - let it crash

---

## 4. Testing & Verification

### Test-Driven Development

- [ ] Write failing tests first, then minimal code to pass
- [ ] Run tests after changes when a test suite exists
- [ ] For legacy code: add characterization tests before refactoring
- [ ] All new features require tests

### Verification Protocol

- [ ] Run one test at a time, watch it pass before next
- [ ] Never write multiple tests before running any
- [ ] Never .skip() without understanding failure
- [ ] Mark tests complete only after confirmed execution
- [ ] VERIFY format: "Ran [test name] — Result: [PASS/FAIL/DID NOT RUN]"

### Quality Gates

- [ ] Run linting, formatting, then tests after editing
- [ ] Demand diffs and tests; review outputs before applying
- [ ] Double-check findings before implementation

---

## 5. Git & Version Control

### Commits

- [ ] Commit messages should be descriptive but concise
- [ ] Focus on "why" not "what"
- [ ] Never commit without passing tests
- [ ] Never commit changes unless explicitly asked
- [ ] Use granular commits (feat|fix|refactor|style|chore|docs)
- [ ] git add files individually - never `git add .`

### Safety

- [ ] Never push (human responsibility only)
- [ ] Never --force, reset --hard, or amend others' commits
- [ ] Check git status; prompt to commit if working tree dirty

### Branch Naming

- [ ] Branches: `feature/STORY-N-description`, `bugfix/BUG-N-description`, `chore/CHORE-N-description`

---

## 6. Error Handling & Debugging

### When Errors Occur

- [ ] Stop immediately when anything fails
- [ ] Explain reasoning, wait for confirmation before proceeding
- [ ] State: raw error, theory about cause, proposed action, expected outcome

### Investigation Protocol

- [ ] Maintain 5+ competing theories simultaneously
- [ ] Never chase single hypothesis
- [ ] Create investigation documents separating FACTS from THEORIES
- [ ] Test one theory at a time

### Root Cause Analysis

- [ ] Distinguish immediate cause from systemic cause from root cause
- [ ] Understand before fixing
- [ ] Checkpoint in deep debugging: write down what's known

---

## 7. Context & Memory Management

### Context Awareness

- [ ] Scroll back to original constraints every ~10 actions
- [ ] Notice signs of degradation: sloppier outputs, forgotten goals, repeated work
- [ ] Say "losing the thread" when coherence declines
- [ ] Context window is not reliable memory

### Checkpoints

- [ ] Batch size: maximum 3 actions before checkpoint
- [ ] Max 5 actions without verification before stopping
- [ ] Every ~10 actions: verify original goal still understood

### Session Handoff

- [ ] State work status (done/in progress/untouched)
- [ ] List current blockers and why stopped
- [ ] Document open questions and unresolved ambiguities
- [ ] Provide recommendations with reasoning
- [ ] List files created, modified, or deleted

---

## 8. Safety & Boundaries

### Autonomy Limits

- [ ] Before significant decisions, ask: "Am I the right entity to decide this?"
- [ ] Punt to user for: ambiguous intent, unexpected state, irreversible actions, scope changes
- [ ] Pause before irreversible actions (database schemas, public APIs, data deletion, git history)

### Code Archaeology

- [ ] Cannot explain why something exists? Cannot touch it until understanding is complete
- [ ] Trace references and git history before claiming code is unused
- [ ] List everything that reads/writes/depends on changed code before touching anything
- [ ] Prove "nothing else uses this" rather than assuming it

### Three Examples Rule

- [ ] Three real examples before abstracting patterns
- [ ] Write code twice, consider abstracting on third iteration

---

## 9. Tool & File Preferences

### File Discovery

- [ ] Use Glob and LS tools for file/directory searches
- [ ] Avoid Bash(grep), Bash(find) in favor of dedicated tools

### File Editing

- [ ] Read file headers for follow-up actions (e.g., schema regeneration scripts)
- [ ] Reload files before making edits
- [ ] Reference exact file paths with minimal surrounding code
- [ ] Return unified diffs touching only specified files

### Environment

- [ ] Use project-specified tooling over personal preferences
- [ ] macOS environment (or specify yours)

---

## 10. Documentation & Output

### Code Documentation

- [ ] Mark incomplete or placeholder code clearly
- [ ] Place imports at file top unless circular dependencies
- [ ] Add function signatures for new code

### Change Documentation

- [ ] Keep atomic commits with clear messaging
- [ ] Update task tracking files upon completion
- [ ] Remind to verify, approve, and commit changes in task summary

---

## 11. Workflow Patterns (Advanced)

### Prediction-Verification Loop

- [ ] Write explicit predictions: DOING / EXPECT / IF YES / IF NO
- [ ] Execute the tool call
- [ ] Compare immediately: RESULT / MATCHES / THEREFORE
- [ ] Stop if unexpected

### Second-Order Effects

- [ ] List everything that reads/writes/depends on changed code before touching
- [ ] Design one-way doors for undo capability

### Investigation Documents

- [ ] Separate FACTS from THEORIES
- [ ] Maintain competing hypotheses

---

## 12. Project-Specific (Examples - Not for User-Level)

These are examples of project-specific directives that belong in project CLAUDE.md, not user-level:

- Use TailwindCSS v4 syntax exclusively
- Centralize types in src/types.ts
- Use tsconfig path aliases; never use relative paths
- Lighthouse scores >92 across all categories
- WCAG 2.1 AA compliance

---

## Sources

- [ctoth's Global CLAUDE.md](https://gist.github.com/ctoth/d8e629209ff1d9748185b9830fa4e79f) — Extensive epistemic and verification rules
- [tsdevau's Claude Rules Template](https://gist.github.com/tsdevau/673876d17d344f97ba3473bc081bd1e5) — Project template with validation checkpoints
- [awesome-claude-md](https://github.com/josix/awesome-claude-md) — Curated collection of exemplary files
- [Harper Reed's Blog](https://harper.blog/2025/05/08/basic-claude-code/) — TDD and stylistic preferences
- [Sidetool Power Users Guide](https://www.sidetool.co/post/claude-code-best-practices-tips-power-users-2025/)
- [Huikang's Mature Codebase Guide](https://blog.huikang.dev/2025/05/31/writing-claude-md.html)
- [Paul Brodner's Tips & Tricks](https://paulbrodner.github.io/2025/claude-code-tips-tricks/)
- [JohnOct's Lessons Learned](https://johnoct.github.io/blog/2025/08/01/claude-code-best-practices-lessons-learned/)
- [Anthropic's Official Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [HumanLayer's CLAUDE.md Guide](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
