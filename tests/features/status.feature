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

  # Next Steps Feature Tests

  Scenario: Status shows create step when artifact missing
    Given a Praxis project with domain "code" and stage "formalize"
    And docs/sod.md does not exist
    When I run praxis status
    Then the output includes a "create" action for "docs/sod.md"
    And 1-3 next steps are shown

  Scenario: Status shows edit step when artifact exists
    Given a Praxis project with domain "code" and stage "formalize"
    And docs/sod.md exists
    When I run praxis status
    Then the output includes an "edit" action for "docs/sod.md"
    And 1-3 next steps are shown

  Scenario: Status shows fix step when validation errors exist
    Given a Praxis project with an invalid domain value in praxis.yaml
    When I run praxis status
    Then the first next step is a "fix" action
    And the step includes the target "praxis.yaml"

  Scenario: Status shows next steps in JSON output
    Given a valid project at stage "capture"
    When I run praxis status with --json
    Then the exit code should be 0
    And the JSON output contains "next_steps" array
    And the next_steps array has 1 to 3 items

  Scenario: Status for Write domain shows brief artifact
    Given a Praxis project with domain "write" and stage "formalize"
    And docs/brief.md does not exist
    When I run praxis status
    Then the output includes a "create" action for "docs/brief.md"
    And 1-3 next steps are shown

  Scenario: Status at capture stage shows run step
    Given a valid project at stage "capture"
    When I run praxis status
    Then the output includes a "run" action
    And the run step includes "praxis stage sense"
