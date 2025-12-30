Feature: Workspace Management
  As a Praxis user
  I want to initialize and manage my workspace
  So that I can organize my extensions, examples, and projects

  Scenario: Initialize workspace with PRAXIS_HOME set
    Given PRAXIS_HOME is set to a temp directory
    And the temp workspace directory exists
    When I call init_workspace
    Then the init result should be successful
    And the directory "extensions" should exist in workspace
    And the directory "examples" should exist in workspace
    And the directory "projects" should exist in workspace
    And the file "workspace-config.yaml" should exist in workspace

  Scenario: Get workspace info
    Given PRAXIS_HOME is set to a temp directory
    And a valid workspace exists at PRAXIS_HOME
    When I call get_workspace_info
    Then the workspace info should contain the config
    And the workspace info should have extensions_path
    And the workspace info should have examples_path
    And the workspace info should have projects_path

  Scenario: Workspace requires PRAXIS_HOME
    Given PRAXIS_HOME is not set
    When I call require_praxis_home
    Then a ValueError should be raised with message containing "PRAXIS_HOME"
