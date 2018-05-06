import argparse

from next_action.todotxt import Task
from next_action.pick_action import next_action_based_on_priority


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Show the next action in your todo.txt")
    parser.add_argument("-f", "--file", help="Filename of the todo.txt file to read",
                        type=str, default="todo.txt")
    return parser.parse_args()


def next_action() -> None:
    filename: str = parse_arguments().file
    with open(filename, "r") as todotxt_file:
        tasks = [Task(line.strip()) for line in todotxt_file.readlines()]
    action = next_action_based_on_priority(tasks)
    if action:
        print(action.text)
    else:
        print("Nothing to do!")
