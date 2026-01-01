Feature: Praxis New CLI
  As a user starting a new project
  I want a guided entrypoint to create a project directory and initialize governance
  So that I can start with correct defaults and safe scaffolding

  Scenario: Create new project with flags
    Given an empty directory
    When I run praxis new "my-project" with domain "code" and privacy "personal"
    Then the exit code should be 0
    And the output should contain "project created"
    And praxis.yaml should exist with domain "code"
    And CLAUDE.md should exist
    And docs/capture.md should exist

  Scenario: New --json fails without PRAXIS_HOME or --path
    Given PRAXIS_HOME is not set
    When I run praxis new "my-project" with domain "code" and privacy "personal" --json
    Then the exit code should be 3
    And the output should contain "PRAXIS_HOME not set"
