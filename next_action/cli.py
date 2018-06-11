""" Entry point for Next-action's command-line interface. """

import os

from next_action.arguments import parse_arguments
from next_action.pick_action import next_actions
from next_action.todotxt import read_todotxt_files
from next_action.output import render


def next_action() -> None:
    """ Entry point for the command-line interface.

        Basic recipe:
        1) parse command-line arguments,
        2) read todo.txt file(s),
        3) determine the next action(s) and,
        4) display them.
    """
    parser, namespace = parse_arguments()
    filenames = [os.path.expanduser(filename) for filename in namespace.file]
    try:
        tasks = read_todotxt_files(filenames)
    except OSError as reason:
        parser.error("can't open file: {0}".format(reason))
    actions = next_actions(tasks, namespace)[:namespace.number]
    if actions:
        result = render(actions, namespace)
    else:
        result = "Nothing to do!"
    print(result)
