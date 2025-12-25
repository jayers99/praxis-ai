# Code Domain Rules

Apply these rules when working on projects with domain: code in praxis.yaml.

## Code Style

- Follow existing project conventions when present
- Prefer readability over cleverness
- Keep functions focused and small
- Use meaningful variable names

## Workflow

- Trace full call stacks before drawing conclusions
- Run tests after changes when a test suite exists
- Commit messages should be descriptive but concise

## Testing

- Write failing tests first, then minimal code to pass
- For legacy code: add characterization tests before refactoring

## Dependencies

- Never assume a library is available — check first
- Check package.json/pyproject.toml before adding dependencies
- Prefer standard library solutions when reasonable
- Justify new dependencies before adding them

## Git

- Never commit without passing tests
- Never commit unless explicitly asked
