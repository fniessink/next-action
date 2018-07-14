"""Test the next action feature."""

@given("an empty todo.txt")
def empty_todotxt(context):  # pylint: disable=unused-argument
    pass

@given("a todo.txt with")
def todotxt(context):
    context.file.write(context.text)

@when("the user asks for the next action")
def next_action(context):
    context.arguments.extend(["--file", context.file.name])

@when("the user asks for the next action with a context")
def next_action_with_context(context):
    context.arguments.append("@some_context")

@when("the user asks for the next action with a project")
def next_action_with_project(context):
    context.arguments.append("+some_project")

@then("Next-action tells the user there's nothing to do")
def nothing_todo(context):
    assert "Nothing to do!" in context.next_action()
