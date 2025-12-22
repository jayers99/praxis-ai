Feature: Helloworld command
  As a CLI user
  I want to greet someone
  So that I can verify the CLI is working

  Scenario: Default greeting
    When I run the helloworld command
    Then I should see "Hello, World!"

  Scenario: Custom greeting
    When I run the helloworld command with name "Praxis"
    Then I should see "Hello, Praxis!"
