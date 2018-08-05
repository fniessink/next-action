Feature: validate a Next-action configuration file

  Scenario: configuration file not found
    When the user asks for the next action
    And the user specifies a configuration file that doesn't exist
    Then Next-action tells the user it can't read the configuration file

  Scenario: configuration file not readable
    When the user asks for the next action
    And the user specifies a configuration file that can't be read
    Then Next-action tells the user it can't read the configuration file

  Scenario: empty configuration file
    Given an empty todo.txt
    When the user asks for the next action
    And the user specifies a configuration file that is empty
    Then Next-action tells the user there's nothing to do

  Scenario: configuration file invalid YAML
    Given a configuration file with
      """
      @invalid_yaml
      """
    When the user asks for the next action
    Then Next-action tells the user it can't parse the configuration file

  Scenario: configuration file invalid type
    Given a configuration file with
      """
      number: text
      """
    When the user asks for the next action
    Then Next-action tells the user the configuration file is invalid

  Scenario: configuration file not a mapping
    Given a configuration file with
      """
      [list]
      """
    When the user asks for the next action
    Then Next-action tells the user the configuration file is invalid
