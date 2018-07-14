Feature: showing there's nothing to do

  Scenario: nothing to do when todo.txt is empty
    Given an empty todo.txt
    When the user asks for the next action
    Then Next-action tells the user there's nothing to do

  Scenario: nothing to do when all tasks are completed
    Given a todo.txt with
      """
      x One completed task
      """
    When the user asks for the next action
    Then Next-action tells the user there's nothing to do

  Scenario: nothing to do when all tasks are future tasks
    Given a todo.txt with
      """
      A future task t:9999-01-01
      """
    When the user asks for the next action
    Then Next-action tells the user there's nothing to do

  Scenario: nothing to do when there are no tasks with the given context
    Given a todo.txt with
      """
      Task without context
      """
    When the user asks for the next action with a context
    Then Next-action tells the user there's nothing to do

  Scenario: nothing to do when there are no tasks with the given project
    Given a todo.txt with
      """
      Task without project
      """
    When the user asks for the next action with a project
    Then Next-action tells the user there's nothing to do
