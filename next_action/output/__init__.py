"""Package for formatting output."""

import argparse
from typing import Iterable, List

from pygments.styles import get_all_styles

from .. import todotxt, arguments
from .color import colorize
from .reference import reference
from .warning import invalid_arguments


def render_blocked_tasks(task: todotxt.Task, namespace: argparse.Namespace, level: int = 0) -> str:
    """Render the tasks blocked by the task, if any."""
    rendered_blocked_tasks = ""
    if namespace.blocked:
        blocked_tasks = task.blocked_tasks()
        if blocked_tasks:
            rendered_blocked_tasks += "\n" + level * "  " + "blocks:"
            for blocked_task in blocked_tasks:
                rendered_blocked_tasks += "\n" + render_task(blocked_task, namespace, level + 1)
    return rendered_blocked_tasks


def render_task(task: todotxt.Task, namespace: argparse.Namespace, level: int = 0) -> str:
    """Render one task."""
    indent = (level - 1) * "  " + "- " if level else ""
    rendered_task = colorize(reference(task, namespace), namespace)
    rendered_blocked_tasks = render_blocked_tasks(task, namespace, level)
    return indent + rendered_task + rendered_blocked_tasks


def render_tasks(tasks: todotxt.Tasks, namespace: argparse.Namespace) -> str:
    """Render the tasks using the options in the namespace."""
    return "\n".join(render_task(task, namespace) for task in tasks)


def render_grouped_tasks(tasks: todotxt.Tasks, namespace: argparse.Namespace) -> str:
    """Render the tasks grouped using the options in the namespace."""
    get_groups = dict(
        project=lambda task: task.projects() or [None],
        context=lambda task: task.contexts() or [None],
        priority=lambda task: [task.priority() or None],
        duedate=lambda task: [task.due_date() or None],
        source=lambda task: [task.filename])[namespace.groupby]
    no_group_label = f"No {namespace.groupby}".replace("duedate", "due date")
    groups: List[str] = []
    for task in tasks:
        for group in sorted(get_groups(task)):
            if group not in groups:
                groups.append(group)
    lines = []
    for group in groups:
        lines.append(f"{group or no_group_label}:")
        lines.extend(render_task(task, namespace, level=1) for task in tasks if group in get_groups(task))
    return "\n".join(lines)


def render_nothing_todo(tasks: todotxt.Tasks, namespace: argparse.Namespace):
    """Tell the user there's nothing to do and warn about invalid arguments, if any."""
    warning = invalid_arguments(namespace, tasks)
    return "Nothing to do!" + (warning if warning else " 😴")


def render_next_action(next_actions: todotxt.Tasks, tasks: todotxt.Tasks, namespace: argparse.Namespace) -> str:
    """Render the next action(s) or, if there are none, tell the user there's nothing to do."""
    if next_actions:
        render = render_grouped_tasks if namespace.groupby else render_tasks
        return render(next_actions, namespace)
    return render_nothing_todo(tasks, namespace)


def render_arguments(argument_type: str, tasks: todotxt.Tasks) -> str:
    """Return the argument for tab completion."""
    argument_type = argument_type.replace("_", "-")  # Undo escaping
    argument_values: Iterable[str]
    if argument_type in ("--groupby", "-g"):
        argument_values = arguments.parser.GROUPBY_CHOICES
    elif argument_type in ("--reference", "-r"):
        argument_values = arguments.parser.REFERENCE_CHOICES
    elif argument_type in ("--style", "-s"):
        argument_values = get_all_styles()
    elif argument_type in ("--priority", "-p"):
        argument_values = tasks.priorities()
    elif argument_type in ("@", "-@"):
        argument_values = (f"{argument_type}{context}" for context in tasks.contexts())
    elif argument_type in ("+", "-+"):
        argument_values = (f"{argument_type}{project}" for project in tasks.projects())
    else:
        argument_values = arguments.parser.ARGUMENTS
    return " ".join(sorted(argument_values))
