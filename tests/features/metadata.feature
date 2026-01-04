Feature: Deterministic project naming and metadata
  As a Praxis user
  I want consistent project metadata fields
  So that I can identify and categorize projects reliably

  Scenario: New project gets metadata automatically
    Given an empty directory
    When I run praxis new "my-project" with domain "code" and privacy "personal"
    Then the exit code should be 0
    And praxis.yaml should contain name "My Project"
    And praxis.yaml should contain slug "my-project"
    And praxis.yaml should have empty description
    And praxis.yaml should contain empty tags

  Scenario: Status displays project metadata
    Given a project with name "My CLI Tool" and slug "my-cli-tool"
    When I run praxis status
    Then the exit code should be 0
    And the output should contain "Project: My CLI Tool"
    And the output should contain "Slug:    my-cli-tool"

  Scenario: Legacy project gets auto-generated metadata
    Given a project directory "old-project" with no metadata fields
    When I run praxis validate
    Then the exit code should be 0
    And slug should be auto-generated as "old-project"
    And name should be auto-generated as "Old Project"

  Scenario: Slug format is validated
    Given a praxis.yaml with slug "Invalid Slug!"
    When I run praxis validate
    Then the exit code should be 1
    And the output should contain "slug"
    And the output should contain "pattern"

  Scenario: Project with description and tags displays in status
    Given a project with description "A test CLI tool" and tags "test,demo"
    When I run praxis status
    Then the exit code should be 0
    And the output should contain "Desc:    A test CLI tool"
    And the output should contain "Tags:    test, demo"

  Scenario: Init command generates metadata from directory name
    Given a directory named "api-backend"
    When I run praxis init with domain "code" and privacy "personal"
    Then the exit code should be 0
    And praxis.yaml should contain name "Api Backend"
    And praxis.yaml should contain slug "api-backend"

  Scenario: Complex directory name is properly slugified
    Given a directory named "My_Special@Project#123"
    When I run praxis init with domain "code" and privacy "personal"
    Then the exit code should be 0
    And praxis.yaml should contain slug "my-special-project-123"
