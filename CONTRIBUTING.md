# Contributing to Praxis-AI

Thank you for your interest in contributing to Praxis-AI! This document outlines the process for contributing and the terms under which contributions are accepted.

## Contributor License Agreement (CLA)

By submitting a pull request or otherwise contributing to this project, you agree to the following terms:

### 1. Grant of Copyright License

You hereby grant to the Project Owner (the owner of the GitHub repository at https://github.com/jayers99/praxis-ai) a perpetual, worldwide, non-exclusive, royalty-free, irrevocable copyright license to:

- Reproduce, prepare derivative works of, publicly display, publicly perform, sublicense, and distribute your contributions and any derivative works thereof
- Incorporate your contributions into the project under any license, including licenses different from the current project license

### 2. Grant of Patent License

You hereby grant to the Project Owner a perpetual, worldwide, non-exclusive, royalty-free, irrevocable patent license to make, have made, use, offer to sell, sell, import, and otherwise transfer your contributions, where such license applies only to patent claims licensable by you that are necessarily infringed by your contribution alone or in combination with the project.

### 3. Representations

You represent that:

- You are legally entitled to grant the above licenses
- If your employer has rights to intellectual property that you create, you have received permission to make contributions on behalf of that employer, or your employer has waived such rights
- Your contributions are your original work and do not violate any third-party rights
- You are not aware of any claims, suits, or actions pertaining to your contributions

### 4. Right to Relicense

You understand and agree that the Project Owner may, at their sole discretion, change the license of the project (including your contributions) at any time, without notice to you.

### 5. No Obligation

You understand that your contributions are voluntary and that the Project Owner is under no obligation to accept, use, or include your contributions.

---

## How to Contribute

### Reporting Issues

- Use GitHub Issues to report bugs or suggest features
- Check existing issues before creating a new one
- Provide as much detail as possible

### Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Ensure your code follows existing patterns
5. **Add tests for new functionality** (see Testing Requirements below)
6. Run tests, linting, and type checking
7. Commit with clear messages
8. Push to your fork
9. Open a Pull Request

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
4. Wait for review and address feedback

---

## Code of Conduct

Be respectful, constructive, and professional. We're here to build something useful together.

---

## Questions?

Open an issue or reach out to the project owner.

---

*By submitting a contribution, you acknowledge that you have read and agree to the terms of this Contributor License Agreement.*
