# Execute (Code / CLI)

**Stage:** Execute

---

## Implementation checklist

- [ ] Set up project structure (hexagonal architecture)
- [ ] Configure tooling (Poetry, ruff, mypy)
- [ ] Implement core commands
- [ ] Add `--help` and `--version` flags
- [ ] Add JSON output support
- [ ] Add exit codes per spec
- [ ] Write tests (BDD + unit)
- [ ] Add documentation

## CLI entry points

- [ ] Console script configured in `pyproject.toml`
- [ ] `__main__.py` for `python -m` support

## Quality gates

- [ ] `poetry run pytest` passes
- [ ] `poetry run ruff check .` passes
- [ ] `poetry run mypy .` passes
- [ ] `tool --help` works
- [ ] `tool --version` works

## Validation

```bash
praxis validate .
praxis audit
```

---

## Exit criteria

- [ ] All commands implemented
- [ ] Tests passing
- [ ] Lint/type checks passing
- [ ] Help and version working
- [ ] Ready to move to Sustain
