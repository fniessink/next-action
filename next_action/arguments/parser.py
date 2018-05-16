""" Parser for the command line arguments. """

import argparse
from typing import Any, List, Sequence, Tuple, Union

import next_action


def build_parser(default_filenames: List[str]) -> argparse.ArgumentParser:
    """ Create the arguments parsers. """
    parser = argparse.ArgumentParser(
        description="Show the next action in your todo.txt. The next action is selected from the tasks in the todo.txt \
                     file based on priority, due date, creation date, and supplied filters.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        usage="%(prog)s [-h] [--version] [-f <todo.txt>] [-n <number> | -a] [<context|project> ...]")
    parser.add_argument("--version", action="version", version="%(prog)s {0}".format(next_action.__version__))
    parser.add_argument(
        "-f", "--file", action="append", dest="filenames", metavar="<todo.txt>", default=default_filenames, type=str,
        help="todo.txt file to read; argument can be repeated to read tasks from multiple todo.txt files")
    number = parser.add_mutually_exclusive_group()
    number.add_argument("-n", "--number", metavar="<number>", help="number of next actions to show", type=int,
                        default=1)
    number.add_argument("-a", "--all", help="show all next actions", action="store_true")
    filters = parser.add_argument_group("optional context and project arguments; these can be repeated")
    filters.add_argument("contexts", metavar="@<context>", help="context the next action must have",
                         action=ContextProjectAction, nargs="*", type=str, default=argparse.SUPPRESS)
    filters.add_argument("projects", metavar="+<project>", help="project the next action must be part of",
                         action=ContextProjectAction, nargs="*", type=str, default=argparse.SUPPRESS)
    filters.add_argument("excluded_contexts", metavar="-@<context>", help="context the next action must not have",
                         nargs="*", type=str, default=argparse.SUPPRESS)
    filters.add_argument("excluded_projects", metavar="-+<project>", help="project the next action must not be part of",
                         nargs="*", type=str, default=argparse.SUPPRESS)
    return parser


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
        if not hasattr(namespace, "contexts"):
            namespace.contexts = contexts
        if not hasattr(namespace, "projects"):
            namespace.projects = projects


def parse_remaining_args(parser: argparse.ArgumentParser, remaining: List[str],
                         contexts: List[str], projects: List[str]) -> Tuple[List[str], List[str]]:
    """ Parse the remaining command line arguments. """
    excluded_contexts, excluded_projects = [], []
    for argument in remaining:
        if is_valid_prefixed_arg("context", "-@", argument, parser):
            context = argument[len("-@"):]
            if context in contexts:
                parser.error("context {0} is both included and excluded".format(context))
            else:
                excluded_contexts.append(context)
        elif is_valid_prefixed_arg("project", "-+", argument, parser):
            project = argument[len("-+"):]
            if project in projects:
                parser.error("project {0} is both included and excluded".format(project))
            else:
                excluded_projects.append(project)
        else:
            parser.error("unrecognized arguments: {0}".format(argument))
    return excluded_contexts, excluded_projects


def is_valid_prefixed_arg(argument_type: str, argument_prefix: str, value: str,
                          parser: argparse.ArgumentParser) -> bool:
    """ Check whether the value is a (valid) prefixed argument. """
    if value.startswith(argument_prefix):
        if len(value) > len(argument_prefix):
            return True
        else:
            parser.error("{0} name cannot be empty".format(argument_type))
    return False
