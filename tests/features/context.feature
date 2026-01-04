Feature: Praxis Context Command
  As a developer using Praxis with AI assistants
  I want to generate deterministic context bundles
  So that AI sessions have consistent, reproducible context

  Scenario: Generate human-readable context bundle
    Given a valid Praxis project with praxis.yaml
    When I run praxis context
    Then the exit code should be 0
    And the output should contain "Project:"
    And the output should contain "Domain:"
    And the output should contain "Stage:"
    And the output should contain "Privacy:"
    And the output should contain "Opinions:"

  Scenario: Generate JSON context bundle
    Given a valid Praxis project with praxis.yaml
    When I run praxis context with --json
    Then the exit code should be 0
    And the output is valid JSON
    And the JSON contains field "schema_version"
    And the JSON contains field "domain"
    And the JSON contains field "stage"
    And the JSON contains field "privacy_level"
    And the JSON contains field "opinions"

  Scenario: Deterministic output
    Given a valid Praxis project with praxis.yaml
    When I run praxis context twice
    Then both outputs are identical

  Scenario: Include formalize artifact excerpt for commit stage
    Given a Praxis project at stage "commit" with domain "code"
    And a file "docs/sod.md" exists
    When I run praxis context with --json
    Then the exit code should be 0
    And the JSON field "formalize_artifact.path" equals "docs/sod.md"
    And the JSON field "formalize_artifact.excerpt" is not null

  Scenario: Handle missing formalize artifact at commit stage
    Given a Praxis project at stage "commit" with domain "code"
    And no file "docs/sod.md" exists
    When I run praxis context with --json
    Then the exit code should be 0
    And the JSON field "formalize_artifact.path" equals "docs/sod.md"
    And the JSON field "formalize_artifact.excerpt" is null

  Scenario: No formalize artifact required at capture stage
    Given a Praxis project at stage "capture" with domain "code"
    When I run praxis context with --json
    Then the exit code should be 0
    And the JSON field "formalize_artifact.path" is null

  Scenario: Handle missing praxis.yaml
    Given a directory without praxis.yaml
    When I run praxis context
    Then the exit code should be 1
    And the output should contain "praxis.yaml not found"

  Scenario: Handle invalid config values
    Given a praxis.yaml with invalid domain value
    When I run praxis context
    Then the exit code should be 1
    And the output should contain error message

  Scenario: Quiet mode suppresses output
    Given a valid Praxis project with praxis.yaml
    When I run praxis context with --quiet
    Then the exit code should be 0
    And the output is empty

  Scenario: Context includes resolved opinions
    Given a Praxis project with domain "code" and stage "formalize"
    And an opinions directory structure exists
    And opinion file "code/principles.md" exists
    When I run praxis context with --json
    Then the exit code should be 0
    And the JSON field "opinions" is an array
    And the opinions array is not empty

  Scenario: Context for Write domain shows brief artifact
    Given a Praxis project at stage "commit" with domain "write"
    And a file "docs/brief.md" exists
    When I run praxis context with --json
    Then the exit code should be 0
    And the JSON field "formalize_artifact.path" equals "docs/brief.md"

  Scenario: Context includes subtype if configured
    Given a Praxis project with domain "code" and subtype "cli"
    When I run praxis context with --json
    Then the exit code should be 0
    And the JSON field "subtype" equals "cli"
