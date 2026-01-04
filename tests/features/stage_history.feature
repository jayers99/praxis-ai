Feature: Stage history tracking
  As a developer using Praxis
  I want to track stage transitions over time
  So that I can see the complete evolution of my project

  Scenario: Stage transition records history entry
    Given a project at stage "explore"
    When I run praxis stage "formalize"
    Then the exit code should be 0
    And praxis.yaml should contain a history entry with from_stage "explore"
    And praxis.yaml should contain a history entry with to_stage "formalize"
    And praxis.yaml should contain a history entry with timestamp

  Scenario: Formalize transition generates contract ID
    Given a project at stage "shape"
    When I run praxis stage "formalize"
    Then the exit code should be 0
    And praxis.yaml should contain a contract_id matching "contract-\d{8}-\d{6}"

  Scenario: Non-standard regression requires rationale in automation mode
    Given a project at stage "execute" with docs/sod.md
    When I run praxis stage "explore" with --json flag
    Then the exit code should be 1
    And the output should contain "not standard"

  Scenario: Regression with inline rationale succeeds
    Given a project at stage "execute" with docs/sod.md
    When I run praxis stage "explore" with reason "Scope change discovered"
    Then the exit code should be 0
    And praxis.yaml should contain a history entry with reason "Scope change discovered"

  Scenario: Status displays history
    Given a project at stage "explore"
    And the project has transitioned through "capture" to "sense" to "explore"
    When I run praxis status
    Then the exit code should be 0
    And the output should contain "Stage History:"
    And the output should contain "capture → sense"
    And the output should contain "sense → explore"

  Scenario: Existing project without history initializes gracefully
    Given a project at stage "capture" without history field
    When I run praxis stage "sense"
    Then the exit code should be 0
    And praxis.yaml should contain a history section
    And praxis.yaml should contain a history entry with from_stage "capture"

  Scenario: Multiple transitions build history
    Given a project at stage "capture"
    When I run praxis stage "sense"
    And I run praxis stage "explore"
    Then praxis.yaml should have 2 history entries
    And praxis.yaml should contain a history entry with from_stage "capture"
    And praxis.yaml should contain a history entry with from_stage "sense"

  Scenario: Allowed regression does not require reason
    Given a project at stage "execute" with docs/sod.md
    When I run praxis stage "formalize"
    Then the exit code should be 0
    And praxis.yaml should contain a history entry without reason

  Scenario: Non-standard regression shows Formalize crossing warning
    Given a project at stage "execute" with contract "contract-20260101-120000"
    When I run praxis stage "explore"
    Then the exit code should be 1
    And the output should contain "crosses the Formalize boundary"
    And the output should contain "contract-20260101-120000"

  Scenario: Non-standard regression with reason and Formalize crossing succeeds
    Given a project at stage "execute" with contract "contract-20260101-120000"
    When I run praxis stage "explore" with reason "Major scope change discovered"
    Then the exit code should be 0
    And praxis.yaml should contain a history entry with reason "Major scope change discovered"

  Scenario: Commit to Shape crosses Formalize boundary
    Given a project at stage "commit" with contract "contract-20260101-120000"
    When I run praxis stage "shape"
    Then the exit code should be 1
    And the output should contain "crosses the Formalize boundary"
    And the output should contain "contract-20260101-120000"

  Scenario: Sustain to Execute does NOT cross Formalize
    Given a project at stage "sustain" with docs/sod.md
    When I run praxis stage "execute"
    Then the exit code should be 0
    And the output should not contain "crosses the Formalize boundary"

  Scenario: Regression in automation mode includes crossing_formalize in JSON
    Given a project at stage "execute" with contract "contract-20260101-120000"
    When I run praxis stage "explore" with --json flag
    Then the exit code should be 1
    And the JSON output should contain "crossing_formalize": true
    And the JSON output should contain "voided_contract_id": "contract-20260101-120000"
