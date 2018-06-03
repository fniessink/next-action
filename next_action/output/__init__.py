""" Package for formatting output. """

import argparse
from typing import Sequence

from ..todotxt import Task

from .color import colorize
from .reference import reference


def render(tasks: Sequence[Task], namespace: argparse.Namespace) -> str:
    """ Render the tasks using the options in the namespace. """
    render_task = reference if (namespace.reference == "always" or namespace.reference == "multiple"
                                and len(namespace.file) > 1) else lambda task: task.text
    return colorize("\n".join(render_task(task) for task in tasks), namespace.style or "")
