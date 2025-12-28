Feature: CLI Automation Flags
  As a developer using Praxis in CI/CD
  I want machine-readable output and quiet mode
  So that I can automate praxis commands

  # --json flag tests

  Scenario: Init with --json outputs structured JSON
    Given an empty project directory
    When I run praxis init --domain code --privacy personal --json
    Then the exit code should be 0
    And the output should be valid JSON
    And the JSON should have key "success"
    And the JSON should have key "files_created"

  Scenario: Init --json requires --domain and --privacy
    Given an empty project directory
    When I run praxis init --json
    Then the exit code should be 1
    And the output should contain "errors"

  Scenario: Validate with --json outputs structured JSON
    Given a valid praxis project at capture stage
    When I run praxis validate --json
    Then the exit code should be 0
    And the output should be valid JSON
    And the JSON should have key "valid"
    And the JSON should have key "config"

  Scenario: Stage with --json outputs structured JSON
    Given a valid praxis project at capture stage
    When I run praxis stage sense --json
    Then the exit code should be 0
    And the output should be valid JSON
    And the JSON should have key "success"

  Scenario: Status with --json outputs structured JSON
    Given a valid praxis project at capture stage
    When I run praxis status --json
    Then the exit code should be 0
    And the output should be valid JSON
    And the JSON should have key "project_name"
    And the JSON should have key "config"

  # --quiet flag tests

  Scenario: Init with --quiet suppresses output on success
    Given an empty project directory
    When I run praxis init --domain code --privacy personal --quiet
    Then the exit code should be 0
    And the output should be empty

  Scenario: Validate with --quiet suppresses output on success
    Given a valid praxis project at capture stage
    When I run praxis validate --quiet
    Then the exit code should be 0
    And the output should be empty

  Scenario: Stage with --quiet suppresses success message
    Given a valid praxis project at capture stage
    When I run praxis stage sense --quiet
    Then the exit code should be 0
    And the output should be empty

  Scenario: Status with --quiet suppresses output
    Given a valid praxis project at capture stage
    When I run praxis status --quiet
    Then the exit code should be 0
    And the output should be empty

  Scenario: Audit with --quiet suppresses output
    Given a valid praxis project at capture stage
    When I run praxis audit --quiet
    Then the exit code should be 0
    And the output should be empty
