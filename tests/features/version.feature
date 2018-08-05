Feature: showing Next-action version number

  Scenario: show version number
    When the user asks for the version number
    Then Next-action shows the version number

  Scenario: show version number and ask for help
    When the user asks for the version number
    And the user asks for help
    Then Next-action shows the version number

  Scenario: show version number and ask for all next actions
    When the user asks for the version number
    And the user asks for all next actions
    Then Next-action shows the version number
