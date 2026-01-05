Feature: AI Guards Composition and Rendering

  As a Praxis user
  I want to compose AI guards from multiple sources
  So that I can generate vendor-specific instruction files

  Background:
    Given I have initialized a Praxis workspace

  Scenario: Render guards with no user or project guards
    Given I have a code project with no AI guards configured
    When I run "praxis guards render"
    Then the command should succeed
    And a CLAUDE.md file should be created
    And the file should contain "No Guards Configured"

  Scenario: Render guards with project-level guards only
    Given I have a code project
    And the project has a "praxis/ai-guards/code.md" file with content:
      """
      # Code Domain Guards
      Use TypeScript for all new code
      """
    When I run "praxis guards render --vendor claude"
    Then the command should succeed
    And the CLAUDE.md file should contain "Use TypeScript for all new code"
    And the CLAUDE.md file should contain "Project Guards: code"

  Scenario: Render guards for multiple vendors
    Given I have a code project
    And the project has a "praxis/ai-guards/code.md" file with guards
    When I run "praxis guards render --vendor all"
    Then the command should succeed
    And a CLAUDE.md file should be created
    And a .github/copilot-instructions.md file should be created
    And a GEMINI.md file should be created

  Scenario: List active guards shows composition
    Given I have a code project
    And the project has a "praxis/ai-guards/code.md" file with guards
    When I run "praxis guards list"
    Then the command should succeed
    And the output should contain "Active environment:"
    And the output should contain "project_domain"

  Scenario: Validate guards composition
    Given I have a code project
    And the project has a "praxis/ai-guards/code.md" file with guards
    When I run "praxis guards validate"
    Then the command should succeed
    And the output should contain "Guard composition is valid"

  Scenario: Render guards with dry-run flag
    Given I have a code project
    And the project has a "praxis/ai-guards/code.md" file with guards
    When I run "praxis guards render --dry-run"
    Then the command should succeed
    And no guard files should be created
    And the output should contain "Would write"

  Scenario: Render guards for specific vendor
    Given I have a code project
    When I run "praxis guards render --vendor copilot"
    Then the command should succeed
    And a .github/copilot-instructions.md file should be created
    And no CLAUDE.md file should be created
    And no GEMINI.md file should be created
