Feature: show error message when things go wrong

  Scenario: todo.txt can't be opened
    Given an unreadable todo.txt
    When the user asks for the next action
    Then Next-action tells the user the todo.txt can't be read

  Scenario: unrecognized argument
    When the user asks for the next action with argument "-!"
    Then Next-action tells the user the argument "-!" is unrecognized

  Scenario: unrecognized optional argument
    When the user asks for the next action with argument "foo"
    Then Next-action tells the user the argument "foo" is unrecognized
