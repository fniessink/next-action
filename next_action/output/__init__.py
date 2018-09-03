"""Package for formatting output."""

import argparse

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


def render_nothing_todo(tasks: todotxt.Tasks, namespace: argparse.Namespace):
    """Tell the user there's nothing to do and warn about invalid arguments, if any."""
    return "Nothing to do!" + invalid_arguments(namespace, tasks)


def render_next_action(next_actions: todotxt.Tasks, tasks: todotxt.Tasks, namespace: argparse.Namespace) -> str:
    """Render the next action(s) or, if there are none, tell the user there's nothing to do."""
    return render_tasks(next_actions, namespace) if next_actions else render_nothing_todo(tasks, namespace)


def render_arguments(argument_type: str, tasks: todotxt.Tasks) -> str:
    """Return the arguments, for tab completion."""
    prefix = dict(contexts="@", projects="+", excluded_contexts="-@", excluded_projects="-+").get(argument_type, "")
    if argument_type == "reference":
        argument_values = arguments.parser.REFERENCE_CHOICES
    elif argument_type == "styles":
        argument_values = get_all_styles()
    else:
        arguments_getter = argument_type.split("_")[-1]
        argument_values = getattr(tasks, arguments_getter)()
    prefixed_argument_values = (f"{prefix}{value}" for value in argument_values)
    return " ".join(sorted(prefixed_argument_values))
