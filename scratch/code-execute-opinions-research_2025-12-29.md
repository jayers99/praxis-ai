# Execute Stage Opinions Research: Python CLI

**Research Date:** 2025-12-29
**Scope:** Execute stage guidance for Code domain (Python CLI subtype)
**Influences:** Dave Farley, TDD, BDD, DDD, DevSecOps, SOLID, Clean Code
**Time Budget:** 120 minutes

---

## Consensus Strength Rubric

| Rating | Definition |
|--------|------------|
| **High** | Multiple authoritative sources agree; widely adopted in industry; supported by empirical studies |
| **Medium** | General agreement among experts; some variation in implementation details |
| **Low** | Emerging practice; conflicting opinions; context-dependent recommendations |

---

## 1. First Principles

### 1.1 The Execute Stage in Context

The Execute stage marks the transition from "what should we build?" to "build it reliably and repeatedly." This is where formalized designs become running software in production.

**Key Insight:** Execution is not merely deployment—it encompasses the entire cycle of building, testing, integrating, deploying, and monitoring production systems.

> "The Deployment Phase marks the pivotal moment when developed and tested software transitions from a controlled environment to production, becoming accessible to end users."
> — [Stratoflow SDLC Guide](https://stratoflow.com/software-deployment-phase/)

**Consensus Strength: High** — All major SDLC frameworks agree on this definition.

### 1.2 Continuous Delivery as Engineering Discipline

Dave Farley argues that Continuous Delivery (CD) represents a genuine engineering approach to software:

> "CD is founded on the application of scientific principles to solving problems in software: making evidence-based decisions, using falsification, forming hypotheses that are tested as (often automated) experiments, proceeding in small steps, validating learning as progress is made."
> — [Dave Farley, Modern Software Engineering](https://www.amazon.com/Modern-Software-Engineering-Discipline-Development/dp/0137314914)

**Core CD Principles for Execute Stage:**

| Principle | Application |
|-----------|-------------|
| Work so software is always releasable | Maintain deployable main branch at all times |
| Optimize for speed of feedback | Fast test suites, quick CI pipelines |
| Work in small batches | Small, frequent commits over large releases |
| Automate everything repeatable | CI/CD pipelines, deployment scripts |

**Consensus Strength: High** — Farley's principles are foundational to modern DevOps; supported by [DORA research](https://dora.dev/).

### 1.3 The Hexagonal Architecture Foundation

> "Allow an application to equally be driven by users, programs, automated test or batch scripts, and to be developed and tested in isolation from its eventual run-time devices and databases."
> — [Alistair Cockburn, original Ports & Adapters article (2005)](https://alistair.cockburn.us/hexagonal-architecture/)

For Python CLI applications, this architecture enables:
- **Testability:** Domain logic tested without invoking CLI
- **Flexibility:** Easy to swap infrastructure (file systems, APIs)
- **Clarity:** Clear boundaries between business logic and adapters

**Consensus Strength: High** — Widely adopted; documented in [AWS Prescriptive Guidance](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html) and [Architecture Patterns with Python (O'Reilly)](https://www.amazon.com/Architecture-Patterns-Python-Domain-Driven-Microservices/dp/1492052205).

---

## 2. Test-Driven Development (TDD)

### 2.1 The Red-Green-Refactor Cycle

Kent Beck's TDD discipline remains the gold standard for Execute stage quality:

> "TDD is a software development process where tests are written before the actual code. The workflow follows a simple cycle: Red — Write a test that fails. Green — Write the minimal code to make the test pass. Refactor — Clean up the code while keeping the test green."
> — [TestDriven.io, Modern TDD](https://testdriven.io/blog/modern-tdd/)

**Kent Beck's Two Rules:**
1. Write new code only if an automated test has failed
2. Eliminate duplication

**Consensus Strength: High** — Beck's original work (2002) remains authoritative; studies show 40–90% defect density reduction.

### 2.2 Test Pyramid Strategy

```
        /\
       /  \     E2E Tests (20%)
      /----\
     /      \   Integration Tests (30%)
    /--------\
   /          \ Unit Tests (50%)
  --------------
```

> "You should strive for your tests to resemble a pyramid shape (50% unit, 30% integration, 20% e2e). Although, in simple applications, it may look more like a house (40% unit, 40% integration, 20% e2e), which is fine."
> — [TestDriven.io](https://testdriven.io/blog/modern-tdd/)

**Consensus Strength: High** — Originally from Mike Cohn; widely adopted.

### 2.3 TDD Best Practices for Python CLI

| Practice | Rationale | Source |
|----------|-----------|--------|
| Test behavior, not implementation | Avoid brittle tests that break on refactoring | [TestDriven.io](https://testdriven.io/blog/modern-tdd/) |
| Keep tests atomic and isolated | Each test should run independently | [pytest-with-eric](https://pytest-with-eric.com/tdd/pytest-tdd/) |
| Tests should be fast | Quick feedback enables rapid iteration | [CodingNomads](https://codingnomads.com/python-301-test-driven-development-best-practices) |
| Tests should be idempotent | Same outcome every time | [pytest-with-eric](https://pytest-with-eric.com/tdd/pytest-tdd/) |
| Use Arrange–Act–Assert structure | Clarity and consistency | [DataCamp](https://www.datacamp.com/tutorial/test-driven-development-in-python) |
| Name tests descriptively | `should_calculate_total_with_tax` | [pytest-with-eric](https://pytest-with-eric.com/tdd/pytest-tdd/) |

**Consensus Strength: High** — Universal agreement across Python testing resources.

### 2.4 Coverage Philosophy

> "Try to keep it high but don't add tests just to have 100% coverage. A test is valuable only when it protects you against regressions, allows you to refactor, and provides you fast feedback."
> — [TestDriven.io](https://testdriven.io/blog/modern-tdd/)

**Recommendation:** Aim for meaningful coverage + mutation testing, not arbitrary percentage targets.

**Consensus Strength: Medium** — Agreement on avoiding 100% as vanity metric; variation on specific thresholds.

---

## 3. Behavior-Driven Development (BDD)

### 3.1 pytest-bdd for Python

> "pytest-bdd implements a subset of the Gherkin language to enable automating project requirements testing and to facilitate behavioral driven development. Unlike many other BDD tools, it does not require a separate runner and benefits from the power and flexibility of pytest."
> — [PyPI pytest-bdd](https://pypi.org/project/pytest-bdd/)

**Key Benefits:**
- Readable tests in plain English (Gherkin syntax)
- Living documentation (feature files serve as specs)
- Reusable step definitions
- Full pytest plugin ecosystem access (800+ plugins)

**Consensus Strength: High** — pytest-bdd is the dominant BDD framework for Python; integrates seamlessly with pytest.

### 3.2 Gherkin Structure

```gherkin
Feature: User authentication
  As a user
  I want to log in securely
  So that I can access my account

  Scenario: Successful login with valid credentials
    Given a registered user exists
    When the user provides valid credentials
    Then the user should be authenticated
    And redirected to the dashboard
```

**Best Practices:**
- Use Given-When-Then consistently
- Keep scenarios focused on one behavior
- Parameterize with Scenario Outlines for variations
- Share step definitions across features

**Consensus Strength: High** — Gherkin syntax is standardized across BDD tools.

### 3.3 pytest-bdd vs Behave

| Factor | pytest-bdd | Behave |
|--------|------------|--------|
| Parallel execution | Excellent (pytest-xdist) | Limited |
| Plugin ecosystem | 800+ pytest plugins | Smaller ecosystem |
| Fixture reuse | Native pytest fixtures | Separate context |
| Learning curve | Familiar to pytest users | Separate paradigm |

> "If parallel test execution is an important factor, Pytest will definitely be the better choice."
> — [Codoid](https://codoid.com/automation-testing/pytest-bdd-vs-behave-pick-the-best-python-bdd-framework/)

**Consensus Strength: High** — pytest-bdd preferred for teams already using pytest.

---

## 4. Domain-Driven Design (DDD)

### 4.1 When to Apply DDD

> "Some practices presented here are not recommended for small-medium sized applications with not a lot of business logic. There is added up-front complexity to support all those building blocks and layers, boilerplate code, abstractions, data mapping etc."
> — [Sairyss/domain-driven-hexagon](https://github.com/Sairyss/domain-driven-hexagon)

**Consensus Strength: High** — Universal agreement that DDD is overhead for simple CRUD applications.

### 4.2 DDD + Hexagonal for Python CLI

> "DDD focuses on modeling the core domain and isolating business logic, while Hexagonal Architecture ensures this logic remains independent of external systems through ports and adapters."
> — [DEV Community](https://dev.to/hieutran25/building-maintainable-python-applications-with-hexagonal-architecture-and-domain-driven-design-chp)

**CLI Architecture Mapping:**

```
src/package_name/
├── domain/           # Pure business logic (Entities, Value Objects)
│   ├── models.py     # Domain models (Pydantic recommended)
│   └── services.py   # Domain services
├── application/      # Use cases (orchestration)
│   └── *_service.py  # Application services (verbs)
├── infrastructure/   # External concerns (adapters)
│   ├── file_system.py
│   ├── api_client.py
│   └── config.py
└── cli.py            # Thin CLI adapter (Typer)
```

**Key DDD Concepts for CLI:**

| Concept | CLI Application |
|---------|-----------------|
| Ubiquitous Language | Consistent naming between CLI commands and domain |
| Bounded Context | Clear module boundaries |
| Entities | Objects with identity (e.g., `Project`, `User`) |
| Value Objects | Immutable objects (e.g., `FilePath`, `Version`) |
| Aggregates | Consistency boundaries for transactions |

**Consensus Strength: Medium** — DDD principles apply, but full tactical patterns (Aggregates, Repositories) may be overkill for most CLIs.

### 4.3 Reference Implementation

- [python-hexagonal-ddd](https://github.com/HieuTranV/python-hexagonal-ddd) — Full Python implementation
- [Architecture Patterns with Python](https://www.amazon.com/Architecture-Patterns-Python-Domain-Driven-Microservices/dp/1492052205) — O'Reilly book by Percival & Gregory

**Consensus Strength: High** — These are canonical Python DDD resources.

---

## 5. SOLID Principles

### 5.1 Overview

> "SOLID is an acronym representing five fundamental object-oriented design principles formulated by Robert C. Martin, also known as Uncle Bob."
> — [Real Python](https://realpython.com/solid-principles-python/)

### 5.2 Principles Applied to Python CLI

| Principle | Definition | CLI Example |
|-----------|------------|-------------|
| **S**ingle Responsibility | One reason to change | Separate `ValidateService` from `InitService` |
| **O**pen/Closed | Open for extension, closed for modification | Plugin architecture for new commands |
| **L**iskov Substitution | Subtypes substitutable for base types | `FileWriter` interface with `LocalFileWriter`, `S3FileWriter` |
| **I**nterface Segregation | Don't force unused dependencies | Separate `Readable`, `Writable` protocols |
| **D**ependency Inversion | Depend on abstractions | Domain depends on `ConfigLoader` protocol, not `YamlLoader` |

**Consensus Strength: High** — SOLID is foundational OOP; extensively documented in [Real Python](https://realpython.com/solid-principles-python/) and [Clean Architecture (Martin)](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164).

### 5.3 Python-Specific Patterns

Use Python's **Protocol** (PEP 544) for structural subtyping:

```python
from typing import Protocol

class ConfigLoader(Protocol):
    def load(self, path: Path) -> Config: ...

class YamlLoader:
    def load(self, path: Path) -> Config:
        # YAML-specific implementation
        ...
```

**Consensus Strength: High** — Protocol is the Pythonic way to implement interface segregation.

---

## 6. Clean Code Principles

### 6.1 Core Philosophy

> "Developers spend way more time reading code than actually writing it, which is why it's important to write good code. Writing code is easy, but writing good, clean code is hard."
> — [TestDriven.io](https://testdriven.io/blog/clean-code-python/)

### 6.2 Naming Conventions (PEP 8)

| Element | Convention | Example |
|---------|------------|---------|
| Variables, functions | `snake_case` | `calculate_total` |
| Classes | `CapWords` | `ValidationResult` |
| Constants | `UPPER_SNAKE` | `MAX_RETRIES` |
| Private members | `_leading_underscore` | `_internal_state` |
| Module-level dunder | `__dunder__` | `__version__` |

> "One of Guido's key insights is that code is read much more often than it is written."
> — [PEP 8](https://peps.python.org/pep-0008/)

**Consensus Strength: High** — PEP 8 is the authoritative Python style guide.

### 6.3 Clean Code Hallmarks

| Hallmark | Description |
|----------|-------------|
| Descriptive names | Intention-revealing identifiers |
| Modular design | Minimal dependencies between components |
| DRY (Don't Repeat Yourself) | Refactor to avoid duplication |
| Simplicity | Minimize complexity and cognitive load |
| Readability | Follow standard conventions, proper whitespace |

**Consensus Strength: High** — Universal agreement; codified in [zedr/clean-code-python](https://github.com/zedr/clean-code-python).

### 6.4 Code Smells and Refactoring

> "A code smell is a surface indication that usually corresponds to a deeper problem in the system."
> — [Martin Fowler](https://martinfowler.com/bliki/CodeSmell.html)

**Common Code Smells:**

| Smell | Symptom | Refactoring |
|-------|---------|-------------|
| Long Method | >20 lines | Extract Method |
| Large Class | Too many responsibilities | Extract Class |
| Long Parameter List | >3 parameters | Introduce Parameter Object |
| Duplicate Code | Copy-paste patterns | Extract Method/Class |
| Feature Envy | Method uses another class's data | Move Method |

**Reference:** [Refactoring (Fowler, 2nd ed.)](https://martinfowler.com/books/refactoring.html), [refactoring.guru/smells](https://refactoring.guru/refactoring/smells)

**Consensus Strength: High** — Fowler's catalog is definitive.

---

## 7. DevSecOps Practices

### 7.1 Security Testing Types

| Type | When | Tools | Purpose |
|------|------|-------|---------|
| **SAST** | Build time | Bandit, Semgrep, SonarQube | Find vulnerabilities in source code |
| **SCA** | Build time | Trivy, Safety, pip-audit | Check dependencies for CVEs |
| **DAST** | Runtime | OWASP ZAP, Burp Suite | Test running application |
| **Secrets** | Pre-commit | GitLeaks, TruffleHog | Prevent credential leaks |

> "For SAST, Python offers Bandit, a powerful tool for detecting vulnerabilities in Python codebases."
> — [Medium DevSecOps Guide](https://medium.com/@mrugaja3ri/devsecops-pipelines-with-python-how-to-integrate-security-tools-056171b5ef62)

**Consensus Strength: High** — These categories and tools are industry standard.

### 7.2 Shift Left Security

> "Shift left — integrate tools as early in the pipeline as possible; Automate everything — manual security checks slow pipelines; Run in parallel — don't bottleneck deployments with non-blocking checks."
> — [Pynt DevSecOps Guide](https://www.pynt.io/learning-hub/devsecops/devsecops-principles-tools-and-best-practices-2025-guide)

**Pipeline Integration Points:**

```
Pre-commit → SAST, Secrets scanning
Build → SAST, SCA, License compliance
Test → Unit, Integration, E2E
Deploy → DAST, Container scanning
Runtime → Monitoring, Alerting
```

**Consensus Strength: High** — Shift-left is universally recommended.

### 7.3 Python-Specific Security Tools

| Tool | Purpose | Integration |
|------|---------|-------------|
| [Bandit](https://bandit.readthedocs.io/) | SAST for Python | `bandit -r src/` |
| [Safety](https://pyup.io/safety/) | Dependency CVE check | `safety check` |
| [pip-audit](https://pypi.org/project/pip-audit/) | Dependency audit | `pip-audit` |
| [Semgrep](https://semgrep.dev/) | Code pattern matching | `semgrep --config auto` |

**Consensus Strength: High** — Bandit and Safety are standard Python security tools.

---

## 8. CI/CD Pipeline Design

### 8.1 GitHub Actions for Python (2025)

> "In 2025, the current recommended tools for setting up a Python project and running continuous integration via GitHub Actions revolve significantly around recently introduced tools by Astral."
> — [ber2.github.io](https://ber2.github.io/posts/2025_github_actions_python/)

**Recommended 2025 Stack:**
- **uv** (Astral) for fast dependency management
- **ruff** (Astral) for linting and formatting
- **pytest** for testing
- **mypy** for type checking

**Consensus Strength: Medium** — uv is emerging; Poetry remains widely used.

### 8.2 Pipeline Stages

```yaml
jobs:
  quality:
    steps:
      - Checkout
      - Setup Python (matrix: 3.10, 3.11, 3.12)
      - Install dependencies
      - Lint (ruff check)
      - Type check (mypy)
      - Test (pytest with coverage)
      - Security scan (bandit, safety)

  deploy:
    needs: quality
    steps:
      - Build package
      - Publish to PyPI
```

**Consensus Strength: High** — Standard pipeline structure.

### 8.3 Matrix Testing

> "Run tests across multiple Python versions (e.g., 3.8, 3.10) to catch incompatibilities early using tools like tox or matrix builds in GitHub Actions."
> — [Atmosly CI/CD Guide](https://atmosly.com/blog/python-ci-cd-pipeline-mastery-a-complete-guide-for-2025)

**Consensus Strength: High** — Matrix testing is standard practice.

---

## 9. CLI Testing Patterns

### 9.1 Typer CliRunner

> "Import CliRunner and create a runner object. This runner is what will 'invoke' or 'call' your command line application."
> — [Typer Testing Docs](https://typer.tiangolo.com/tutorial/testing/)

**Basic Pattern:**

```python
from typer.testing import CliRunner
from myapp.cli import app

runner = CliRunner()

def test_validate_command():
    result = runner.invoke(app, ["validate", "."])
    assert result.exit_code == 0
    assert "Valid" in result.stdout
```

**Consensus Strength: High** — This is the canonical Typer testing approach.

### 9.2 Separating stdout/stderr

> "By default, CliRunner is created with mix_stderr=True. Recommended practice: Verify separately the content of stdout and stderr."
> — [Typer Testing Docs](https://typer.tiangolo.com/tutorial/testing/)

```python
runner = CliRunner(mix_stderr=False)
result = runner.invoke(app, ["command"])
assert "data" in result.stdout
assert "warning" in result.stderr
```

**Consensus Strength: High** — Best practice for CLI testing.

### 9.3 Isolated Filesystem

> "For basic command line tools with file system operations, the CliRunner.isolated_filesystem() method is useful for setting the current working directory to a new, empty folder."
> — [Typer Testing Docs](https://typer.tiangolo.com/tutorial/testing/)

**Consensus Strength: High** — Standard practice for file-manipulating CLIs.

---

## 10. Observability & Monitoring

### 10.1 The Three Pillars

> "The three pillars of observability are: 1) structured logging, 2) metrics, and 3) tracing."
> — [Speaker Deck](https://speakerdeck.com/braz/adding-the-three-pillars-of-observability-to-your-python-app)

**For CLI applications, logging is the primary pillar.**

### 10.2 Structured Logging

> "With structured logging, it becomes a queryable timeline of events that supports effective debugging and operational insight."
> — [Dash0 Logging Guide](https://www.dash0.com/guides/logging-in-python)

**Environment-Specific Configuration:**

| Environment | Format | Purpose |
|-------------|--------|---------|
| Development | Colored, human-readable | Easy debugging |
| Production | JSON (structured) | Machine-parseable for observability tools |

**Recommended Libraries:**
- [structlog](https://www.structlog.org/) — Rich, queryable structured logs
- [loguru](https://github.com/Delgan/loguru) — Simple, powerful logging

**Consensus Strength: High** — Structured logging is the modern standard.

### 10.3 Logging Best Practices

| Practice | Rationale |
|----------|-----------|
| Include context (request_id, user_id) | Trace operations across components |
| Use appropriate log levels | DEBUG/INFO/WARNING/ERROR/CRITICAL |
| Don't log sensitive data | Security and compliance |
| Decouple logging config from code | Environment-specific behavior |

**Consensus Strength: High** — Universal agreement.

---

## 11. Design Patterns for Python CLI

### 11.1 Gang of Four Patterns (GoF)

> "Design patterns are largely language-agnostic. They are conceptual blueprints and principles for solving design problems."
> — [DigitalOcean GoF Guide](https://www.digitalocean.com/community/tutorials/gangs-of-four-gof-design-patterns)

**Most Relevant for CLI:**

| Pattern | Category | CLI Use Case |
|---------|----------|--------------|
| **Strategy** | Behavioral | Different output formats (JSON, YAML, table) |
| **Command** | Behavioral | CLI command encapsulation |
| **Factory** | Creational | Create services based on config |
| **Adapter** | Structural | Integrate external APIs |
| **Decorator** | Structural | Add logging, timing to functions |

**Consensus Strength: High** — GoF patterns are foundational (1994).

### 11.2 Python-Specific Idioms

Python's dynamic nature enables simpler patterns:

| GoF Pattern | Pythonic Alternative |
|-------------|---------------------|
| Singleton | Module-level instance |
| Strategy | First-class functions |
| Factory | `__init__` with class methods |
| Iterator | Generators (`yield`) |

**Consensus Strength: High** — Documented in [python.org workshop proceedings](https://legacy.python.org/workshops/1997-10/proceedings/savikko.html).

---

## 12. Deployment & Production

### 12.1 Deployment Strategies

| Strategy | Risk | Rollback | Use Case |
|----------|------|----------|----------|
| Big Bang | High | Difficult | Small teams, simple apps |
| Rolling | Medium | Good | Zero-downtime requirement |
| Blue-Green | Low | Instant | Production-critical systems |
| Canary | Low | Good | Feature validation |

> "Blue-Green deployment maintains two identical production environments for instant rollback capability."
> — [NinjaOne Deployment Guide](https://www.ninjaone.com/blog/software-deployment-best-practices/)

**Consensus Strength: High** — These strategies are industry standard.

### 12.2 Post-Deployment Monitoring

> "Real-time monitoring of the software's performance, use, and any faults is essential."
> — [OpenMindt Deployment Guide](https://www.openmindt.com/knowledge/top-10-steps-for-a-successful-software-deployment-process/)

**Key Metrics:**
- Latency (response time)
- Throughput (requests per second)
- Error rates
- Resource usage (CPU, memory)

**Consensus Strength: High** — Universal agreement on monitoring necessity.

### 12.3 Rollback Planning

> "Prepare a detailed rollback plan in case the deployment encounters critical issues that cannot be resolved in the production environment."
> — [Stratoflow SDLC Guide](https://stratoflow.com/software-deployment-phase/)

**Consensus Strength: High** — Rollback capability is essential.

---

## 13. Execute Stage Quality Gates

Based on the research, the following quality gates are recommended for the Execute stage:

### 13.1 Pre-Merge Gates

| Gate | Tool | Threshold |
|------|------|-----------|
| All tests pass | pytest | 100% |
| Type checks pass | mypy | No errors |
| Linting passes | ruff | No errors |
| Coverage threshold | pytest-cov | ≥80% (project-specific) |
| Security scan clean | bandit, safety | No high/critical issues |

### 13.2 Pre-Deploy Gates

| Gate | Verification |
|------|--------------|
| Version tagged | `git tag` exists |
| Changelog updated | CHANGELOG.md has entry |
| CI pipeline green | All checks passed |
| Rollback tested | Rollback procedure documented |

### 13.3 Post-Deploy Gates

| Gate | Verification |
|------|--------------|
| Health check passes | Application responds correctly |
| No error spike | Error rate within baseline |
| Performance acceptable | Latency within SLA |

**Consensus Strength: High** — These gates align with industry best practices.

---

## 14. Anti-Patterns to Avoid

### 14.1 Testing Anti-Patterns

| Anti-Pattern | Problem | Instead |
|--------------|---------|---------|
| Testing implementation | Brittle tests | Test behavior |
| Slow test suites | Slow feedback | Fast, isolated unit tests |
| Test interdependence | Flaky tests | Isolated tests with fixtures |
| Over-mocking | Tests pass but code fails | Test integration boundaries |

### 14.2 Deployment Anti-Patterns

| Anti-Pattern | Problem | Instead |
|--------------|---------|---------|
| Manual deployments | Human error, slow | Automate with CI/CD |
| Friday deploys | Weekend incidents | Deploy early in week |
| Big bang releases | High risk | Small, frequent releases |
| No rollback plan | Stuck with bugs | Always have rollback ready |

### 14.3 Code Anti-Patterns

| Anti-Pattern | Problem | Instead |
|--------------|---------|---------|
| Clever over clear | Unmaintainable | Boring, explicit code |
| Premature optimization | Wasted effort | Profile first |
| Cargo cult | Fragile patterns | Understand before applying |
| God classes | Hard to test/change | Single responsibility |

**Consensus Strength: High** — These anti-patterns are well-documented across sources.

---

## 15. References

### Books

| Title | Author(s) | Year | Relevance |
|-------|-----------|------|-----------|
| [Modern Software Engineering](https://www.amazon.com/Modern-Software-Engineering-Discipline-Development/dp/0137314914) | Dave Farley | 2021 | Core principles |
| [Continuous Delivery](https://www.continuous-delivery.co.uk/) | Farley & Humble | 2010 | CD practices |
| [Test-Driven Development by Example](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530) | Kent Beck | 2002 | TDD principles |
| [Refactoring](https://martinfowler.com/books/refactoring.html) | Martin Fowler | 2018 | Code smells, refactoring |
| [Clean Code](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882) | Robert C. Martin | 2008 | Code quality |
| [Architecture Patterns with Python](https://www.amazon.com/Architecture-Patterns-Python-Domain-Driven-Microservices/dp/1492052205) | Percival & Gregory | 2020 | DDD, Hexagonal in Python |
| [Hexagonal Architecture Explained](https://www.amazon.com/Hexagonal-Architecture-Explained-Alistair-Cockburn/dp/173751978X) | Cockburn & Garrido | 2023 | Ports & Adapters |

### Online Resources

| Resource | URL | Topic |
|----------|-----|-------|
| Dave Farley's Blog | [davefarley.net](https://www.davefarley.net/) | CD, Modern SE |
| pytest-bdd | [pypi.org/project/pytest-bdd](https://pypi.org/project/pytest-bdd/) | BDD |
| Real Python SOLID | [realpython.com/solid-principles-python](https://realpython.com/solid-principles-python/) | SOLID |
| Typer Testing | [typer.tiangolo.com/tutorial/testing](https://typer.tiangolo.com/tutorial/testing/) | CLI testing |
| PEP 8 | [peps.python.org/pep-0008](https://peps.python.org/pep-0008/) | Style guide |
| Clean Code Python | [github.com/zedr/clean-code-python](https://github.com/zedr/clean-code-python) | Clean code |
| refactoring.guru | [refactoring.guru/refactoring/smells](https://refactoring.guru/refactoring/smells) | Code smells |
| domain-driven-hexagon | [github.com/Sairyss/domain-driven-hexagon](https://github.com/Sairyss/domain-driven-hexagon) | DDD patterns |

### Tools

| Tool | Purpose | URL |
|------|---------|-----|
| pytest | Testing framework | [pytest.org](https://pytest.org/) |
| pytest-bdd | BDD testing | [pypi.org/project/pytest-bdd](https://pypi.org/project/pytest-bdd/) |
| Typer | CLI framework | [typer.tiangolo.com](https://typer.tiangolo.com/) |
| ruff | Linting/formatting | [astral.sh/ruff](https://astral.sh/ruff) |
| mypy | Type checking | [mypy-lang.org](https://mypy-lang.org/) |
| Bandit | Security (SAST) | [bandit.readthedocs.io](https://bandit.readthedocs.io/) |
| structlog | Structured logging | [structlog.org](https://www.structlog.org/) |

---

## 16. Summary: Execute Stage Principles

1. **Always be releasable** — Main branch deployable at all times (High consensus)
2. **Automate everything** — CI/CD for testing, security, deployment (High consensus)
3. **Test behavior, not implementation** — TDD with behavior focus (High consensus)
4. **Shift security left** — SAST/SCA in CI pipeline (High consensus)
5. **Structure for testability** — Hexagonal architecture, dependency injection (High consensus)
6. **Log for observability** — Structured logging, environment-specific config (High consensus)
7. **Deploy in small batches** — Frequent, low-risk releases (High consensus)
8. **Plan for failure** — Rollback procedures, monitoring, alerting (High consensus)
9. **Keep code clean** — Follow PEP 8, refactor continuously (High consensus)
10. **Measure meaningful coverage** — Quality over quantity in tests (Medium consensus)

---

*Research compiled: 2025-12-29*
*Sources: 35+ authoritative references with inline citations*
