# Contributing to Praxis-AI

Thank you for your interest in contributing to Praxis-AI! This document outlines the process for contributing and the terms under which contributions are accepted.

## Contributor License Agreement (CLA)

By submitting a pull request or otherwise contributing to this project, you agree to the following terms:

### 1. License Grant

You agree that your contributions are licensed under the [GNU General Public License v3.0](LICENSE) (GPLv3), the same license that covers this project. You retain copyright ownership of your contributions.

### 2. Grant of Patent License

You hereby grant to the Project Owner and to recipients of the software a perpetual, worldwide, non-exclusive, royalty-free, irrevocable patent license to make, have made, use, offer to sell, sell, import, and otherwise transfer your contributions, where such license applies only to patent claims licensable by you that are necessarily infringed by your contribution alone or in combination with the project.

### 3. Representations

You represent that:

- You are legally entitled to grant the above licenses
- If your employer has rights to intellectual property that you create, you have received permission to make contributions on behalf of that employer, or your employer has waived such rights
- Your contributions are your original work and do not violate any third-party rights
- You are not aware of any claims, suits, or actions pertaining to your contributions

### 4. No Obligation

You understand that your contributions are voluntary and that the Project Owner is under no obligation to accept, use, or include your contributions.

---

## How to Contribute

### Reporting Issues

- Use GitHub Issues to report bugs or suggest features
- Check existing issues before creating a new one
- Provide as much detail as possible
- Use issue templates when available

**For security vulnerabilities:** See [SECURITY.md](SECURITY.md) for private reporting instructions.

**Issue labels:**
- `maturity: raw|shaped|formalized` — Issue readiness level
- `size: small|medium|large` — Effort estimate
- `type: feature|spike|chore` — Work type
- `priority: high|medium|low` — Importance
- `security` — Security-related issues (non-vulnerabilities)
- `documentation` — Documentation improvements

See [CONTRIBUTING.md workflow section](CONTRIBUTING.md) for more details on the issue maturity model.

### Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Ensure your code follows existing patterns
5. **Add tests for new functionality** (see Testing Requirements below)
6. Run tests, linting, and type checking (see Local Development below)
7. Commit with clear messages
8. Push to your fork
9. Open a Pull Request

### Local Development Setup

**Prerequisites:**
- Python >=3.10
- Poetry (install via `pip install poetry` or see https://python-poetry.org/)
- Git

**Initial setup:**
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/praxis-ai.git
cd praxis-ai

# Install dependencies
poetry install

# Verify installation
poetry run praxis --version
```

**Running quality checks locally:**
```bash
# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest tests/features/test_validate.py

# Run tests with verbose output
poetry run pytest -v

# Run linting (code style checks)
poetry run ruff check .

# Auto-fix linting issues where possible
poetry run ruff check . --fix

# Run type checking
poetry run mypy .

# Run all checks (recommended before committing)
poetry run pytest && poetry run ruff check . && poetry run mypy .
```

**Debugging:**
```bash
# Run tests with debugging output
poetry run pytest -vv -s

# Run specific test scenario by name
poetry run pytest -k "test_scenario_name"
```

### Testing Requirements

This project uses **Behavior-Driven Development (BDD)** with Gherkin feature files:

- **All new features require Gherkin acceptance criteria**
- Feature files go in `tests/features/`
- Step definitions go in `tests/step_defs/`
- Use Given-When-Then format for test scenarios
- Follow existing feature files as examples

**Running tests:**
```bash
poetry run pytest                    # Run all tests
poetry run pytest tests/features/    # Run BDD tests only
poetry run ruff check .              # Linting
poetry run mypy .                    # Type checking
```

**Example Gherkin scenario:**
```gherkin
Scenario: Validate project at Execute stage requires SOD
  Given a praxis project at stage "execute" with domain "code"
  When I run "praxis validate"
  And no file exists at "docs/sod.md"
  Then the command should fail
  And the output should contain "Missing formalize artifact"
```

### Pull Request Process

1. PRs should target the `main` branch
2. Include a clear description of changes
3. Reference any related issues
4. **All CI checks must pass** (when CI is implemented)
5. Wait for review and address feedback
6. Squash commits if requested

**Current CI status:** Manual review only. GitHub Actions CI is planned but not yet implemented. You must run tests, linting, and type checking locally before submitting.

---

## Security and Responsible Development

### Secrets and Credentials

**Never commit secrets, credentials, or sensitive data to the repository.**

This includes:
- API keys, tokens, passwords
- Private keys, certificates
- Personal identifiable information (PII)
- Proprietary data or code from other sources
- Environment-specific configuration with sensitive values

**Best practices:**
- Use environment variables for secrets (`.env` files, not committed)
- Add sensitive file patterns to `.gitignore`
- Review your commits before pushing (`git diff --cached`)
- Use `git log -p` to audit recent commits
- If you accidentally commit a secret, notify maintainers immediately

**If a secret is committed:**
1. DO NOT just delete it in a new commit (it remains in git history)
2. Notify maintainers via the security contact (see SECURITY.md)
3. Rotate/revoke the exposed credential immediately
4. Maintainers may need to rewrite git history or rotate repo keys

### Dependency Management

**When adding or updating dependencies:**
- Add dependencies via `poetry add <package>`
- Update `poetry.lock` by running `poetry update` or `poetry lock`
- Commit both `pyproject.toml` and `poetry.lock` changes
- Document why the dependency is needed in PR description
- Check for known vulnerabilities (planned: automated scanning)

**Avoid:**
- Directly editing `pyproject.toml` without running `poetry lock`
- Adding dependencies with wildcard versions (`*`)
- Including development-only dependencies in production dependencies

### Code Review for Security

When reviewing PRs, consider:
- Does this change handle user input safely?
- Are file paths validated to prevent directory traversal?
- Are shell commands constructed safely (avoid shell injection)?
- Does privacy level enforcement remain intact?
- Are new dependencies from trusted sources?

---

## Code of Conduct

Be respectful, constructive, and professional. We're here to build something useful together.

---

## Questions?

Open an issue or reach out to the project owner.

---

*By submitting a contribution, you acknowledge that you have read and agree to the terms of this Contributor License Agreement. All contributions are licensed under GPLv3.*
