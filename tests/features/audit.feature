Feature: Praxis Audit CLI
  As a developer using Praxis
  I want to audit my project against domain best practices
  So that I can ensure my project follows aspirational goals

  Scenario: Audit valid Python CLI project
    Given a Python CLI project with all checks passing
    When I run praxis audit
    Then the exit code should be 0
    And the output should contain "passed"

  Scenario: Audit project missing Poetry
    Given a code project without pyproject.toml
    When I run praxis audit
    Then the exit code should be 0
    And the output should contain "Poetry not configured"

  Scenario: Strict mode fails on warnings
    Given a code project without pyproject.toml
    When I run praxis audit --strict
    Then the exit code should be 1

  Scenario: JSON output format
    Given a Python CLI project with all checks passing
    When I run praxis audit --json
    Then the output should contain "checks"
    And the output should contain "project_name"

  Scenario: Non-code domain shows no checks
    Given a project with domain "observe"
    When I run praxis audit
    Then the exit code should be 0
    And the output should contain "0 passed"

  Scenario: Invalid config shows failed check
    Given a project with invalid praxis.yaml
    When I run praxis audit
    Then the exit code should be 1
    And the output should contain "Invalid or missing praxis.yaml"
