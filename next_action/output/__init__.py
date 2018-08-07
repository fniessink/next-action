"""Package for formatting output."""

import argparse

from ..todotxt import Task, Tasks

from .color import colorize
from .reference import reference


def render_task(task: Task, namespace: argparse.Namespace, level: int = 0) -> str:
    """Render one task."""
    indent = (level - 1) * "  " + "- " if level else ""
    rendered_task = reference(task, namespace)
    rendered_task = indent + colorize(rendered_task, namespace.style or "")
    if namespace.blocked:
        blocked_tasks = task.blocked_tasks()
        if blocked_tasks:
            rendered_task += "\n" + level * "  " + "blocks:"
            for blocked_task in blocked_tasks:
                rendered_task += "\n" + render_task(blocked_task, namespace, level + 1)
    return rendered_task


def render(tasks: Tasks, namespace: argparse.Namespace) -> str:
    """Render the tasks using the options in the namespace."""
    return "\n".join(render_task(task, namespace) for task in tasks)
