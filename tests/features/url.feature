Feature: open url

  Scenario: open a url
    Given a configuration file with
      """
      reference: never  # Without a config file we won't get to 100% branch coverage
      """
    And a todo.txt with
      """
      A task with a url https://google.com
      """
    When the user asks for the next action with the open urls option
    Then Next-action opens the url "https://google.com" and shows the next action "A task with a url https://google.com"

  Scenario: configure open url
    Given a configuration file with
      """
      open_urls: true
      """
    And a todo.txt with
      """
      A task with a url https://google.com
      """
    When the user asks for the next action
    Then Next-action opens the url "https://google.com" and shows the next action "A task with a url https://google.com"
