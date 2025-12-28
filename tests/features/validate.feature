Feature: Praxis Validate CLI
  As a developer using Praxis
  I want to validate my praxis.yaml configuration
  So that I can ensure governance compliance before execution

  Scenario: Valid configuration passes
    Given a project with domain "code" and stage "execute"
    And a docs/sod.md file exists
    When I run praxis validate
    Then the exit code should be 0
    And the output should contain "passed"

  Scenario: Missing SOD at Execute stage fails
    Given a project with domain "code" and stage "execute"
    And no docs/sod.md file exists
    When I run praxis validate
    Then the exit code should be 1
    And the output should contain "ERROR"
    And the output should contain "docs/sod.md"

  Scenario: Valid configuration at early stage without artifact
    Given a project with domain "code" and stage "explore"
    And no docs/sod.md file exists
    When I run praxis validate
    Then the exit code should be 0
    And the output should contain "passed"

  Scenario: Invalid domain rejected
    Given a project with domain "invalid_domain" and stage "explore"
    When I run praxis validate
    Then the exit code should be 1
    And the output should contain "ERROR"

  Scenario: Invalid stage rejected
    Given a project with domain "code" and stage "invalid_stage"
    When I run praxis validate
    Then the exit code should be 1
    And the output should contain "ERROR"

  Scenario: Check-all flag runs all tool checks
    Given a valid project with passing tests
    When I run praxis validate --check-all
    Then the exit code should be 0
    And the output should contain "Tool Checks"
    And the output should contain "pytest"

  Scenario: Check-tests flag runs pytest
    Given a valid project with passing tests
    When I run praxis validate --check-tests
    Then the exit code should be 0
    And the output should contain "pytest"

  Scenario: Check-lint flag runs ruff
    Given a valid project with passing tests
    When I run praxis validate --check-lint
    Then the exit code should be 0
    And the output should contain "ruff"

  Scenario: Check-types flag runs mypy
    Given a valid project with passing tests
    When I run praxis validate --check-types
    Then the exit code should be 0
    And the output should contain "mypy"

  Scenario: Check-coverage without threshold configured fails
    Given a project with domain "code" and stage "execute"
    And a docs/sod.md file exists
    When I run praxis validate --check-coverage
    Then the exit code should be 1
    And the output should contain "coverage_threshold not set"

  Scenario: Check-coverage with threshold configured attempts coverage
    Given a valid project with coverage threshold 50
    When I run praxis validate --check-coverage
    Then the output should contain "coverage"

  Scenario: Check-all includes coverage when threshold configured
    Given a valid project with coverage threshold 50
    When I run praxis validate --check-all
    Then the output should contain "coverage"
