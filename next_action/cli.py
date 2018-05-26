""" Entry point for Next-action's command-line interface. """

import fileinput

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
    parser, arguments = parse_arguments()
    try:
        with fileinput.input(arguments.filenames) as todotxt_file:
            tasks = read_todotxt_file(todotxt_file)
    except OSError as reason:
        parser.error("can't open file: {0}".format(reason))
    actions = next_actions(tasks, arguments)
    if actions:
        result = colorize("\n".join(action.text for action in actions[:arguments.number]), arguments.style or "")
    else:
        result = "Nothing to do!"
    print(result.rstrip("\n"))
