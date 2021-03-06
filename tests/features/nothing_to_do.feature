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

  Scenario: nothing to do when all tasks have future creation dates
    Given a todo.txt with
      """
      9999-01-01 A future task
      """
    When the user asks for the next action
    Then Next-action tells the user there's nothing to do

  Scenario: nothing to do when there are no tasks with the given context
    Given a todo.txt with
      """
      Task without context
      """
    When the user asks for the next action at home
    Then Next-action tells the user there's nothing to do

  Scenario: nothing to do when there are no tasks for the given project
    Given a todo.txt with
      """
      Task without project
      """
    When the user asks for the next action for Project
    Then Next-action tells the user there's nothing to do

  Scenario: nothing to do when there are only hidden tasks
    Given a todo.txt with
      """
      Hidden task h:1
      """
    When the user asks for the next action
    Then Next-action tells the user there's nothing to do
