Feature: Project Templates
  As a developer starting a new Python CLI project
  I want to use praxis init --template python-cli
  So that I get a complete project structure with hexagonal architecture

  Scenario: Initialize with python-cli template
    Given an empty directory
    When I run praxis init with domain "code", privacy "personal", and template "python-cli"
    Then the exit code should be 0
    And the output should contain "initialized"
    And praxis.yaml should exist with domain "code"
    And pyproject.toml should exist
    And the project should have hexagonal architecture structure
    And the project should have a sample hello command

  Scenario: Template validates domain match
    Given an empty directory
    When I run praxis init with domain "create", privacy "personal", and template "python-cli"
    Then the exit code should be 1
    And the output should contain "domain"

  Scenario: Template generates working tests
    Given an empty directory
    When I run praxis init with domain "code", privacy "personal", and template "python-cli"
    Then the exit code should be 0
    And tests/features/hello.feature should exist
    And tests/step_defs/test_hello.py should exist
    And tests/test_hello_service.py should exist

  Scenario: Unknown template rejected
    Given an empty directory
    When I run praxis init with domain "code", privacy "personal", and template "unknown-template"
    Then the exit code should be 1
    And the output should contain "Unknown template"

  Scenario: Init without template works as before
    Given an empty directory
    When I run praxis init with domain "code" and privacy "personal"
    Then the exit code should be 0
    And the output should contain "initialized"
    And praxis.yaml should exist with domain "code"
    And pyproject.toml should not exist
