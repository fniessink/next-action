Feature: open url

  Scenario: open a url
    Given a todo.txt with
      """
      A task with a url https://google.com
      """
    When the user asks for the next action with the open url option
    Then Next-action opens the url "https://google.com" and shows the next action "A task with a url https://google.com"
