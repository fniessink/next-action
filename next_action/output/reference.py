""" Reference the next actions with their source filename. """

from ..todotxt import Task


def reference(task: Task) -> str:
    """ Reference the next action with its source filename. """
    return "{0} [{1}]".format(task.text, task.filename)
