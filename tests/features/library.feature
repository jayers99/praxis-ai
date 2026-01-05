Feature: Library CLI commands
  As a researcher using Praxis
  I want to query and maintain the research library via CLI
  So that I can discover and manage research artifacts

  # Happy paths

  Scenario: Query the library with a question
    Given the research library exists with cataloged artifacts
    When I run praxis library query "What are the praxis roles?"
    Then the exit code should be 0
    And the output should contain "Coverage:"
    And the output should contain "Sources:"

  Scenario: Search the library by keyword
    Given the research library exists with cataloged artifacts
    When I run praxis library search with keyword "roles"
    Then the exit code should be 0
    And the output should contain "match"

  Scenario: Get citation for an artifact
    Given the research library exists with cataloged artifacts
    When I run praxis library cite "roles-rationale-2025-12-28"
    Then the exit code should be 0
    And the output should contain "Rationale for Praxis Roles"
    And the output should contain "Consensus:"

  Scenario: Check for orphaned artifacts
    Given the research library exists with cataloged artifacts
    When I run praxis library check-orphans
    Then the exit code should be 0

  Scenario: Check for stale artifacts
    Given the research library exists with cataloged artifacts
    When I run praxis library check-stale with days 400
    Then the exit code should be 0
    And the output should contain "stale"

  Scenario: Reindex the library
    Given the research library exists with cataloged artifacts
    When I run praxis library reindex
    Then the exit code should be 0
    And the output should contain "not yet implemented"

  # Edge cases

  Scenario: Search with obscure keyword returns low relevance results
    Given the research library exists with cataloged artifacts
    When I run praxis library search with keyword "zzznonexistent999"
    Then the exit code should be 0

  # Error paths

  Scenario: Cite non-existent artifact
    Given the research library exists with cataloged artifacts
    When I run praxis library cite "invalid-artifact-id"
    Then the exit code should be 1
    And the output should contain "Artifact not found"

  Scenario: Query with empty string
    Given the research library exists with cataloged artifacts
    When I run praxis library query with empty string
    Then the exit code should be 1
    And the output should contain "cannot be empty"

  Scenario: JSON output for query
    Given the research library exists with cataloged artifacts
    When I run praxis library query "roles" with json flag
    Then the exit code should be 0
    And the JSON output should contain "coverage_level"
    And the JSON output should contain "sources"
