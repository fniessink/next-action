"""Test the next action feature."""

import tempfile

from asserts import assert_equal, assert_in, assert_true
from behave import given, when, then


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
def next_action_at_context(context, contexts):
    contexts = contexts.split(" and at ")
    context.arguments.extend([f"@{c}" for c in contexts])

@when("the user asks for the next action not at {contexts}")
def next_action_not_at_context(context, contexts):
    contexts = contexts.split(" and not at ")
    context.arguments.extend([f"-@{c}" for c in contexts])

@when("the user asks for the next action for {projects}")
def next_action_for_project(context, projects):
    projects = projects.split(" or for ")
    context.arguments.extend([f"+{p}" for p in projects])

@when("the user asks for the next action not for {projects}")
def next_action_not_for_project(context, projects):
    projects = projects.split(" and not for ")
    context.arguments.extend([f"-+{p}" for p in projects])

@then("Next-action tells the user there's nothing to do")
def nothing_todo(context):
    assert_in("Nothing to do!", context.next_action())

@when("the user asks for {number} next actions")
def ask_next_actions(context, number):
    context.arguments.extend(["--all"] if number == "all" else ["--number", str(number)])

@then("Next-action shows the next action at {contexts}")
def show_next_action_at_contexts(context, contexts):
    contexts = contexts.split(" and at ")
    assert_true(all([f"@{c}" in context.next_action() for c in contexts]))

@then("Next-action shows the next action not at {contexts}")
def show_next_action_not_at_contexts(context, contexts):
    contexts = contexts.split(" and not at ")
    assert_true(all([f"@{c}" not in context.next_action() for c in contexts]))

@then("Next-action shows the next action for {projects}")
def show_next_action_for_projects(context, projects):
    projects = projects.split(" or for ")
    assert_true(any([f"+{p}" in context.next_action() for p in projects]))

@then("Next-action shows the next action not for {projects}")
def show_next_action_at_home(context, projects):
    projects = projects.split(" and not for ")
    assert_true(all([f"+{p}" not in context.next_action() for p in projects]))

@then("Next-action shows the user {number} next {action}")
def show_next_actions(context, number, action):
    number = 1 if number == "the" else int(number)
    assert_equal(context.next_action().strip().count("\n"), number - 1)

@then("Next-action tells the user the number argument is invalid")
def show_next_actions(context):
    assert_in("next-action: error: argument -n/--number: invalid number:", context.next_action())
