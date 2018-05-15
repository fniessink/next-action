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

    parser = argparse.ArgumentParser(
        description="Show the next action in your todo.txt. The next action is selected from the tasks in the todo.txt \
                     file based on priority, due date, creation date, and supplied filters.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        usage="%(prog)s [-h] [--version] [-f <todo.txt>] [-n <number> | -a] [<context|project> ...]")
    parser.add_argument("--version", action="version", version="%(prog)s {0}".format(next_action.__version__))
    default_filenames = ["todo.txt"]
    parser.add_argument(
        "-f", "--file", action="append", dest="filenames", metavar="<todo.txt>", default=default_filenames, type=str,
        help="todo.txt file to read; argument can be repeated to read tasks from multiple todo.txt files")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-n", "--number", metavar="<number>", help="number of next actions to show", type=int, default=1)
    group.add_argument("-a", "--all", help="show all next actions", action="store_true")
    filters = parser.add_argument_group("optional context and project arguments; these can be repeated")
    filter_kwargs = dict(nargs="*", type=str, default=None)
    filters.add_argument("contexts", metavar="@<context>", help="context the next action must have",
                         action=ContextProjectAction, **filter_kwargs)
    filters.add_argument("projects", metavar="+<project>", help="project the next action must be part of",
                         action=ContextProjectAction, **filter_kwargs)
    filters.add_argument("excluded_contexts", metavar="-@<context>", help="context the next action must not have",
                         **filter_kwargs)
    filters.add_argument("excluded_projects", metavar="-+<project>",
                         help="project the next action must not be part of", **filter_kwargs)
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
