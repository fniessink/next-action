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

  Scenario: override context in configuration file with opposite context
    Given a configuration file with
      """
      filters: '@work'
      """
    When the user asks for the next action not at work
    Then Next-action shows the user the next action not at work

Scenario: excluded context in configuration file
    Given a configuration file with
      """
      filters: -@work
      """
    When the user asks for the next action
    Then Next-action shows the user the next action not at work

  Scenario: override excluded context in configuration file
    Given a configuration file with
      """
      filters: -@work
      """
    When the user asks for the next action at work
    Then Next-action shows the user the next action at work

  Scenario: invalid context
    When the user asks for the next action with an invalid context
    Then Next-action tells the user the context is invalid

  Scenario: invalid excluded context
    When the user asks for the next action with an invalid excluded context
    Then Next-action tells the user the context is invalid

  Scenario: context both included and excluded
    When the user asks for the next action with a context that is both included and excluded
    Then Next-action tells the user the context is both included and excluded

  Scenario: list contexts for tab completion
    When the user asks for the list of contexts
    Then Next-action shows the user the list of filters: @home @work

  Scenario: list excluded contexts for tab completion
    When the user asks for the list of excluded contexts
    Then Next-action shows the user the list of filters: -@home -@work
