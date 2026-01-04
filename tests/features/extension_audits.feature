Feature: Extension Audit Contributions

  As a Praxis user
  I want extensions to contribute audit checks via manifest
  So that domain-specific checks are extensible without core modifications

  Background:
    Given I am in a temporary directory
    And I have a workspace with PRAXIS_HOME set

  # Happy Path Scenarios

  Scenario: Extension contributes audit check
    Given an installed extension "mobile-pack" with praxis-extension.yaml
    And the manifest declares an audit check "mobile_manifest_present" for domain "code"
    And I have a project with domain "code" and subtype "mobile"
    When I run "praxis audit"
    Then the command succeeds
    And the output contains "mobile.json not found"

  Scenario: File exists check passes
    Given an installed extension "config-pack" with a "file_exists" audit check for "config.json"
    And I have a code project at stage "capture"
    And the project contains "config.json"
    When I run "praxis audit"
    Then the command succeeds
    And the check passes with the configured pass_message

  Scenario: File exists check fails
    Given an installed extension "config-pack" with a "file_exists" audit check for "config.json"
    And I have a code project at stage "capture"
    And the project does not contain "config.json"
    When I run "praxis audit"
    Then the check fails with the configured fail_message

  Scenario: Dir exists check works
    Given an installed extension "mobile-pack" with a "dir_exists" audit check for "src/mobile"
    And I have a code project at stage "capture"
    And the project contains directory "src/mobile"
    When I run "praxis audit"
    Then the check passes

  Scenario: File contains check with regex
    Given an installed extension "version-pack" with a "file_contains" audit check
    And the check looks for pattern "version.*=.*\"\\d+\\.\\d+\"" in "pyproject.toml"
    And I have a code project at stage "capture"
    And the project's pyproject.toml contains "version = \"1.0.0\""
    When I run "praxis audit"
    Then the check passes

  # Filtering Scenarios

  Scenario: Audit check respects subtype filtering
    Given an installed extension "mobile-pack" contributing audit checks for subtype "mobile"
    And I have a project with domain "code" and subtype "cli"
    When I run "praxis audit"
    Then the mobile-only audit checks are not executed

  Scenario: Audit check respects domain filtering
    Given an installed extension "create-pack" contributing audit checks for domain "create"
    And I have a code domain project
    When I run "praxis audit"
    Then the create-only audit checks are not executed

  Scenario: Audit check respects min_stage filtering
    Given an installed extension "formalize-pack" with an audit check with min_stage "formalize"
    And I have a code project at stage "explore"
    When I run "praxis audit"
    Then the check is not executed

  # Error Handling Scenarios

  Scenario: Malformed audit contribution is skipped
    Given an installed extension "broken-pack" with a malformed audit check definition
    When I run "praxis audit" in a code project
    Then the malformed check is skipped with a warning
    And other valid checks are executed normally

  Scenario: Unknown check_type is skipped
    Given an installed extension "custom-pack" with an audit check using check_type "custom_eval"
    When I run "praxis audit" in a code project
    Then the check is skipped with a warning about unsupported check_type
    And other checks continue to execute

  Scenario: Invalid regex pattern is handled gracefully
    Given an installed extension "regex-pack" with a "file_contains" check
    And the pattern contains invalid regex syntax "[unclosed"
    When I run "praxis audit" in a code project
    Then the check is skipped with a warning about invalid regex
    And other checks continue to execute

  # Multi-Extension Scenarios

  Scenario: Multiple extensions contribute checks in deterministic order
    Given an installed extension "aaa-pack" contributing check "check_a"
    And an installed extension "zzz-pack" contributing check "check_b"
    And I have a code project at stage "capture"
    When I run "praxis audit"
    Then both checks are executed
    And "check_a failed" appears before "check_b failed"
