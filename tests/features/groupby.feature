Feature: group next actions by context, project, due date or priority

  Scenario: group by context
    Given a todo.txt with
      """
      Task
      Another task
      """
    When the user asks for all next actions grouped by context
    Then Next-action shows all next actions grouped by context

  Scenario: group by due date
    Given a todo.txt with
      """
      Task
      """
    When the user asks for all next actions grouped by due date
    Then Next-action shows all next actions grouped by due date

  Scenario: group by priority
    Given a todo.txt with
      """
      Task
      """
    When the user asks for all next actions grouped by priority
    Then Next-action shows all next actions grouped by priority

  Scenario: group by project
    Given a todo.txt with
      """
      Task
      """
    When the user asks for all next actions grouped by project
    Then Next-action shows all next actions grouped by project

  Scenario: group by source
    Given a todo.txt named configured_todo.txt with
      """
      Task
      """
    And a configuration file with
      """
      file: configured_todo.txt
      """
    When the user asks for all next actions grouped by source
    Then Next-action shows all next actions grouped by source

  Scenario: group by context configured
    Given a todo.txt named configured_todo.txt with
      """
      Task
      """
    And a configuration file with
      """
      file: configured_todo.txt
      groupby: context
      """
    When the user asks for all next actions
    Then Next-action shows all next actions grouped by context

  Scenario: override group by context configuration
    Given a todo.txt named configured_todo.txt with
      """
      Task
      """
    And a configuration file with
      """
      file: configured_todo.txt
      groupby: context
      """
    When the user asks for all next actions grouped by project
    Then Next-action shows all next actions grouped by project
