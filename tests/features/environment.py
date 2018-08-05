"""Code to run before and after certain events during testing."""

import subprocess  # nosec


def before_all(context):
    """Create a shortcut for invoking Next-action."""
    def run_next_action():
        """Run Next-action and return both stderr and stdout."""
        result = subprocess.run(context.arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        return result.stdout + result.stderr

    context.next_action = run_next_action
    subprocess.run(["coverage", "erase"])


def before_scenario(context, scenario):  # pylint: disable=unused-argument
    """Set up arguments."""
    context.files = []
    context.arguments = ["coverage", "run", "--omit", ".venv/*", "--branch", "--parallel-mode", ".venv/bin/next-action"]


def after_all(context):  # pylint: disable=unused-argument
    """Create coverage report."""
    subprocess.run(["coverage", "combine"])
    subprocess.run(["coverage", "html", "--rcfile", ".coveragerc-behave", "--directory", "build/htmlcov"])
