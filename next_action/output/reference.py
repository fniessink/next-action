"""Reference the next actions with their source filename."""

from ..todotxt import Task


def reference(task: Task) -> str:
    """Decorate the next action with a reference to its source filename."""
    return "{0} [{1}]".format(task.text, task.filename)
