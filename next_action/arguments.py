""" Parse the command line arguments. """

import argparse
import os
import shutil
from typing import Any, Sequence, Union

import next_action


class ContextProjectAction(argparse.Action):  # pylint: disable=too-few-public-methods
    """ An argument parser action that checks for contexts and projects. """
    def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace,
                 values: Union[str, Sequence[Any], None], option_string: str = None) -> None:
        if not values or not isinstance(values, str):
            return
        if values.startswith("@"):
            if len(values) > 1:
                setattr(namespace, "context", values)
            else:
                parser.error("Context name cannot be empty.")
        elif values.startswith("+"):
            if len(values) > 1:
                setattr(namespace, "project", values)
            else:
                parser.error("Project name cannot be empty.")
        else:
            parser.error("Unrecognized option '{0}'.".format(values))


def parse_arguments() -> argparse.Namespace:
    """ Parse the command line arguments. """
    # Ensure that the help info is printed using all columns available
    os.environ['COLUMNS'] = str(shutil.get_terminal_size().columns)

    parser = argparse.ArgumentParser(description="Show the next action in your todo.txt",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--version", action="version", version="%(prog)s {0}".format(next_action.__version__))
    parser.add_argument("-f", "--file", help="filename of the todo.txt file to read",
                        type=str, default="todo.txt")
    parser.add_argument("context", metavar="@CONTEXT", help="show the next action in the specified context", nargs="?",
                        type=str, action=ContextProjectAction)
    parser.add_argument("project", metavar="+PROJECT", help="show the next action for the specified project", nargs="?",
                        type=str, action=ContextProjectAction)
    return parser.parse_args()
