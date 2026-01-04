Feature: Privacy guardrails for AI prompt exports

  As a Praxis user
  I want privacy guardrails on AI prompt exports
  So that I can safely collaborate with AI according to my declared privacy level

  Background:
    Given I am in a temporary directory
    And I have an opinions directory structure

  Scenario: Public project exports without constraints
    Given a praxis.yaml with domain "code" stage "capture" and privacy "public"
    And opinions/_shared/first-principles.md exists with valid frontmatter
    When I run "praxis opinions --prompt"
    Then the output does not contain "Privacy Constraints"
    And the stderr does not contain "Privacy Level"
    And the exit code is 0

  Scenario: Personal project exports with warning
    Given a praxis.yaml with domain "code" stage "capture" and privacy "personal"
    And opinions/_shared/first-principles.md exists with valid frontmatter
    When I run "praxis opinions --prompt"
    Then the stderr contains "Privacy Level: PERSONAL"
    And the output contains "No credentials, secrets, or regulated identifiers"
    And the exit code is 0

  Scenario: Confidential project exports with strong warning
    Given a praxis.yaml with domain "code" stage "capture" and privacy "confidential"
    And opinions/_shared/first-principles.md exists with valid frontmatter
    When I run "praxis opinions --prompt"
    Then the stderr contains "Privacy Level: CONFIDENTIAL"
    And the output contains "Redacted or abstracted inputs only"
    And the output contains "no raw logs, configs, or identifiers"
    And the exit code is 0

  Scenario: Restricted project exports with maximum constraints
    Given a praxis.yaml with domain "code" stage "capture" and privacy "restricted"
    And opinions/_shared/first-principles.md exists with valid frontmatter
    When I run "praxis opinions --prompt"
    Then the stderr contains "Privacy Level: RESTRICTED"
    And the output contains "No external AI with raw content"
    And the output contains "abstract summaries only, never source material"
    And the exit code is 0

  Scenario: Redact flag sanitizes obvious patterns
    Given a praxis.yaml with domain "code" stage "capture" and privacy "personal"
    And opinions/_shared/first-principles.md exists with content containing "API_KEY=sk-abc123"
    When I run "praxis opinions --prompt --redact"
    Then the output contains "[REDACTED:API_KEY]"
    And the output does not contain "sk-abc123"
    And the stderr contains "Redaction applied"
    And the exit code is 0

  Scenario: Deterministic output for same inputs
    Given a praxis.yaml with domain "code" stage "capture" and privacy "confidential"
    And opinions/_shared/first-principles.md exists with valid frontmatter
    When I run "praxis opinions --prompt"
    And I save the output as "first_run"
    And I run "praxis opinions --prompt"
    And I save the output as "second_run"
    Then "first_run" equals "second_run"

  Scenario: Restricted project with redact flag combines both mechanisms
    Given a praxis.yaml with domain "code" stage "capture" and privacy "restricted"
    And opinions/_shared/first-principles.md exists with content containing "AWS_SECRET=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    When I run "praxis opinions --prompt --redact"
    Then the stderr contains "Privacy Level: RESTRICTED"
    And the output contains "No external AI with raw content"
    And the output contains "[REDACTED:AWS_SECRET]"
    And the output does not contain "wJalrXUtnFEMI"
    And the stderr contains "Redaction applied"
    And the exit code is 0

  Scenario: Multiple redaction patterns detected
    Given a praxis.yaml with domain "code" stage "capture" and privacy "personal"
    And opinions/_shared/first-principles.md exists with content containing "password=hunter2 and JWT=eyJhbGci.test.token"
    When I run "praxis opinions --prompt --redact"
    Then the output contains "[REDACTED:PASSWORD]"
    And the output contains "[REDACTED:JWT]"
    And the stderr contains "Redaction applied"
    And the exit code is 0
