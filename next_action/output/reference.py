"""Reference the next actions with their source filename."""

import argparse

from .. import todotxt


def reference(task: todotxt.Task, namespace: argparse.Namespace) -> str:
    """Decorate the next action with a reference to its source filename."""
    rendered_task = task.text
    if namespace.reference == "always" or namespace.reference == "multiple" and len(namespace.file) > 1:
        rendered_task += f" [{task.filename}]"
    return rendered_task
