"""Code to run before and after certain events during testing."""

import subprocess


def before_all(context):
    """Create a shortcut for invoking Next-action."""
    def run_next_action():
        """ Run Next-action and return both stderr and stdout. """
        result = subprocess.run(context.arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        return result.stdout + result.stderr

    context.next_action = run_next_action

def before_scenario(context, scenario):  # pylint: disable=unused-argument
    """Create a temporary todo.txt file."""
    context.arguments = ["next-action"]
