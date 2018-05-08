from next_action.todotxt import Task
from next_action.pick_action import next_action_based_on_priority
from next_action.arguments import parse_arguments


def next_action() -> None:
    filename: str = parse_arguments().file
    with open(filename, "r") as todotxt_file:
        tasks = [Task(line.strip()) for line in todotxt_file.readlines()]
    action = next_action_based_on_priority(tasks)
    if action:
        print(action.text)
    else:
        print("Nothing to do!")
