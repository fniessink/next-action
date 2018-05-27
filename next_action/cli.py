""" Entry point for Next-action's command-line interface. """

import fileinput
import os

from next_action.arguments import parse_arguments
from next_action.pick_action import next_actions
from next_action.todotxt import read_todotxt_file
from next_action.output import colorize


def next_action() -> None:
    """ Entry point for the command-line interface.

        Basic recipe:
        1) parse command-line arguments,
        2) read todo.txt file(s),
        3) determine the next action(s) and,
        4) display them.
    """
    parser, namespace = parse_arguments()
    try:
        with fileinput.input([os.path.expanduser(filename) for filename in namespace.file]) as todotxt_file:
            tasks = read_todotxt_file(todotxt_file)
    except OSError as reason:
        parser.error("can't open file: {0}".format(reason))
    actions = next_actions(tasks, namespace)
    if actions:
        result = colorize("\n".join(action.text for action in actions[:namespace.number]), namespace.style or "")
    else:
        result = "Nothing to do!"
    print(result)
