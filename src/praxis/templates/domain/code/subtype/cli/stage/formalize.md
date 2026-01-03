# Formalize (Code / CLI)

**Stage:** Formalize

---

## CLI constraints

- Pipeline safety requirements:
- Backwards compatibility policy:
- Version scheme (semver?):
- Supported platforms:

## Command contract

<!-- Finalized command structure from Shape -->

### Commands

| Command | Required Flags | Optional Flags | Exit Codes |
|---------|----------------|----------------|------------|
| | | | |

### Global behavior

- Help flag: `--help` / `-h`
- Version flag: `--version` / `-v`
- JSON output: `--json`
- Quiet mode: `--quiet` / `-q`

## Error handling

<!-- How errors are formatted, exit codes -->

## Testing strategy

- Unit tests:
- Integration tests:
- BDD scenarios:

---

## Required artifact

- Ensure `docs/sod.md` is created and reflects the locked CLI scope.

## Exit criteria

- [ ] SOD created with CLI design locked
- [ ] Command contract documented
- [ ] Exit codes defined
- [ ] Testing strategy established
- [ ] Ready to move to Commit
