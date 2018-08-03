Feature: filter next-actions by project

  1. Specify projects
  2. Read result
  1a. Project doesn't exist
  1b. Project name is empty


  Background: a todo.txt file with different projects
    Given a todo.txt with
      """
      Task A
      Task B +GarageSale
      Task C +PaintHouse
      Task D +GarageSale +PaintHouse
      """

  Scenario: one project
    When the user asks for the next action for GarageSale
    Then Next-action shows the next action for GarageSale

  Scenario: two projects
    When the user asks for the next action for GarageSale or for PaintHouse
    Then Next-action shows the next action for GarageSale or for PaintHouse

  Scenario: non-existing project
    When the user asks for the next action for DogHouse
    Then Next-action tells the user there's nothing to do

  Scenario: mix of existing and non-existing projects
    When the user asks for the next action for DogHouse or for PaintHouse
    Then Next-action shows the next action for PaintHouse

  Scenario: exclude one project
    When the user asks for the next action not for GarageSale
    Then Next-action shows the next action not for GarageSale

  Scenario: exclude two projects
    When the user asks for the next action not for GarageSale and not for PaintHouse
    Then Next-action shows the next action not for GarageSale and not for PaintHouse

  Scenario: exclude non-existing project
    When the user asks for the next action not for DogHouse
    Then Next-action shows the user the next action

  Scenario: project in configuration file
    Given a configuration file with
      """
      filters: +PaintHouse
      """
    When the user asks for the next action
    Then Next-action shows the user the next action for PaintHouse

  Scenario: override project in configuration file
    Given a configuration file with
      """
      filters: +PaintHouse
      """
    When the user asks for the next action at GarageSale
    Then Next-action shows the user the next action for GarageSale

  Scenario: invalid project
    When the user asks for the next action with an invalid project
    Then Next-action tells the user the project is invalid

  Scenario: invalid excluded project
    When the user asks for the next action with an invalid excluded project
    Then Next-action tells the user the project is invalid

  Scenario: project both included and excluded
    When the user asks for the next action with a project that is both included and excluded
    Then Next-action tells the user the project is both included and excluded
