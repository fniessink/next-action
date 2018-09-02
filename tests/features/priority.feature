Feature: limit the next actions by priority

  Background:
    Given a todo.txt with
      """
      (A) Task A
      (B) Task B
      Task C
      """

  Scenario: filter tasks with a minimum priority
    When the user asks for all next actions with at least priority A
    Then Next-action shows the user all next actions with at least priority A

  Scenario: filter tasks with a priority
    When the user asks for all next actions with a priority
    Then Next-action shows the user all next actions with a priority

  Scenario: filter tasks with an invalid priority
    When the user asks for all next actions with an invalid priority
    Then Next-action tells the user the priority argument is invalid

  Scenario: priority in configuration file
    Given a configuration file with
      """
      priority: A
      """
    When the user asks for all next actions
    Then Next-action shows the user all next actions with at least priority A

  Scenario: override priority in configuration file
    Given a configuration file with
      """
      priority: A
      """
    When the user asks for all next actions with a priority
    Then Next-action shows the user all next actions with a priority

  Scenario: list priorities for tab completion
    When the user asks for the list of priorities
    Then Next-action shows the user the list of priorities: A B
