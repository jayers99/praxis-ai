Feature: Praxis Status CLI
  As a developer using Praxis
  I want to see my project's current status
  So that I can understand where I am in the lifecycle

  Scenario: Show status of valid project
    Given a valid project at stage "capture"
    When I run praxis status
    Then the exit code should be 0
    And the output should contain "Domain:  code"
    And the output should contain "Stage:   capture (1/9)"
    And the output should contain "Next Stage: sense"

  Scenario: Show status with artifact present
    Given a valid project at stage "execute" with docs/sod.md
    When I run praxis status
    Then the exit code should be 0
    And the output should contain "docs/sod.md"

  Scenario: Show status with missing artifact
    Given a valid project at stage "execute"
    When I run praxis status
    Then the exit code should be 0
    And the output should contain "docs/sod.md"

  Scenario: Show status at final stage
    Given a valid project at stage "close"
    When I run praxis status
    Then the exit code should be 0
    And the output should contain "Next Stage: (none - at final stage)"

  Scenario: Show status with invalid config
    Given a project with invalid praxis.yaml
    When I run praxis status
    Then the exit code should be 1

  Scenario: Show status with validation errors
    Given a valid project at stage "execute"
    When I run praxis status
    Then the exit code should be 0
    And the output should contain "requires formalization artifact"
