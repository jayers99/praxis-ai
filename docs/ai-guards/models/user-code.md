# Code Domain Rules

**User-Level Rules** — Apply to all code domain projects.

## Code Style

- Follow existing project conventions when present
- Prefer readability over cleverness
- Keep functions focused and small
- Use meaningful variable names

## Analysis & Planning

- Trace full call stacks before drawing conclusions
- Understand before fixing — a fix you don't understand becomes a timebomb
- List everything that reads/writes/depends on code before changing it

## Testing

- Run tests after changes when a test suite exists
- Write failing tests first, then minimal code to pass
- For legacy code: add characterization tests before refactoring

## Dependencies

- Verify library availability before using
- Check package.json/pyproject.toml before adding dependencies
- Prefer standard library solutions when reasonable
- Justify new dependencies before adding them

## Safety

- Preserve public APIs; note breaking changes explicitly
- Three real examples before abstracting patterns
- Cannot explain why something exists? Cannot touch it until understanding is complete

## Git

- Commit messages should be descriptive but concise, focusing on "why" not "what"
