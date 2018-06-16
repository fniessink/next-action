""" Package for formatting output. """

import argparse

from ..todotxt import Task, Tasks

from .color import colorize
from .reference import reference


def render(tasks: Tasks, namespace: argparse.Namespace) -> str:
    """ Render the tasks using the options in the namespace. """
    reference_task = namespace.reference == "always" or namespace.reference == "multiple" and len(namespace.file) > 1
    render_task = reference if reference_task else lambda task: task.text
    return colorize("\n".join(render_task(task) for task in tasks), namespace.style or "")
