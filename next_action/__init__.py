"""Main Next-action package."""

from .arguments import parse_arguments
from .pick_action import next_actions
from .output import render_next_action, render_arguments, open_urls
from .todotxt import read_todotxt_files


__title__ = "next-action"
__version__ = "1.12.0"


def next_action() -> None:
    """Entry point for the command-line interface.

    Basic recipe:
    1) parse command-line arguments,
    2) read todo.txt file(s),
    3) determine the next action(s),
    4) display them, and
    5) open their urls if requested by the user.
    """
    parser, namespace = parse_arguments(__version__)
    try:
        tasks = read_todotxt_files(namespace.file)
    except OSError as reason:
        parser.error(f"can't open file: {reason}")
    if namespace.list_arguments:
        print(render_arguments(namespace.list_arguments, tasks))
    else:
        actions = next_actions(tasks, namespace)
        print(render_next_action(actions, tasks, namespace))
        if namespace.open_urls:
            open_urls(actions)
