"""Test the next action feature."""

import datetime
import tempfile

from asserts import assert_equal, assert_in, assert_true
from behave import given, when, then


def relative_date(days: int) -> str:
    """Return a relative date as ISO-formatted string."""
    return (datetime.date.today() + datetime.timedelta(days=days)).isoformat()


def tomorrow() -> str:
    """Return the date of tomorrow as an ISO-formatted string."""
    return relative_date(1)


def yesterday() -> str:
    """Return the date of yesterday as an ISO-formatted string."""
    return relative_date(-1)


@given("an empty todo.txt")
def empty_todotxt(context):
    """Create an empty temporary todo.txt file that can be read by Next-action."""
    context.file = tempfile.NamedTemporaryFile(mode="w")
    context.arguments.extend(["--file", context.file.name])


@given("a todo.txt with")
def todotxt(context):
    """Add the contents to the temporary todo.txt file."""
    context.execute_steps("given an empty todo.txt")
    context.file.write(context.text.format(tomorrow=tomorrow(), yesterday=yesterday()))
    context.file.seek(0)


@when("the user asks for the next action")
def next_action(context):
    """Next-action shows the next action by default, so no arguments needed."""
    pass


@when("the user asks for the next action due tomorrow")
def next_action_due(context):
    """Add the due argument."""
    context.arguments.extend(["--due", tomorrow()])


@when("the user asks for the next action that's over due")
def next_action_over_due(context):
    """Add the over due argument."""
    context.arguments.extend(["--overdue"])


@when("the user asks for the next action at {contexts}")
def next_action_at_context(context, contexts):
    """Add the contexts to the command line arguments."""
    contexts = contexts.split(" and at ")
    context.arguments.extend([f"@{c}" for c in contexts])


@when("the user asks for the next action not at {contexts}")
def next_action_not_at_context(context, contexts):
    """Add the excluded contexts to the command line arguments."""
    contexts = contexts.split(" and not at ")
    context.arguments.extend([f"-@{c}" for c in contexts])


@when("the user asks for the next action for {projects}")
def next_action_for_project(context, projects):
    """Add the projects to the command line arguments."""
    projects = projects.split(" or for ")
    context.arguments.extend([f"+{p}" for p in projects])


@when("the user asks for the next action not for {projects}")
def next_action_not_for_project(context, projects):
    """Add the excluded projects to the command line arguments."""
    projects = projects.split(" and not for ")
    context.arguments.extend([f"-+{p}" for p in projects])


@then("Next-action tells the user there's nothing to do")
def nothing_todo(context):
    """Check that Next-action tells the user there's nothing to do."""
    assert_in("Nothing to do!", context.next_action())


@when("the user asks for {number} next actions")
def ask_next_actions(context, number):
    """Add either the number of the all command line option to the command line arguments."""
    context.arguments.extend(["--all"] if number == "all" else ["--number", str(number)])


@then("Next-action shows the next action at {contexts}")
def show_next_action_at_contexts(context, contexts):
    """Check that the next action has the required contexts."""
    contexts = contexts.split(" and at ")
    assert_true(all([f"@{c}" in context.next_action() for c in contexts]))


@then("Next-action shows the next action not at {contexts}")
def show_next_not_at_contexts(context, contexts):
    """Check that the next action doesn't have the excluded contexts."""
    contexts = contexts.split(" and not at ")
    assert_true(all([f"@{c}" not in context.next_action() for c in contexts]))


@then("Next-action shows the next action for {projects}")
def show_next_action_for_projects(context, projects):
    """Check that the next action has the required projects."""
    projects = projects.split(" or for ")
    assert_true(any([f"+{p}" in context.next_action() for p in projects]))


@then("Next-action shows the next action not for {projects}")
def show_next_action_at_home(context, projects):
    """Check that the next action doesn't have the excluded projects."""
    projects = projects.split(" and not for ")
    assert_true(all([f"+{p}" not in context.next_action() for p in projects]))


@then("Next-action shows the user the next action due tomorrow")
def show_next_action_due_tomorrow(context):
    """Check that the next action is due tomorrow."""
    assert_in(tomorrow(), context.next_action())


@then("Next-action shows the user the next action that's over due")
def show_next_action_over_due(context):
    """Check that the next action was due yesterday."""
    assert_in(yesterday(), context.next_action())


@then("Next-action shows the user {number} next {action}")
def show_next_actions(context, number, action):
    """Check the number of next actions shown."""
    number = 1 if number == "the" else int(number)
    assert_equal(context.next_action().strip().count("\n"), number - 1)


@then("Next-action tells the user the number argument is invalid")
def check_eror_messge(context):
    """Check the error message."""
    assert_in("next-action: error: argument -n/--number: invalid number:", context.next_action())
