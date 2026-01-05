Feature: Research CLI commands
  As a researcher using Praxis
  I want to manage research sessions via CLI
  So that I can track research workflows systematically

  # Happy paths

  Scenario: Initialize a research session
    Given a valid research corpus exists
    When I run praxis research init with topic "Test Topic" and corpus path
    Then the exit code should be 0
    And the output should contain "Research session initialized"
    And a session.yaml file is created

  Scenario: Check research session status
    Given an active research session exists at phase "intake"
    When I run praxis research status
    Then the exit code should be 0
    And the output should contain "Phase:  intake"
    And the output should contain "Status: active"

  Scenario: Run the next research phase
    Given an active research session exists at phase "intake"
    When I run praxis research run
    Then the exit code should be 0
    And the output should contain "Advanced from intake to rtc"
    And the session phase is now "rtc"

  Scenario: Reject research session at any phase
    Given an active research session exists at phase "rtc"
    When I run praxis research reject with rationale "Not viable"
    Then the exit code should be 0
    And the output should contain "Research rejected"
    And the output should contain "Archived as draft"

  # Error paths

  Scenario: Initialize session without required topic
    Given a valid research corpus exists
    When I run praxis research init without topic
    Then the exit code should be 2
    And the output should contain "Missing option"

  Scenario: Approve when not at synthesis phase
    Given an active research session exists at phase "idas"
    When I run praxis research approve with rationale "Test approval"
    Then the exit code should be 1
    And the output should contain "must be at synthesis phase"

  Scenario: Status when no session exists
    Given no research session exists in the working directory
    When I run praxis research status
    Then the exit code should be 1
    And the output should contain "No active research session found"

  Scenario: JSON output for status
    Given an active research session exists at phase "intake"
    When I run praxis research status with json flag
    Then the exit code should be 0
    And the JSON output should contain "session_id"
    And the JSON output should contain "phase"
