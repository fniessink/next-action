"""Test the version feature."""

from asserts import assert_equal

import next_action


@when("the user asks for the version number")
def argument_version(context):
    """Add the version command line argument."""
    context.arguments.append("--version")


@when("the user asks for help")
def argument_help(context):
    """Add the help command line argument."""
    context.arguments.append("--help")


@then("Next-action shows the version number")
def check_version_number(context):
    """Check that the version number is the current Next-action version."""
    expected = "next-action {0}\n".format(next_action.__version__)
    assert_equal(expected, context.next_action())
