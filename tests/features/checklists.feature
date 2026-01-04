Feature: Lifecycle checklists as first-class artifacts
  As a Praxis user
  I want to see checklist references for my current stage
  So that I can understand what's required to complete the stage

  Scenario: All stages have checklist files
    Given the Praxis framework is installed
    When I list files in "core/checklists/"
    Then I see 9 checklist files, one per lifecycle stage
    And each file follows the consistent checklist structure

  Scenario: Status shows checklist reference for current stage
    Given a project at stage "formalize"
    When I run "praxis status"
    Then the output includes a reference to "core/checklists/formalize.md"

  Scenario: Status shows domain-specific checklist when available
    Given a project at stage "formalize" with domain "code"
    When I run "praxis status"
    Then the output includes a reference to "core/checklists/formalize.md"
    And the output includes a reference to "core/checklists/formalize-code.md"

  Scenario: Validate references checklist on gate failure
    Given a project at stage "commit"
    And the SOD artifact is missing
    When I run "praxis validate"
    Then the validation fails with an error
    And the output includes "See checklist: core/checklists/formalize.md"

  Scenario: Graceful handling when domain addendum missing
    Given a project at stage "capture" with domain "code"
    And no domain addendum exists for "capture-code"
    When I run "praxis status"
    Then the output includes a reference to "core/checklists/capture.md"
    And the output does not reference a missing addendum file

  Scenario: Checklist content aligns with lifecycle spec
    Given the checklist file "core/checklists/formalize.md"
    When I compare its entry/exit criteria
    Then they match the criteria defined in "core/spec/lifecycle.md"
