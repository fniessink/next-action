Feature: select todo.txt file(s) to read

  Scenario: configure file in configuration file
    Given a todo.txt named configured_todo.txt with
      """
      A task
      """
    And a configuration file with
      """
      file: configured_todo.txt
      """
    When the user asks for the next action
    Then Next-action shows the next action "A task"

  Scenario: override configured file
    Given a todo.txt named configured_todo.txt with
      """
      (A) A high priority task
      """
    And a configuration file with
      """
      file: configured_todo.txt
      """
    And a todo.txt named another_todo.txt with
      """
      Another task
      """
    When the user asks for the next action from another_todo.txt
    Then Next-action shows the next action "Another task"
