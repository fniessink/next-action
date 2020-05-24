"""Reference the next actions with their source filename."""

import argparse

from .. import todotxt


def reference(task: todotxt.Task, namespace: argparse.Namespace) -> str:
    """Decorate the next action with a reference to its source filename and/or line number."""
    task_reference = None
    if namespace.reference == "always" or namespace.reference == "multiple" and len(namespace.file) > 1:
        task_reference = f"{task.filename}:{task.line_number}" if namespace.line_number else task.filename
    elif namespace.line_number:
        task_reference = str(task.line_number)
    return f"{task.text} [{task_reference}]" if task_reference else task.text
