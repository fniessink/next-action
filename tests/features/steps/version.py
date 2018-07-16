"""Test the version feature."""

import next_action


@when("the user asks for the version number")
def argument_version(context):
    context.arguments.append("--version")

@when("the user asks for help")
def argument_help(context):
    context.arguments.append("--help")

@then("Next-action shows the version number")
def check_version_number(context):
    expected = "next-action {0}\n".format(next_action.__version__)
    assert expected == context.next_action()
