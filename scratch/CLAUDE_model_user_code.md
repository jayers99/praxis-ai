# Code Domain Rules

Apply these rules when working on projects with domain: code in praxis.yaml.

## Planning & Approach

- Read before modifying — understand existing code first
- Use Plan Mode for non-trivial implementations
- Trace full call stacks before drawing conclusions

## Code Quality

- Follow existing project conventions when present
- Prefer readability over cleverness
- Keep functions focused and small
- Use meaningful variable names

## Testing

- Run tests after changes when a test suite exists
- Write failing tests first, then minimal code to pass
- For legacy code: add characterization tests before refactoring

## Dependencies

- Never assume a library is available — check first
- Check package.json/pyproject.toml before adding dependencies
- Prefer standard library solutions when reasonable

## Git

- Commit messages: brief, focusing on "why" not "what"
- Never commit without passing tests
- Never commit unless explicitly asked
