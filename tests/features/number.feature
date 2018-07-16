Feature: show more than one next action

  Background: A simple todo.txt file
    Given a todo.txt with
      """
      Task A
      Task B
      Task C
      """

  Scenario: show two next actions
    When the user asks for 2 next actions
    Then Next-action shows the user 2 next actions

  Scenario: show all next actions
    When the user asks for all next actions
    Then Next-action shows the user 3 next actions

  Scenario: ask for more next actions than available
    When the user asks for 4 next actions
    Then Next-action shows the user 3 next actions

  Scenario: ask for a negative number of next actions
    When the user asks for -2 next actions
    Then Next-action tells the user the number argument is invalid

  Scenario: ask for a invalid number of next actions
    When the user asks for x next actions
    Then Next-action tells the user the number argument is invalid
