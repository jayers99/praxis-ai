# Execute (Code / Library)

**Stage:** Execute

---

## Implementation checklist

- [ ] Set up project structure
- [ ] Configure tooling (Poetry, ruff, mypy)
- [ ] Implement public API
- [ ] Add `__version__` to package
- [ ] Define `__all__` exports
- [ ] Write docstrings for all public APIs
- [ ] Write tests (unit + integration)
- [ ] Create usage examples
- [ ] Set up documentation site

## Library structure

- [ ] Package with `__init__.py` defining `__all__`
- [ ] `__version__` variable in sync with pyproject.toml
- [ ] Public API clearly separated from internals

## Quality gates

- [ ] `uv run pytest` passes
- [ ] `uv run ruff check .` passes
- [ ] `uv run mypy .` passes
- [ ] Coverage meets threshold
- [ ] All public APIs documented

## Validation

```bash
praxis validate .
praxis audit
```

---

## Exit criteria

- [ ] All public APIs implemented
- [ ] Tests passing
- [ ] Lint/type checks passing
- [ ] Documentation complete
- [ ] Ready to move to Sustain
