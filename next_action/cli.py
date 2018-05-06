import argparse

from next_action.todotxt import Task
from next_action.pick_action import next_action_based_on_priority


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Show the next action in your todo.txt")
    parser.add_argument("-f", "--file", help="Filename of the todo.txt file to read",
                        default="todo.txt")
    return parser.parse_args()


def next_action() -> None:
    with open(parse_arguments().file, "r") as tasks:
        tasks = [Task(line.strip()) for line in tasks.readlines()]
    next = next_action_based_on_priority(*tasks)
    if next:
        print(next.text)
    else:
        print("Nothing to do!")
