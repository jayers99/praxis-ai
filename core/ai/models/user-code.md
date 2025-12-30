# Code Domain Rules

**User-Level Rules** — Apply to all code domain projects.

---

## Design & Planning

- Work in small, reversible increments; design feedback-driven through tests
- Use Plan Mode before starting non-trivial implementations
- Read architecture docs and CLAUDE.md before modifying code
- Anchor work with: goal, acceptance criteria, non-goals

---

## Analysis Before Change

- Read before modifying; understand existing code first
- Trace full call stacks and git history before conclusions
- List everything that reads/writes/depends on changed code before touching it
- Cannot explain why code exists? Cannot touch it until understanding is complete
- For legacy code without tests: add characterization tests first

---

## Code Quality

- Follow existing project conventions when present
- Prefer readability and simplicity over cleverness
- Keep functions focused and small; use meaningful variable names
- Preserve public APIs; note breaking changes explicitly
- Match existing code style and patterns

---

## Dependencies

- Check package.json/pyproject.toml before adding dependencies
- Prefer standard library solutions when reasonable
- Justify new dependencies before adding them
- Verify library availability before using

---

## Testing & Verification

- Run tests after changes when a test suite exists
- Write failing tests first, then minimal code to pass
- Run one test at a time; watch it pass before running the next
- Mark tests complete only after confirmed execution
- All new features require tests

### Verification Protocol
Format: "Ran [test name] — Result: [PASS/FAIL/DID NOT RUN]"

---

## Safety & Edge Cases

- Flag edge cases and add covering tests
- Silent fallbacks convert hard failures into data corruption; let it crash instead
- Alter runtime behavior only with proof of safety
- Pause before irreversible changes: data mutations, public API changes, git history rewrites

---

## Git & Commits

- Commit messages should be descriptive but concise, focusing on "why" not "what"
- Use granular commits; follow pattern: feat|fix|refactor|style|chore|docs
- Add files individually; never use `git add .`
- Never commit without passing tests
- Never commit changes unless explicitly asked

---

## Error Handling & Debugging

- Stop immediately when anything fails
- Explain reasoning: raw error, theory about cause, proposed action, expected outcome
- Maintain multiple competing theories simultaneously; never chase a single hypothesis
- Distinguish immediate cause from systemic cause from root cause
- Checkpoint in deep debugging: write down what's known

---

## Linting & Quality Gates

- Run linting, formatting, then tests after editing
- Demand diffs and test outputs before applying changes
- Double-check findings before implementation
