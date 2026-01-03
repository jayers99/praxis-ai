Feature: Praxis Templates Render CLI
  As a developer using Praxis
  I want to render formalize artifacts for my domain
  So that I can transition from discovery to execution with clear structure

  Scenario: Generate formalize artifact for Code domain
    Given a project with domain "code" at stage "shape"
    When I run praxis templates render --stage formalize
    Then the exit code should be 0
    And "docs/sod.md" should be created
    And "docs/formalize.md" should be created
    And the output should contain "Created docs/sod.md"

  Scenario: Generate formalize artifact for Create domain
    Given a project with domain "create" at stage "shape"
    When I run praxis templates render --stage formalize
    Then the exit code should be 0
    And "docs/brief.md" should be created
    And "docs/formalize.md" should be created
    And the output should contain "Created docs/brief.md"

  Scenario: Generate formalize artifact for Write domain
    Given a project with domain "write" at stage "shape"
    When I run praxis templates render --stage formalize
    Then the exit code should be 0
    And "docs/brief.md" should be created
    And "docs/formalize.md" should be created
    And the output should contain "Created docs/brief.md"

  Scenario: Generate formalize artifact for Learn domain
    Given a project with domain "learn" at stage "shape"
    When I run praxis templates render --stage formalize
    Then the exit code should be 0
    And "docs/plan.md" should be created
    And "docs/formalize.md" should be created
    And the output should contain "Created docs/plan.md"

  Scenario: Skip generation when artifact exists
    Given a project with domain "create" at stage "shape"
    And "docs/brief.md" already exists
    When I run praxis templates render --stage formalize
    Then the exit code should be 0
    And the existing file should not be modified
    And the output should contain "Skipping docs/brief.md — file already exists"

  Scenario: Observe domain has no formalize artifact
    Given a project with domain "observe" at stage "shape"
    When I run praxis templates render --stage formalize
    Then the exit code should be 0
    And the output should contain "Observe domain has no formalize artifact"
    And the output should contain "Observe is for raw capture and does not cross into execution"

  Scenario: Validation detects missing formalize artifact at Commit
    Given a project with domain "code" at stage "commit"
    And "docs/sod.md" does not exist
    When I run praxis validate
    Then the exit code should be 1
    And the output should contain "ERROR"
    And the output should contain "docs/sod.md"

  Scenario: Status shows formalize artifact path
    Given a project with domain "code" at stage "execute"
    And "docs/sod.md" does not exist
    When I run praxis status
    Then the exit code should be 0
    And the output should contain "docs/sod.md"
