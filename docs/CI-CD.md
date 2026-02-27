# CI/CD and Release Process

This document describes the current and planned continuous integration, testing, and release processes for Praxis.

## Current Status: Manual Process

**As of January 2026, Praxis uses a manual development workflow with no automated CI/CD.**

### Required Checks Before Merge

All pull requests must pass these checks **manually** before merge:

```bash
# 1. Run all tests
poetry run pytest

# 2. Run linting
poetry run ruff check .

# 3. Run type checking
poetry run mypy .

# All checks must pass (exit code 0)
```

**Maintainer responsibility:** Verify that contributors have run these checks before merging.

**Contributor responsibility:** Run all checks locally and confirm in PR description that they pass.

## Current Release Process

**Status:** No formal releases yet (early-stage development)

**Installation method:** Clone repository + `poetry install` (development mode)

**Version management:**
- Version defined in `pyproject.toml` (currently `0.1.0`)
- No git tags or GitHub releases yet
- No PyPI publication yet

### Future Release Process (Planned)

When stable releases begin:

1. **Version bump:** Update version in `pyproject.toml` following semver
2. **Changelog:** Update CHANGELOG.md with release notes
3. **Git tag:** Create annotated tag (`git tag -a v0.1.0 -m "Release 0.1.0"`)
4. **GitHub Release:** Create release via GitHub UI with release notes
5. **PyPI publish:** `poetry publish --build` (requires PyPI credentials)
6. **Verification:** Install from PyPI and run smoke tests

## Planned CI/CD Automation

### Phase 1: GitHub Actions - Basic Checks (Planned)

**Workflow:** `.github/workflows/ci.yml` (not yet created)

**Triggers:**
- All pull requests
- Pushes to `main` branch

**Jobs:**
1. **Test Matrix:**
   - Python 3.10, 3.11, 3.12
   - Ubuntu (primary), macOS (secondary)
   - Windows (best-effort)

2. **Linting:**
   - `ruff check .` (must pass)

3. **Type Checking:**
   - `mypy .` (must pass)

4. **Coverage:**
   - `pytest --cov=praxis --cov-report=xml`
   - Upload to Codecov (or similar)
   - Enforce minimum coverage threshold (e.g., 80%)

**PR requirements:**
- All jobs must pass (green checkmark)
- At least one maintainer approval
- No merge conflicts

### Phase 2: Security Scanning (Planned)

**Additional checks:**

1. **Dependency scanning:**
   - Dependabot alerts enabled
   - `pip-audit` or `safety` in CI
   - Block PRs with known vulnerabilities (configurable)

2. **Secrets detection:**
   - `detect-secrets` or `gitleaks` pre-commit hook
   - Fail CI if secrets detected

3. **SBOM generation:**
   - Generate Software Bill of Materials on release
   - CycloneDX or SPDX format

### Phase 3: Release Automation (Planned)

**Automated release workflow:**

1. **Trigger:** Git tag push (`v*.*.*`)
2. **Build:** `poetry build` (wheel + sdist)
3. **Sign:** GPG or Sigstore signing
4. **Publish:** PyPI + GitHub Release
5. **Provenance:** SLSA attestation
6. **Notifications:** Announce in discussions/slack

## Dependency Management

### Lock File Strategy

- `poetry.lock` is committed to repository
- Lock file updated via:
  - `poetry add <package>` (new dependency)
  - `poetry update` (update all within semver ranges)
  - `poetry update <package>` (update specific package)

**Update cadence:**
- Security patches: As soon as available
- Minor/patch updates: Monthly or as needed
- Major updates: Evaluate impact, coordinate with releases

### Dependency Review Process

For new dependencies:

1. **Justification:** Why is this dependency needed?
2. **Alternatives:** Were alternatives considered?
3. **License:** Compatible with GPLv3?
4. **Maintenance:** Is it actively maintained?
5. **Security:** Known vulnerabilities? (check GitHub Advisories)
6. **Size:** What's the transitive dependency footprint?

Document in PR description when adding dependencies.

## Supply Chain Security

### Current Posture

- ✅ **Lock file:** Dependencies locked in `poetry.lock`
- ✅ **Semver constraints:** Defined in `pyproject.toml`
- ❌ **SBOM:** Not generated
- ❌ **Provenance:** No build attestation
- ❌ **Signing:** Releases not signed
- ❌ **Automated scanning:** No vulnerability CI checks

### Roadmap

- [ ] Implement GitHub Actions CI (Phase 1)
- [ ] Enable Dependabot for dependency updates
- [ ] Add `pip-audit` to CI
- [ ] Generate SBOM on release (CycloneDX format)
- [ ] Implement SLSA provenance attestation (Level 2+)
- [ ] Sign releases with GPG or Sigstore
- [ ] Document verification process for consumers

## Recommendations for Consumers

**If you're using Praxis in production:**

1. **Pin to a specific commit:**
   ```bash
   # Clone with specific commit
   git clone https://github.com/jayers99/praxis-ai.git
   cd praxis-ai
   git checkout <commit-sha>
   poetry install
   ```

2. **Verify integrity:**
   ```bash
   # Check git remote
   git remote -v
   
   # Verify commit (when GPG signing is implemented)
   git verify-commit HEAD
   
   # Run tests to verify functionality
   poetry run pytest
   ```

3. **Monitor for updates:**
   - Watch the repository for security advisories
   - Subscribe to release notifications
   - Review CHANGELOG.md before updating

4. **Run validation in CI:**
   ```bash
   # In your CI pipeline
   poetry run praxis validate --strict
   ```

5. **Audit dependencies periodically:**
   ```bash
   # Check for known vulnerabilities
   poetry run pip-audit  # (if installed)
   
   # Review dependency tree
   poetry show --tree
   ```

## Testing Strategy

### Test Pyramid

```
     /\
    /  \   E2E Tests (CLI integration)
   /----\
  /      \  Integration Tests (service layer)
 /--------\
/__________\ Unit Tests (domain models, validation)
```

**Current coverage:**
- Unit tests: Domain models, validators
- Integration tests: Service orchestration
- E2E tests: CLI commands via pytest-bdd

**Target coverage:** 80% overall, 90% for domain logic

### BDD with Gherkin

All user-facing features require Gherkin scenarios:

```gherkin
Feature: Stage Transition Validation
  Scenario: Cannot execute without formalize artifact
    Given a Code domain project at stage "execute"
    When I run "praxis validate"
    And no file exists at "docs/sod.md"
    Then the command should fail
    And the output should contain "Missing formalize artifact"
```

See `tests/features/` for examples.

## Build and Development Tools

| Tool | Purpose | Command |
|------|---------|---------|
| **Poetry** | Dependency management, packaging | `poetry install`, `poetry build` |
| **pytest** | Test runner | `poetry run pytest` |
| **pytest-bdd** | BDD testing with Gherkin | (integrated with pytest) |
| **ruff** | Linting (replaces flake8, black, isort) | `poetry run ruff check .` |
| **mypy** | Static type checking | `poetry run mypy .` |
| **coverage** | Test coverage reporting | `poetry run pytest --cov` |

**Future tools:**
- `pip-audit` or `safety` for vulnerability scanning
- `bandit` for security linting
- `detect-secrets` for secrets detection

## Questions and Improvements

**Want to help implement CI/CD?** See open issues labeled `infrastructure` and `automation`.

**Have suggestions for the release process?** Open an issue with the `process` label.

**Security concerns?** See [SECURITY.md](../SECURITY.md).
