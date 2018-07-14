"""Code to run before and after certain events during testing."""

import subprocess
import tempfile


def before_all(context):
    """Create a shortcut for invoking Next-action."""
    context.next_action = lambda: subprocess.run(context.arguments, stdout=subprocess.PIPE, encoding="utf-8").stdout

def before_scenario(context, scenario):  # pylint: disable=unused-argument
    """Create a temporary todo.txt file."""
    context.file = tempfile.NamedTemporaryFile(mode="w")
    context.arguments = ["next-action"]
