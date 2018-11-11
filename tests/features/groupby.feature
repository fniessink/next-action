Feature: group next actions by context, project, due date or priority

  Background: a todo.txt file with different tasks
    Given a todo.txt with
        """
        Task A
        Task B @home +PaintHouse
        Task C @work +WriteProposal
        Task D @home @work +PaintHouse +WriteProposal
        """

  Scenario: group by context
    When the user asks for all next actions grouped by context
    Then Next-action shows all next actions grouped by context
