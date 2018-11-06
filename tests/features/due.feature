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

  Scenario: one task due on specific date
    Given a todo.txt with
      """
      (A) Task A
      (B) Task B due:2018-11-01
      """
    When the user asks for the next action due 2018-11-01
    Then Next-action shows the user the next action "(B) Task B due:2018-11-01"

  Scenario: invalid date
    When the user asks for the next action with an invalid due date
    Then Next-action tells the user the due date is invalid

  Scenario: extra tokens
    When the user asks for the next action with a due date with extra tokens
    Then Next-action tells the user the due date is invalid

  Scenario: invalid date in todo.txt is ignored
    Given a todo.txt with
      """
      Task A due:1313-13-13
      """
    When the user asks for the next action over due
    Then Next-action tells the user there's nothing to do

  Scenario: override default number in configuration file
    Given a configuration file with
      """
      number: 3
      """
    And a todo.txt with
      """
      (A) Task A
      (B) Task B @home +GarageSale
      Task C @work +PaintHouse
      Task D @home @work +PaintHouse
      """
    When the user asks for the next action
    Then Next-action shows the user 3 next actions

  Scenario: override configured number on the command line
    Given a configuration file with
      """
      number: 3
      """
    And a todo.txt with
      """
      (A) Task A
      (B) Task B @home +GarageSale
      Task C @work +PaintHouse
      Task D @home @work +PaintHouse
      """
    When the user asks for 2 next actions
    Then Next-action shows the user 2 next actions
