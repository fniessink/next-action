from next_action.todotxt import Task
from next_action.pick_action import next_action_based_on_priority
from next_action.arguments import parse_arguments


def next_action() -> None:
    filename: str = parse_arguments().file
    try:
        todotxt_file = open(filename, "r")
    except FileNotFoundError:
        print("Can't find {0}".format(filename))
        return
    with todotxt_file:
        tasks = [Task(line.strip()) for line in todotxt_file.readlines()]
    action = next_action_based_on_priority(tasks)
    print(action.text if action else "Nothing to do!")
