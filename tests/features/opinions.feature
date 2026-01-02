Feature: Opinions Resolution

  As a Praxis user
  I want to resolve applicable opinions for my project
  So that I can get deterministic governance guidance

  Background:
    Given I am in a temporary directory
    And I have an opinions directory structure

  Scenario: Resolve opinions for code domain project
    Given a praxis.yaml with domain "code" and stage "capture"
    And opinions/_shared/first-principles.md exists with valid frontmatter
    And opinions/code/principles.md exists with valid frontmatter
    And opinions/code/capture.md exists with valid frontmatter
    When I run "praxis opinions"
    Then the output contains "first-principles.md"
    And the output contains "code/principles.md"
    And the output contains "code/capture.md"
    And the exit code is 0

  Scenario: Deterministic resolution produces identical output
    Given a praxis.yaml with domain "code" and stage "execute"
    And opinions/_shared/first-principles.md exists with valid frontmatter
    And opinions/code/principles.md exists with valid frontmatter
    When I run "praxis opinions --json"
    And I save the output as "first_run"
    And I run "praxis opinions --json"
    And I save the output as "second_run"
    Then "first_run" equals "second_run"

  Scenario: Subtype inheritance chain
    Given a praxis.yaml with domain "code" and stage "capture" and subtype "cli"
    And opinions/_shared/first-principles.md exists with valid frontmatter
    And opinions/code/principles.md exists with valid frontmatter
    And opinions/code/subtypes/cli/principles.md exists with valid frontmatter
    When I run "praxis opinions"
    Then the output contains "code/subtypes/cli/principles.md"
    And the exit code is 0

  Scenario: Missing opinions directory shows warning
    Given a praxis.yaml with domain "code" and stage "capture"
    But the opinions directory does not exist
    When I run "praxis opinions"
    Then the stderr contains "No opinions directory found"
    And the exit code is 0

  Scenario: Query without praxis.yaml using flags
    Given no praxis.yaml exists
    And opinions/_shared/first-principles.md exists with valid frontmatter
    And opinions/code/principles.md exists with valid frontmatter
    When I run "praxis opinions --domain code --stage capture"
    Then the output contains "code/principles.md"
    And the exit code is 0

  Scenario: JSON output has stable schema
    Given a praxis.yaml with domain "code" and stage "execute"
    And opinions/_shared/first-principles.md exists with valid frontmatter
    When I run "praxis opinions --json"
    Then the output is valid JSON
    And the JSON contains key "domain"
    And the JSON contains key "stage"
    And the JSON contains key "files"

  Scenario: List all available opinions
    Given opinions/_shared/first-principles.md exists with valid frontmatter
    And opinions/code/principles.md exists with valid frontmatter
    And opinions/create/principles.md exists with valid frontmatter
    When I run "praxis opinions --list"
    Then the output contains "opinions/"
    And the output contains "_shared/"
    And the output contains "code/"
    And the output contains "Total:"
    And the exit code is 0

  Scenario: Error when no domain specified and no praxis.yaml
    Given no praxis.yaml exists
    And opinions/code/principles.md exists with valid frontmatter
    When I run "praxis opinions"
    Then the stderr contains "No praxis.yaml found"
    And the exit code is 1
