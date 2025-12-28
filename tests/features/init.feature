Feature: Praxis Init CLI
  As a developer starting a new project
  I want to initialize a Praxis governance structure
  So that I can govern my AI-assisted work from the start

  Scenario: Initialize new project with flags
    Given an empty directory
    When I run praxis init with domain "code" and privacy "personal"
    Then the exit code should be 0
    And the output should contain "initialized"
    And praxis.yaml should exist with domain "code"
    And CLAUDE.md should exist
    And docs/capture.md should exist

  Scenario: Init fails if praxis.yaml exists
    Given a directory with existing praxis.yaml
    When I run praxis init with domain "code" and privacy "personal"
    Then the exit code should be 1
    And the output should contain "exists"

  Scenario: Init with --force overwrites existing files
    Given a directory with existing praxis.yaml
    When I run praxis init with --force
    Then the exit code should be 0
    And the output should contain "initialized"
    And praxis.yaml should be updated

  Scenario: Invalid domain rejected
    Given an empty directory
    When I run praxis init with domain "invalid" and privacy "personal"
    Then the exit code should be 1
    And the output should contain "Invalid domain"

  Scenario: Invalid privacy rejected
    Given an empty directory
    When I run praxis init with domain "code" and privacy "invalid"
    Then the exit code should be 1
    And the output should contain "Invalid privacy"
