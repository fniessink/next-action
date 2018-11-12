Feature: group next actions by context, project, due date or priority

  Background: a todo.txt file with different tasks
    Given a todo.txt with
        """
        Task A
        (A) Task B @home +PaintHouse due:2018-10-10
        (A) Task C @work +WriteProposal due:2018-10-10
        (B) Task D @home @work +PaintHouse +WriteProposal due:2018-10-11
        """

  Scenario: group by context
    When the user asks for all next actions grouped by context
    Then Next-action shows all next actions grouped by context

  Scenario: group by due date
    When the user asks for all next actions grouped by due date
    Then Next-action shows all next actions grouped by due date

  Scenario: group by priority
    When the user asks for all next actions grouped by priority
    Then Next-action shows all next actions grouped by priority

  Scenario: group by project
    When the user asks for all next actions grouped by project
    Then Next-action shows all next actions grouped by project

  Scenario: group by context configured
    Given a configuration file with
      """
      groupby: context
      """
    When the user asks for all next actions grouped by context
    Then Next-action shows all next actions grouped by context

  Scenario: override group by context configuration
    Given a configuration file with
      """
      groupby: context
      """
    When the user asks for all next actions grouped by project
    Then Next-action shows all next actions grouped by project
