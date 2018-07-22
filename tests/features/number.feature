Feature: show more than one next action

  Background: a simple todo.txt file
    Given a todo.txt with
      """
      Task A
      Task B
      Task C
      """

  Scenario: two next actions
    When the user asks for 2 next actions
    Then Next-action shows the user 2 next actions

  Scenario: all next actions
    When the user asks for all next actions
    Then Next-action shows the user 3 next actions

  Scenario: more next actions than available
    When the user asks for 4 next actions
    Then Next-action shows the user 3 next actions

  Scenario: zero next actions
    When the user asks for 0 next actions
    Then Next-action tells the user the number argument is invalid

  Scenario: a negative number of next actions
    When the user asks for -2 next actions
    Then Next-action tells the user the number argument is invalid

  Scenario: an invalid number of next actions
    When the user asks for x next actions
    Then Next-action tells the user the number argument is invalid

  Scenario: number in configuration file
    Given a configuration file with
      """
      number: 3
      """
    When the user asks for the next action
    Then Next-action shows the user 3 next actions

  Scenario: override number in configuration file
    Given a configuration file with
      """
      number: 3
      """
    When the user asks for 2 next actions
    Then Next-action shows the user 2 next actions
