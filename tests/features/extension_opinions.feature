Feature: Extension Opinion Contributions

  As a Praxis user
  I want extensions to contribute opinion files
  So that domain-specific guidance is extensible without core modifications

  Background:
    Given I am in a temporary directory
    And I have a workspace with PRAXIS_HOME set

  Scenario: Extension contributes opinion file
    Given an installed extension "mobile-pack" with praxis-extension.yaml
    And the manifest declares an opinion contribution "code/subtypes/mobile.md"
    And the extension has the opinion file at "opinions/code/subtypes/mobile.md"
    When I run "praxis opinions --list"
    Then the output contains "subtypes/mobile.md"
    And the output contains "[mobile-pack]"

  Scenario: Invalid manifest fails with helpful error
    Given an installed extension "bad-pack" with praxis-extension.yaml
    And the manifest has an unsupported manifest_version "99.0"
    When I run "praxis opinions --list"
    Then the exit code is 0
    And the stderr does not contain "bad-pack"

  Scenario: Malformed YAML in manifest fails gracefully
    Given an installed extension "broken-pack" with praxis-extension.yaml
    And the manifest contains invalid YAML syntax
    When I run "praxis opinions --list"
    Then the exit code is 0
    And other extensions with valid manifests are loaded

  Scenario: Conflict resolution is deterministic (alphabetical order)
    Given an installed extension "aaa-pack" contributing "code/principles.md"
    And an installed extension "zzz-pack" contributing "code/principles.md"
    And both extensions have the opinion file
    When I run "praxis opinions --list"
    Then the output contains "principles.md [zzz-pack]"

  Scenario: Core contributions take precedence over extensions
    Given the core opinions include "code/principles.md"
    And an installed extension "my-pack" contributing "code/principles.md"
    And the extension has the opinion file at "opinions/code/principles.md"
    When I run "praxis opinions --list"
    Then the output contains "principles.md"
    And the output does not contain "[my-pack]"

  Scenario: Extension without manifest is silently skipped
    Given an installed extension "legacy-pack" without praxis-extension.yaml
    And an installed extension "valid-pack" with praxis-extension.yaml
    When I run "praxis opinions --list"
    Then the exit code is 0
    And the output does not contain "legacy-pack"
    And the output contains "opinions/"
