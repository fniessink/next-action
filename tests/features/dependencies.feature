Feature: task dependencies

  Scenario: task after another task
    Given a todo.txt with
      """
      Task 1 after:task2
      Task 2 id:task2
      """
    When the user asks for the next action
    Then Next-action shows the next action "Task 2 id:task2"

  Scenario: task before another task
    Given a todo.txt with
      """
      Task 1 before:task2
      Task 2 id:task2
      """
    When the user asks for the next action
    Then Next-action shows the next action "Task 1 before:task2"

  Scenario: task after two other tasks
    Given a todo.txt with
      """
      Task 1 after:task2 after:task3
      Task 2 id:task2
      Task 3 id:task3
      """
    When the user asks for the next action
    Then Next-action shows the next action "Task 2 id:task2"

  Scenario: task before two other tasks
    Given a todo.txt with
      """
      Task 1 before:task2 before:task3
      Task 2 id:task2
      Task 3 id:task3
      """
    When the user asks for the next action
    Then Next-action shows the next action "Task 1 before:task2 before:task3"

  Scenario: task after task after task
    Given a todo.txt with
      """
      Task 1 after:task2
      Task 2 id:task2 after:task3
      Task 3 id:task3
      """
    When the user asks for the next action
    Then Next-action shows the next action "Task 3 id:task3"
