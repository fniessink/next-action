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
    When the user asks for the next action over due
    Then Next-action shows the user the next action over due

  Scenario: invalid date
    When the user asks for the next action with an invalid due date
    Then Next-action tells the user the due date is invalid

  Scenario: invalid date in todo.txt is ignored
    Given a todo.txt with
      """
      Task A due:1313-13-13
      """
    When the user asks for the next action over due
    Then Next-action tells the user there's nothing to do

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