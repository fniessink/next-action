"""Test the next action feature."""

import argparse
import datetime
import tempfile

from asserts import assert_equal, assert_in, assert_regex, assert_not_in, assert_true
from behave import given, when, then

from next_action.output import colorize


def relative_date(days: int) -> str:
    """Return a relative date as ISO-formatted string."""
    return (datetime.date.today() + datetime.timedelta(days=days)).isoformat()


def today() -> str:
    """Return the date of today as an ISO-formatted string."""
    return relative_date(0)


def tomorrow() -> str:
    """Return the date of tomorrow as an ISO-formatted string."""
    return relative_date(1)


def yesterday() -> str:
    """Return the date of yesterday as an ISO-formatted string."""
    return relative_date(-1)


@given("an empty todo.txt")
def empty_todotxt(context):
    """Create an empty temporary todo.txt file that can be read by Next-action."""
    context.files.append(tempfile.NamedTemporaryFile(mode="w"))
    context.arguments.extend(["--file", context.files[-1].name])


@given("an unreadable todo.txt")
def unreadable_todotxt(context):
    """Create an empty temporary todo.txt file, but remove it before we Next-action can open it."""
    context.execute_steps("given an empty todo.txt")
    context.files[-1].close()


@given("a todo.txt with")
def todotxt(context):
    """Add the contents to the temporary todo.txt file."""
    context.execute_steps("given an empty todo.txt")
    context.files[-1].write(context.text.format(tomorrow=tomorrow(), yesterday=yesterday()))
    context.files[-1].seek(0)


@given("a todo.txt named {filename} with")
def named_todotxt(context, filename):
    """Add the contents to the temporary todo.txt file and remember its filename."""
    context.execute_steps(f'given a todo.txt with\n"""\n{context.text}\n"""')
    del context.arguments[-2:]  # Remove the --file argument that was automatically added
    context.files[-1].given_filename = filename


@when("the user asks for the next action")
def next_action(context):  # pylint: disable=unused-argument
    """Next-action shows the next action by default, so no arguments needed."""
    pass


@when("the user asks for the next action from {filename}")
def next_action_from_file(context, filename):
    """Remove the other file arguments."""
    real_filename = [file.name for file in context.files if file.given_filename == filename][0]
    context.arguments.extend(["--file", real_filename])


@when("the user asks for the next action due {due_date}")
def next_action_due(context, due_date):
    """Add the due argument."""
    context.arguments.extend(["--due", due_date])


@when("the user asks for the next action over due")
def next_action_over_due(context):
    """Add the over due argument."""
    context.arguments.extend(["--overdue"])


@when("the user asks for all next actions with at least priority A")
def next_action_with_min_prio(context):
    """Add the priority argument with a minimum priority."""
    context.arguments.extend(["--all", "--priority", "A"])


@when("the user asks for all next actions with a priority")
def next_action_with_a_prio(context):
    """Add the priority argument."""
    context.arguments.extend(["--all", "--priority"])


@when("the user asks for all next actions with an invalid priority")
def next_action_with_invalid_prio(context):
    """Add an invalid priority argument."""
    context.arguments.extend(["--all", "--priority", "1"])


@when("the user asks for all next actions grouped by {groupby}")
def next_action_groupby(context, groupby):
    """Add the groupby argument."""
    context.arguments.extend(["--all", "--groupby", groupby.replace("due date", "duedate")])


@when("the user asks for the blocked tasks")
def next_action_with_blocked_tasks(context):
    """Add the blocked option."""
    context.arguments.append("--blocked")


@when("the user asks for the next action with the style {style}")
def next_action_with_a_style(context, style):
    """Add the style argument."""
    context.arguments.extend(["--style", style])


@when('the user asks for the next action with argument "{argument}"')
def next_action_with_invalid_arg(context, argument):
    """Add an invalid argument."""
    if not argument.startswith("-"):
        context.arguments.append("--")
    context.arguments.append(argument)


@when("the user asks for the next action to be referenced {reference}")
def next_action_ref_always(context, reference):
    """Add the reference argument."""
    context.arguments.extend(["--reference", reference])


@when("the user asks for the next action at {contexts}")
def next_action_at_context(context, contexts):
    """Add the contexts to the command line arguments."""
    contexts = contexts.split(" and at ")
    context.arguments.extend([f"@{c}" for c in contexts])


@when("the user asks for the next action with an invalid {argument_type}")
def next_action_invalid_argument(context, argument_type):
    """Add an invalid context, project or due date to the command line arguments."""
    if "due date" in argument_type:
        arguments = ["--due", "2018-02-30"]
    else:
        argument = "@" if "context" in argument_type else "+"
        arguments = [f"-{argument}" if "excluded" in argument_type else argument]
    context.arguments.extend(arguments)


@when("the user asks for the next action with a due date with extra tokens")
def next_action_extra_tokens(context):
    """Add an invalid due date with extra tokens."""
    context.arguments.extend(["--due", "extra 2018-01-01"])


@when("the user asks for the next action with a {context_or_project} that is both included and excluded")
def next_action_c_or_p_in_and_ex(context, context_or_project):
    """Both include and exclude an context or project."""
    argument_type = "@" if "context" in context_or_project else "+"
    context.arguments.extend([f"{argument_type}name", f"-{argument_type}name"])


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


@when("the user asks for {number} next actions")
def ask_next_actions(context, number):
    """Add either the number of the all command line option to the command line arguments."""
    context.arguments.extend(["--all"] if number == "all" else ["--number", str(number)])


@when("the user asks for the list of {argument_type}")
def ask_for_list_of_arguments(context, argument_type):
    """Add the list filters argument."""
    if argument_type.endswith(" arguments"):
        argument_type = argument_type[:-len(" arguments")]
    context.arguments.extend(["--list-arguments", f"{argument_type.replace(' ', '_').replace('-', '_')}"])


@then("Next-action tells the user there's nothing to do")
def nothing_todo(context):
    """Check that Next-action tells the user there's nothing to do."""
    assert_in("Nothing to do!", context.next_action())


@then("Next-action references the source file of the next action")
def check_reference(context):
    """Check the filename reference."""
    assert_in("/", context.next_action())


@then("Next-action doesn't reference the source file of the next action")
def check_does_not_reference(context):
    """Check the filename reference."""
    assert_not_in("/", context.next_action())


@then('Next-action shows the next action "{action}"')
def show_named_next_action(context, action):
    """Check that the named next action is shown."""
    assert_in(action, context.next_action())


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


@then('Next-action shows the blocked task "{task}"')
def show_blocked_task(context, task):
    """Check that the task is shown as blocked task."""
    assert_in(task, context.next_action())


@then("Next-action shows the user the next action due tomorrow")
def show_next_action_due_tomorrow(context):
    """Check that the next action is due tomorrow."""
    assert_in(tomorrow(), context.next_action())


@then("Next-action shows the user the next action over due")
def show_next_action_over_due(context):
    """Check that the next action was due yesterday."""
    assert_in(yesterday(), context.next_action())


@then("Next-action shows the user all next actions with at least priority A")
def show_next_action_with_min_prio(context):
    """Check that the next actions have the minimum priority."""
    for line in context.next_action().strip().split("\n"):
        assert_in("(A)", line)


@then("Next-action shows the user all next actions with a priority")
def show_next_action_with_a_prio(context):
    """Check that the next actions have a priority."""
    for line in context.next_action().strip().split("\n"):
        assert_regex(line, "([A-Z])")


@then("Next-action shows the user {number} next {actions}")
def show_next_actions(context, number, actions):  # pylint: disable=unused-argument
    """Check the number of next actions shown."""
    number = 1 if number == "the" else int(number)
    assert_equal(context.next_action().strip().count("\n"), number - 1)


@then("Next-action tells the user the number argument is invalid")
def invalid_number_error_message(context):
    """Check the error message."""
    assert_in("next-action: error: argument -n/--number: invalid number:", context.next_action())


@then("Next-action tells the user the priority argument is invalid")
def invalid_priority_error_message(context):
    """Check the error message."""
    assert_in("next-action: error: argument -p/--priority: invalid choice:", context.next_action())


@then("Next-action shows the next action with the style {style}")
def show_next_action_with_style(context, style):
    """Check the style."""
    namespace = argparse.Namespace()
    namespace.style = style
    assert_equal(colorize("A task", namespace), context.next_action().strip())


@then("Next-action shows all next actions grouped by {groupby}")
def show_next_actions_grouped_by(context, groupby):
    """Show all next actions grouped by context, project, ..."""
    expected_header = context.files[-1].name if groupby == "source" \
        else f"No {groupby.replace('due date', 'due date')}"
    assert_in(f"{expected_header}:\n- Task\n", context.next_action())


@then("Next-action shows the user the list of {argument_type}: {arguments}")
def show_list_of_arguments(context, argument_type, arguments):  # pylint: disable=unused-argument
    """Check the arguments."""
    if "..." in arguments:
        arguments = arguments.strip(".")
        assert_true(context.next_action().startswith(arguments))
    else:
        assert_equal(arguments, context.next_action().strip())


@then('Next-action tells the user the argument "{argument}" is unrecognized')
def unrecognized_arg_error_message(context, argument):
    """Check the error message."""
    assert_regex(context.next_action(), f".*unrecognized arguments?: {argument}.*")


@then("Next-action tells the user the {argument} is invalid")
def invalid_argument_error_message(context, argument):
    """Check the error message."""
    if "context" in argument or "project" in argument:
        message = f"argument <context|project>: {argument} name missing"
    else:
        message = "argument -d/--due: invalid date: "
    assert_in(f"next-action: error: {message}", context.next_action())


@then("Next-action tells the user the {context_or_project} is both included and excluded")
def c_or_p_in_and_ex_error_message(context, context_or_project):
    """Check the error message."""
    argument_type = "@" if "context" in context_or_project else "+"
    assert_in(f"next-action: error: {argument_type}name is both included and excluded",
              context.next_action())


@then("Next-action tells the user the todo.txt can't be read")
def unreadable_file_error_messge(context):
    """Check the error message."""
    assert_in("next-action: error: can't open file: ", context.next_action())
