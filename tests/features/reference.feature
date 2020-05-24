Feature: reference the source file and/or line number of next actions

  Scenario: reference source file always
    Given a todo.txt with
        """
        A task
        """
    When the user asks for the next action
    And the user asks for the source file to be referenced always
    Then Next-action references the source file of the next action

  Scenario: reference source file never
    Given a todo.txt with
        """
        A task
        """
    And a todo.txt with
       """
       Another task
       """
    When the user asks for the next action
    And the user asks for the source file to be referenced never
    Then Next-action doesn't reference the source file of the next action

  Scenario: reference source file in configuration file
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

  Scenario: override reference source file in configuration file
    Given a configuration file with
      """
      reference: always
      """
    And a todo.txt with
        """
        A task
        """
    When the user asks for the next action
    And the user asks for the source file to be referenced never
    Then Next-action doesn't reference the source file of the next action

  Scenario: reference line number
    Given a todo.txt with
        """
        A task
        """
    When the user asks for the next action
    And the user asks for the line number to be referenced
    Then Next-action references the line number of the next action

  Scenario: reference line number in configuration file
    Given a configuration file with
      """
      line_number: true
      """
    And a todo.txt with
        """
        A task
        """
    When the user asks for the next action
    Then Next-action references the line number of the next action

  Scenario: reference line number and source file
    Given a todo.txt with
        """
        A task
        """
    When the user asks for the next action
    And the user asks for the line number to be referenced
    And the user asks for the source file to be referenced always
    Then Next-action references the line number of the next action
    And Next-action references the source file of the next action
