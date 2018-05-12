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
        if values is None or isinstance(values, str):
            return  # pragma: no cover
        contexts = []
        projects = []
        for value in values:
            if self.__is_valid("Context", "@", value, parser):
                contexts.append(value.strip("@"))
            elif self.__is_valid("Project", "+", value, parser):
                projects.append(value.strip("+"))
            else:
                parser.error("Unrecognized argument '{0}'.".format(value))
        if namespace.contexts is None:
            namespace.contexts = contexts
        if namespace.projects is None:
            namespace.projects = projects

    @staticmethod
    def __is_valid(argument_type: str, argument_prefix: str, value: str, parser: argparse.ArgumentParser) -> bool:
        """ Check whether the value is a (valid) prefixed argument. """
        if value.startswith(argument_prefix):
            if len(value) > 1:
                return True
            else:
                parser.error("{0} name cannot be empty.".format(argument_type.capitalize()))
        return False


def parse_arguments() -> argparse.Namespace:
    """ Parse the command line arguments. """
    # Ensure that the help info is printed using all columns available
    os.environ['COLUMNS'] = str(shutil.get_terminal_size().columns)

    parser = argparse.ArgumentParser(description="Show the next action in your todo.txt",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--version", action="version", version="%(prog)s {0}".format(next_action.__version__))
    parser.add_argument("-f", "--file", help="filename of the todo.txt file to read",
                        type=str, default="todo.txt")
    parser.add_argument("contexts", metavar="@CONTEXT", help="show the next action in the specified contexts",
                        nargs="*", type=str, default=None, action=ContextProjectAction)
    parser.add_argument("projects", metavar="+PROJECT", help="show the next action for the specified projects",
                        nargs="*", type=str, default=None, action=ContextProjectAction)
    return parser.parse_args()
