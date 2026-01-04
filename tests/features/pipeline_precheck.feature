Feature: Research Library Precheck and Rerun Support

  As a Praxis user
  I want the pipeline to check for relevant prior research and support reruns
  So that I can avoid duplicate effort and build on existing work

  Background:
    Given I am in a temporary directory
    And I have a valid praxis.yaml

  Scenario: Precheck finds relevant prior research
    Given the research library contains artifacts with keyword "roles"
    When a new research run is initiated with topic "scrum roles"
    Then the precheck returns a list of matching artifacts
    And each artifact includes path, date, and title

  Scenario: Precheck finds no relevant research
    Given the research library contains no artifacts matching "quantum-computing"
    When a new research run is initiated with topic "quantum computing"
    Then the precheck returns "No relevant prior artifacts found"

  Scenario: Precheck output is machine-readable
    Given the research library contains matching artifacts
    When a precheck is performed
    Then the output includes structured metadata (path, date, title, keywords)

  Scenario: Rerun links to prior attempt
    Given a completed research run exists for topic "ai-guards"
    When a rerun is initiated with changed assumptions
    Then the rerun metadata includes a reference to the prior run
    And the changed assumptions are recorded

  Scenario: Librarian returns ranked matches
    Given the research library catalog exists
    When the librarian is queried with "knowledge distillation"
    Then it returns artifacts ranked by relevance

  Scenario: Librarian handles empty catalog gracefully
    Given the research library catalog is empty
    When the librarian is queried with any topic
    Then it returns an empty list without error
