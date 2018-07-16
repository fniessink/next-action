Feature: show more than one next action

  Scenario: show two next actions
    Given a todo.txt with
      """
      Task A
      Task B
      Task C
      """
    When the user asks for 2 next actions
    Then Next-action shows the user 2 next actions

  Scenario: show all next actions
    Given a todo.txt with
      """
      Task A
      Task B
      Task C
      """
    When the user asks for all next actions
    Then Next-action shows the user 3 next actions