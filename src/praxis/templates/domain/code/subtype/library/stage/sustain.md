# Sustain (Code / Library)

**Stage:** Sustain

---

## Maintenance checklist

- [ ] Monitor for issues
- [ ] Review pull requests
- [ ] Update CHANGELOG for each release
- [ ] Follow semantic versioning
- [ ] Deprecate APIs before removal
- [ ] Keep dependencies up to date

## Release process

1. Update CHANGELOG.md
2. Bump version (semver)
3. Update `__version__` in code
4. Tag release
5. Build and publish package
6. Update documentation

## Breaking change process

- Deprecate in minor release (with warnings)
- Remove in next major release
- Document migration path

## Quality maintenance

- [ ] Tests remain passing
- [ ] Documentation stays current
- [ ] Coverage doesn't regress
- [ ] Performance benchmarks stable

---

## Exit criteria

- [ ] Library actively maintained
- [ ] Users getting support
- [ ] Quality gates enforced
