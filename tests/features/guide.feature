Feature: Praxis Guide CLI
  As a Praxis user
  I want to access key framework concepts from the CLI
  So that I can stay in flow without context-switching to documentation

  # Lifecycle guide scenarios

  Scenario: Display lifecycle guide with stages and hinge concept
    Given the user is in any directory
    When the user runs "praxis guide lifecycle"
    Then the exit code should be 0
    And the output contains all 9 lifecycle stages
    And the output explains the Formalize hinge concept
    And the output contains a reference to "core/spec/lifecycle.md"

  Scenario: Lifecycle guide fits terminal screen
    Given the user is in any directory
    When the user runs "praxis guide lifecycle"
    Then the exit code should be 0
    And the output is less than 50 lines

  # Privacy guide scenarios

  Scenario: Display privacy guide with levels and constraints
    Given the user is in any directory
    When the user runs "praxis guide privacy"
    Then the exit code should be 0
    And the output lists all 5 privacy levels
    And the output explains behavioral constraints for each level
    And the output contains a reference to "core/spec/privacy.md"

  # Domain guide scenarios

  Scenario: Display domain-specific guidance for code domain
    Given the user is in any directory
    When the user runs "praxis guide domain code"
    Then the exit code should be 0
    And the output describes the code domain purpose
    And the output mentions the required formalize artifact "docs/sod.md"
    And the output contains a reference to "core/spec/domains.md"

  Scenario: Display error for unknown domain
    Given the user is in any directory
    When the user runs "praxis guide domain unknown"
    Then the exit code should be 1
    And the output contains "Unknown domain: unknown"
    And the output lists valid domain options

  # Error handling scenarios

  Scenario: Display help for guide command
    Given the user is in any directory
    When the user runs "praxis guide --help"
    Then the exit code should be 0
    And the output lists available guide topics
