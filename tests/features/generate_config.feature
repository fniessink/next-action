Feature: generate a Next-action configuration file

  Scenario: generate the default configuration file
    When the user asks for a configuration file
    Then Next-action shows the default configuration file

  Scenario: add file argument
    When the user asks for a configuration file
    And the user specifies a file argument
    Then Next-action shows the default configuration file with the file argument
