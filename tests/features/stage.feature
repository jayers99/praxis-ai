Feature: Praxis Stage CLI
  As a developer using Praxis
  I want to transition my project between lifecycle stages
  So that I can progress through the Praxis lifecycle

  Scenario: Advance to next stage
    Given a project at stage "capture"
    When I run praxis stage "sense"
    Then the exit code should be 0
    And praxis.yaml should have stage "sense"
    And the output should contain "Stage updated"

  Scenario: Skip stages forward
    Given a project at stage "capture"
    When I run praxis stage "formalize"
    Then the exit code should be 0
    And praxis.yaml should have stage "formalize"

  Scenario: Valid regression allowed
    Given a project at stage "execute" with docs/sod.md
    When I run praxis stage "formalize"
    Then the exit code should be 0
    And praxis.yaml should have stage "formalize"

  Scenario: Missing artifact warns but allows
    Given a project at stage "shape"
    When I run praxis stage "commit"
    Then the exit code should be 0
    And the output should contain "typically requires"
    And praxis.yaml should have stage "commit"

  Scenario: Invalid stage rejected
    Given a project at stage "capture"
    When I run praxis stage "invalid_stage"
    Then the exit code should be 1
    And the output should contain "Invalid stage"

  Scenario: Same stage is no-op with warning
    Given a project at stage "capture"
    When I run praxis stage "capture"
    Then the exit code should be 0
    And the output should contain "Already at stage"

  Scenario: CLAUDE.md stage is updated
    Given a project at stage "capture" with CLAUDE.md
    When I run praxis stage "sense"
    Then the exit code should be 0
    And CLAUDE.md should show stage "sense"
