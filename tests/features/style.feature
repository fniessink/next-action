Feature: styling

  Scenario: specify a style
    Given a todo.txt with
      """
      A task
      """
    When the user asks for the next action with the style native
    Then Next-action shows the next action with the style native

  Scenario: configure a style
    Given a configuration file with
      """
      style: native
      """
    And a todo.txt with
      """
      A task
      """
    When the user asks for the next action
    Then Next-action shows the next action with the style native

  Scenario: override a configured style
    Given a configuration file with
      """
      style: native
      """
    And a todo.txt with
      """
      A task
      """
    When the user asks for the next action with the style default
    Then Next-action shows the next action with the style default
