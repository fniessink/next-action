from next_action.todotxt import Task
from next_action.pick_action import next_action_based_on_priority
from next_action.arguments import parse_arguments


def next_action() -> None:
    arguments = parse_arguments()
    filename: str = arguments.file
    try:
        todotxt_file = open(filename, "r")
    except FileNotFoundError:
        print("Can't find {0}".format(filename))
        return
    with todotxt_file:
        tasks = [Task(line.strip()) for line in todotxt_file.readlines()]
    action = next_action_based_on_priority(tasks, arguments.context)
    print(action.text if action else "Nothing to do!")
