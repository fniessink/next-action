""" Parse the command line arguments. """

import argparse
import os
import shutil
import sys
from typing import Any, List, Sequence, Union

import next_action


def is_valid_prefixed_arg(argument_type: str, argument_prefix: str, value: str,
                          parser: argparse.ArgumentParser) -> bool:
    """ Check whether the value is a (valid) prefixed argument. """
    if value.startswith(argument_prefix):
        if len(value) > len(argument_prefix):
            return True
        else:
            parser.error("{0} name cannot be empty".format(argument_type))
    return False


class ContextProjectAction(argparse.Action):  # pylint: disable=too-few-public-methods
    """ An argument parser action that checks for contexts and projects. """
    def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace,
                 values: Union[str, Sequence[Any], None], option_string: str = None) -> None:
        if values is None or isinstance(values, str):
            return  # pragma: no cover
        contexts = []
        projects = []
        for value in values:
            if is_valid_prefixed_arg("context", "@", value, parser):
                contexts.append(value.strip("@"))
            elif is_valid_prefixed_arg("project", "+", value, parser):
                projects.append(value.strip("+"))
            else:
                parser.error("unrecognized argument: {0}".format(value))
        if namespace.contexts is None:
            namespace.contexts = contexts
        if namespace.projects is None:
            namespace.projects = projects


def parse_arguments() -> argparse.Namespace:
    """ Parse the command line arguments. """
    # Ensure that the help info is printed using all columns available
    os.environ['COLUMNS'] = str(shutil.get_terminal_size().columns)

    parser = argparse.ArgumentParser(description="Show the next action in your todo.txt",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--version", action="version", version="%(prog)s {0}".format(next_action.__version__))
    default_filenames = ["todo.txt"]
    parser.add_argument("-f", "--file", help="todo.txt file to read; argument can be repeated", type=str,
                        action="append", dest="filenames", metavar="FILE", default=default_filenames)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-n", "--number", metavar="N", help="number of next actions to show", type=int, default=1)
    group.add_argument("-a", "--all", help="show all next actions", action="store_true")
    parser.add_argument("contexts", metavar="@CONTEXT", help="show the next action in the specified contexts",
                        nargs="*", type=str, default=None, action=ContextProjectAction)
    parser.add_argument("projects", metavar="+PROJECT", help="show the next action for the specified projects",
                        nargs="*", type=str, default=None, action=ContextProjectAction)
    parser.add_argument("excluded_contexts", metavar="-@CONTEXT", help="exclude actions in the specified contexts",
                        nargs="*", type=str, default=None)
    parser.add_argument("excluded_projects", metavar="-+PROJECT", help="exclude actions for the specified projects",
                        nargs="*", type=str, default=None)
    namespace, remaining = parser.parse_known_args()
    parse_remaining_args(parser, remaining, namespace)
    # Work around the issue that the "append" action doesn't overwrite defaults.
    # See https://bugs.python.org/issue16399.
    if default_filenames != namespace.filenames:
        for default_filename in default_filenames:
            namespace.filenames.remove(default_filename)
    # Remove duplicate filenames while maintaining order.
    namespace.filenames = list(dict.fromkeys(namespace.filenames))
    # If the user wants to see all next actions, set the number to something big.
    if namespace.all:
        namespace.number = sys.maxsize
    return namespace


def parse_remaining_args(parser: argparse.ArgumentParser, remaining: List[str], namespace: argparse.Namespace) -> None:
    """ Parse the remaining command line arguments. """
    excluded_contexts = []
    excluded_projects = []
    for argument in remaining:
        if is_valid_prefixed_arg("context", "-@", argument, parser):
            context = argument[len("-@"):]
            if context in namespace.contexts:
                parser.error("context {0} is both included and excluded".format(context))
            else:
                excluded_contexts.append(context)
        elif is_valid_prefixed_arg("project", "-+", argument, parser):
            project = argument[len("-+"):]
            if project in namespace.projects:
                parser.error("project {0} is both included and excluded".format(project))
            else:
                excluded_projects.append(project)
        else:
            parser.error("unrecognized arguments: {0}".format(argument))
    namespace.excluded_contexts = excluded_contexts
    namespace.excluded_projects = excluded_projects
