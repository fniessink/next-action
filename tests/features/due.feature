Feature: limit the next actions by due date

  Scenario: one task due tomorrow
    Given a todo.txt with
      """
      (A) Task A
      (B) Task B due:{tomorrow}
      """
    When the user asks for the next action due tomorrow
    Then Next-action shows the user the next action due tomorrow

  Scenario: one task due yesterday
    Given a todo.txt with
      """
      (A) Task A
      (B) Task B due:{yesterday}
      """
    When the user asks for the next action that's over due
    Then Next-action shows the user the next action that's over due
