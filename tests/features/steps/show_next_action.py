"""Test the next action feature."""

import tempfile


@given("an empty todo.txt")
def empty_todotxt(context):
    context.file = tempfile.NamedTemporaryFile(mode="w")
    context.arguments.extend(["--file", context.file.name])

@given("a todo.txt with")
def todotxt(context):
    context.execute_steps("given an empty todo.txt")
    context.file.write(context.text)
    context.file.seek(0)

@when("the user asks for the next action")
def next_action(context):
    pass  # No arguments needed

@when("the user asks for the next action at {contexts}")
def next_action_at_home(context, contexts):
    contexts = contexts.split(" and at ")
    context.arguments.extend(["@{0}".format(c) for c in contexts])

@when("the user asks for the next action not at {contexts}")
def next_action_at_home(context, contexts):
    contexts = contexts.split(" and not at ")
    context.arguments.extend(["-@{0}".format(c) for c in contexts])

@when("the user asks for the next action with a project")
def next_action_with_project(context):
    context.arguments.append("+some_project")

@then("Next-action tells the user there's nothing to do")
def nothing_todo(context):
    assert "Nothing to do!" in context.next_action()

@when("the user asks for {number} next actions")
def ask_next_actions(context, number):
    context.arguments.extend(["--all"] if number == "all" else ["--number", str(number)])

@then("Next-action shows the next action at {contexts}")
def show_next_action_at_home(context, contexts):
    contexts = contexts.split(" and at ")
    for c in contexts:
        assert "@{0}".format(c) in context.next_action()

@then("Next-action shows the next action not at {contexts}")
def show_next_action_at_home(context, contexts):
    contexts = contexts.split(" not and at ")
    for c in contexts:
        assert "@{0}".format(c) not in context.next_action()

@then("Next-action shows the user {number:d} next {action}")
def show_next_actions(context, number, action):
    assert context.next_action().strip().count("\n") == number - 1

@then("Next-action tells the user the number argument is invalid")
def show_next_actions(context):
    assert "next-action: error: argument -n/--number: invalid number:" in context.next_action()
