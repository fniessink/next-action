""" Entry point for Next-action's command-line interface. """

from next_action.todotxt import Task
from next_action.pick_action import next_actions
from next_action.arguments import parse_arguments


def next_action() -> None:
    """ Entry point for the command-line interface.

        Basic recipe:
        1) parse command-line arguments,
        2) read todo.txt file(s),
        3) determine the next action(s) and display them.
    """
    arguments = parse_arguments()
    tasks = []
    for filename in arguments.filenames:
        try:
            todotxt_file = open(filename, "r")
        except FileNotFoundError:
            print("Can't find {0}".format(filename))
            return
        with todotxt_file:
            tasks.extend([Task(line.strip()) for line in todotxt_file.readlines() if line.strip()])
    actions = next_actions(tasks,
                           set(arguments.contexts), set(arguments.projects),
                           set(arguments.excluded_contexts), set(arguments.excluded_projects))
    print("\n".join(action.text for action in actions[:arguments.number]) if actions else "Nothing to do!")
