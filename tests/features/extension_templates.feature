Feature: Extension Template Contributions

  As a Praxis user
  I want extensions to contribute template files
  So that domain-specific template scaffolds are extensible without core modifications

  Background:
    Given I am in a temporary directory
    And I have a workspace with PRAXIS_HOME set

  Scenario: Extension contributes stage template
    Given an installed extension "mobile-pack" with praxis-extension.yaml
    And the manifest declares a template contribution:
      | source                                       | target                               | subtypes   |
      | templates/domain/code/subtype/mobile/artifact/sod.md | domain/code/subtype/mobile/artifact/sod.md | ["mobile"] |
    And the extension has the template file at "templates/domain/code/subtype/mobile/artifact/sod.md"
    And I have a project with domain "code" and subtype "mobile"
    When I run "praxis templates render --stage formalize"
    Then the command succeeds
    And the output contains "extension:mobile-pack" or shows the contributed template was used

  Scenario: Template subtype filtering
    Given an installed extension "mobile-pack" with praxis-extension.yaml
    And the manifest declares a template contribution for subtype "mobile"
    And the extension has the template file for mobile subtype
    And I have a project with domain "code" and subtype "cli"
    When I run "praxis templates render --stage formalize"
    Then the mobile-only template is not used

  Scenario: Core templates take precedence over extension templates
    Given an installed extension "override-pack" with praxis-extension.yaml
    And the manifest declares a template contribution that overlaps with core
    And the extension has a template file at the same path as core
    And I have a project with domain "code" and subtype "cli"
    When I run "praxis templates render --stage formalize"
    Then the core template is used

  Scenario: Extension template without subtype filter applies to all subtypes
    Given an installed extension "universal-pack" with praxis-extension.yaml
    And the manifest declares a template contribution with empty subtypes list
    And the extension has the template file
    And I have a project with domain "code" and subtype "cli"
    When I run "praxis templates render --stage formalize"
    Then the contributed template is available for rendering

  Scenario: Manifest with missing template source file
    Given an installed extension "broken-pack" with praxis-extension.yaml
    And the manifest declares a template with source "templates/missing.md"
    And the template source file does not exist
    When I run "praxis templates render --stage formalize" in a code project
    Then a warning is logged for the missing template source
    And the invalid contribution is skipped
