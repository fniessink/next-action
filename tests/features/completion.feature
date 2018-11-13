Feature: list command line options and arguments for tab completion

  Background: a todo.txt file with different contexts and projects
    Given a todo.txt with
      """
      (A) Task A
      (B) Task B @home +GarageSale
      Task C @work +PaintHouse
      Task D @home @work +PaintHouse
      """

  Scenario: list all command-line arguments
    When the user asks for the list of all arguments
    Then Next-action shows the user the list of all arguments: + -+ --all --blocked...

  Scenario: list contexts
    When the user asks for the list of @ arguments
    Then Next-action shows the user the list of contexts: @home @work

  Scenario: list excluded contexts
    When the user asks for the list of -@ arguments
    Then Next-action shows the user the list of excluded contexts: -@home -@work

  Scenario: list projects
    When the user asks for the list of + arguments
    Then Next-action shows the user the list of projects: +GarageSale +PaintHouse

  Scenario: list excluded projects
    When the user asks for the list of -+ arguments
    Then Next-action shows the user the list of excluded projects: -+GarageSale -+PaintHouse

  Scenario: list priorities
    When the user asks for the list of --priority arguments
    Then Next-action shows the user the list of priorities: A B

  Scenario: list groupby options
    When the user asks for the list of --groupby arguments
    Then Next-action shows the user the list of groupby arguments: context duedate priority project source

  Scenario: list reference options
    When the user asks for the list of --reference arguments
    Then Next-action shows the user the list of reference arguments: always multiple never

  Scenario: list styles
    When the user asks for the list of --style arguments
    Then Next-action shows the user the list of styles: abap algol algol_nu ...
