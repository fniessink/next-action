Feature: time travel

  Scenario: pretend it's tomorrow
    Given a todo.txt with
      """
        (A) A high prio task
        A task due:{tomorrow}
      """
    When the user asks for the next action due today
    Then Next-action shows the user the next action with priority A
    When the user asks for the next action due today
    And the user wants to pretend it's tomorrow
    Then Next-action shows the user the next action due tomorrow

  Scenario: pretend it's yesterday
    Given a todo.txt with
      """
        (A) A high prio task
        A task due:{yesterday}
      """
    When the user asks for the next action over due
    Then Next-action shows the user the next action due yesterday
    When the user asks for the next action over due
    And the user wants to pretend it's yesterday
    Then Next-action shows the user the next action with priority A

  Scenario: pretend it's today
    Given a todo.txt with
      """
        (A) A high prio task
        A task due:{yesterday}
      """
    When the user asks for the next action over due
    And the user wants to pretend it's today
    Then Next-action shows the user the next action with due today

 Scenario: list arguments for tab completion
    When the user asks for the list of time travel arguments
    Then Next-action shows the user the list of time travel arguments: tomorrow yesterday Monday Tuesday ...
