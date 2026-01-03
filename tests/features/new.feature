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
    And praxis.yaml should exist with subtype "cli"
    And CLAUDE.md should exist
    And docs/capture.md should exist

  Scenario: Create new project twice without and with --force
    Given an empty directory
    When I run praxis new "my-project" with domain "code" and privacy "personal"
    Then the exit code should be 0
    When I run praxis new "my-project" again without --force
    Then the exit code should be 1
    And the output should contain "--force"
    When I run praxis new "my-project" again with --force
    Then the exit code should be 0

  Scenario: Invalid subtype format fails fast
    Given an empty directory
    When I run praxis new "my-project" with invalid subtype format
    Then the exit code should be 1
    And the output should contain "Invalid subtype"

  Scenario: Invalid subtype for domain fails fast
    Given an empty directory
    When I run praxis new "my-project" with subtype "visual" and domain "code"
    Then the exit code should be 1
    And the output should contain "Invalid subtype 'visual' for domain 'code'"
    And the output should contain "Valid subtypes: cli, library, api, webapp, infrastructure, script"

  Scenario: New --json succeeds with PRAXIS_HOME defaults
    Given PRAXIS_HOME is set with a workspace config
    When I run praxis new "my-project" with domain "code" and privacy "personal" --json
    Then the exit code should be 0
    And praxis.yaml should exist with domain "code"

  Scenario: New --json fails without PRAXIS_HOME or --path
    Given PRAXIS_HOME is not set
    When I run praxis new "my-project" with domain "code" and privacy "personal" --json
    Then the exit code should be 3
    And the output should contain "PRAXIS_HOME not set"
