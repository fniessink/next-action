import argparse

import next_action


def parse_arguments() -> argparse.Namespace:
    """ Parse the command line arguments. """
    parser = argparse.ArgumentParser(description="Show the next action in your todo.txt",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file", help="filename of the todo.txt file to read",
                        type=str, default="todo.txt")
    parser.add_argument("--version", action="version", version="Next-action {0}".format(next_action.__version__))
    return parser.parse_args()
