Feature: filter next-actions by context

  Background: a todo.txt file with different contexts
    Given a todo.txt with
      """
      Task A
      Task B @home
      Task C @work
      Task D @home @work
      """

  Scenario: one context
    When the user asks for the next action at home
    Then Next-action shows the next action at home

  Scenario: two contexts
    When the user asks for the next action at home and at work
    Then Next-action shows the next action at home and at work

  Scenario: non-existing context
    When the user asks for the next action at night
    Then Next-action tells the user there's nothing to do

  Scenario: mix of existing and non-existing contexts
    When the user asks for the next action at night and at work
    Then Next-action tells the user there's nothing to do

  Scenario: exclude one context
    When the user asks for the next action not at home
    Then Next-action shows the next action not at home

  Scenario: exclude two contexts
    When the user asks for the next action not at home and not at work
    Then Next-action shows the next action not at home and not at work

  Scenario: exclude non-existing context
    When the user asks for the next action not at night
    Then Next-action shows the user the next action

  Scenario: context in configuration file
    Given a configuration file with
      """
      filters: '@work'
      """
    When the user asks for the next action
    Then Next-action shows the user the next action at work

  Scenario: override context in configuration file
    Given a configuration file with
      """
      filters: '@work'
      """
    When the user asks for the next action at home
    Then Next-action shows the user the next action at home
