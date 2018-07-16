"""Test the next action feature."""

import tempfile


@given("an empty todo.txt")
def empty_todotxt(context):  # pylint: disable=unused-argument
    context.file = tempfile.NamedTemporaryFile(mode="w")
    context.arguments.extend(["--file", context.file.name])

@given("a todo.txt with")
def todotxt(context):
    context.file = tempfile.NamedTemporaryFile(mode="w")
    context.file.write(context.text)
    context.file.seek(0)
    context.arguments.extend(["--file", context.file.name])

@when("the user asks for the next action")
def next_action(context):
    pass

@when("the user asks for the next action with a context")
def next_action_with_context(context):
    context.arguments.append("@some_context")

@when("the user asks for the next action with a project")
def next_action_with_project(context):
    context.arguments.append("+some_project")

@then("Next-action tells the user there's nothing to do")
def nothing_todo(context):
    assert "Nothing to do!" in context.next_action()

@when("the user asks for {number} next actions")
def ask_next_actions(context, number):
    if number == "all":
        context.arguments.append("--all")
    else:
        context.arguments.extend(["--number", str(number)])

@then("Next-action shows the user {number:d} next actions")
def show_next_actions(context, number):
    print(context.next_action())
    assert context.next_action().strip().count("\n") == number - 1
