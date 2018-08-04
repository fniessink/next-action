Feature: reference next actions with the source file

  Scenario: reference next action always
    Given a todo.txt with
        """
        A task
        """
    When the user asks for the next action
    And the user asks for the next action to be referenced always
    Then Next-action references the source file of the next action

  Scenario: reference next action never
    Given a todo.txt with
        """
        A task
        """
    And a todo.txt with
       """
       Another task
       """
    When the user asks for the next action
    And the user asks for the next action to be referenced never
    Then Next-action doesn't reference the source file of the next action

  Scenario: reference in configuration file
    Given a configuration file with
      """
      reference: always
      """
    And a todo.txt with
        """
        A task
        """
    When the user asks for the next action
    Then Next-action references the source file of the next action

  Scenario: override reference in configuration file
    Given a configuration file with
      """
      reference: always
      """
    When the user asks for the next action
    And the user asks for the next action to be referenced never
    Then Next-action doesn't reference the source file of the next action
