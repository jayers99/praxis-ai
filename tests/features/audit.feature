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

  Scenario: Observe domain shows domain-specific checks
    Given a project with domain "observe" at stage "capture"
    When I run praxis audit
    Then the exit code should be 0
    And the output should contain "Organization"

  Scenario: Invalid config shows failed check
    Given a project with invalid praxis.yaml
    When I run praxis audit
    Then the exit code should be 1
    And the output should contain "Invalid or missing praxis.yaml"

  # Multi-domain audit scenarios (from issue requirements)

  Scenario: Create project shows Create-specific checks
    Given a create project at stage "formalize"
    When I run praxis audit
    Then the exit code should be 0
    And the output should contain "Brief"
    And the output should contain "Assets"

  Scenario: Learn project with subtype skill shows practice_log check
    Given a learn project with subtype "skill"
    When I run praxis audit
    Then the exit code should be 0
    And the output should contain "Practice log"

  Scenario: Write project at capture stage skips brief_present check
    Given a write project at stage "capture"
    When I run praxis audit
    Then the exit code should be 0
    And the output should not contain "Brief not found"

  Scenario: JSON output includes check metadata
    Given a create project at stage "capture"
    When I run praxis audit --json
    Then the output should contain "name"
    And the output should contain "category"
    And the output should contain "status"

  Scenario: Project with no subtype runs domain-level checks only
    Given an observe project without subtype
    When I run praxis audit
    Then the exit code should be 0
    And the output should contain "Captures"
    And the output should contain "Index"

  # CLI subtype-specific audit scenarios

  Scenario: CLI subtype project shows CLI-specific checks
    Given a code project with subtype "cli"
    When I run praxis audit
    Then the exit code should be 0
    And the output should contain "Cli:"
    And the output should contain "CLI entry point"
    And the output should contain "--help flag"
    And the output should contain "--version flag"

  Scenario: Code project without subtype does not show CLI checks
    Given a code project without subtype
    When I run praxis audit
    Then the exit code should be 0
    And the output should not contain "Cli:"
    And the output should not contain "CLI entry point"
