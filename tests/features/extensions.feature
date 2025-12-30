Feature: Extension Management
  As a Praxis user
  I want to manage extensions
  So that I can add capabilities to my workflow

  Scenario: List available extensions
    Given a valid workspace with praxis-ai at PRAXIS_HOME
    When I call list_extensions
    Then the extension list should contain "render-run"
    And the extension list should contain "template-python-cli"

  Scenario: Add extension not in registry
    Given a valid workspace with praxis-ai at PRAXIS_HOME
    When I call add_extension with name "nonexistent-extension"
    Then the add result should be unsuccessful
    And the add result error should contain "not found"

  Scenario: List available examples
    Given a valid workspace with praxis-ai at PRAXIS_HOME
    When I call list_examples
    Then the example list should contain "uat-praxis-code"
    And the example list should contain "opinions-framework"

  Scenario: Add example not in registry
    Given a valid workspace with praxis-ai at PRAXIS_HOME
    When I call add_example with name "nonexistent-example"
    Then the example add result should be unsuccessful
    And the example add result error should contain "not found"
