Feature: generate a Next-action configuration file

  Scenario: generate the default configuration file
    When the user asks for a configuration file
    Then Next-action shows the default configuration file

  Scenario: add file-argument
    When the user asks for a configuration file
    And the user specifies the file-argument with value my_todo.txt
    Then Next-action includes the file-argument with value my_todo.txt in the configuration file

  Scenario: add priority-argument
    When the user asks for a configuration file
    And the user specifies the priority-argument with value C
    Then Next-action includes the priority-argument with value C in the configuration file

  Scenario: add number-argument
    When the user asks for a configuration file
    And the user specifies the number-argument with value 3
    Then Next-action includes the number-argument with value 3 in the configuration file

  Scenario: add all-option
    When the user asks for a configuration file
    And the user specifies the all-option
    Then Next-action includes the all-option in the configuration file

  Scenario: add context-filter
    When the user asks for a configuration file
    And the user specifies a context-filter
    Then Next-action includes the context-filter in the configuration file

  Scenario: add project-filter
    When the user asks for a configuration file
    And the user specifies a project-filter
    Then Next-action includes the project-filter in the configuration file

  Scenario: add blocked-option
    When the user asks for a configuration file
    And the user specifies the blocked-option
    Then Next-action includes the blocked-option in the configuration file

  Scenario: add groupby-argument
    When the user asks for a configuration file
    And the user specifies the groupby-argument with value context
    Then Next-action includes the groupby-argument with value context in the configuration file
