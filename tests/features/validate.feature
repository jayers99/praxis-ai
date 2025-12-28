Feature: Praxis Validate CLI
  As a developer using Praxis
  I want to validate my praxis.yaml configuration
  So that I can ensure governance compliance before execution

  Scenario: Valid configuration passes
    Given a project with domain "code" and stage "execute"
    And a docs/sod.md file exists
    When I run praxis validate
    Then the exit code should be 0
    And the output should contain "valid"

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
    And the output should contain "valid"

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
