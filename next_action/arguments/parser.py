""" Parser for the command line arguments. """

import argparse
from typing import List

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
    filters.add_argument("filters", metavar="<context|project>", help=argparse.SUPPRESS, nargs="*", type=filter_type)
    # These are here for the help info only:
    filters.add_argument("filters", metavar="@<context>", help="context the next action must have",
                         nargs="*", type=filter_type, default=argparse.SUPPRESS)
    filters.add_argument("filters", metavar="+<project>", help="project the next action must be part of",
                         nargs="*", type=filter_type, default=argparse.SUPPRESS)
    filters.add_argument("filters", metavar="-@<context>", help="context the next action must not have",
                         nargs="*", type=filter_type, default=argparse.SUPPRESS)
    filters.add_argument("filters", metavar="-+<project>", help="project the next action must not be part of",
                         nargs="*", type=filter_type, default=argparse.SUPPRESS)
    return parser


def parse_remaining_args(parser: argparse.ArgumentParser, remaining: List[str], namespace: argparse.Namespace) -> None:
    """ Parse the remaining command line arguments. """
    for argument in remaining:
        if is_valid_prefixed_arg("context", "-@", argument, parser):
            if argument[1:] in getattr(namespace, "filters", []):
                parser.error("context {0} is both included and excluded".format(argument[len("-@"):]))
            else:
                namespace.filters.append(argument)
        elif is_valid_prefixed_arg("project", "-+", argument, parser):
            if argument[1:] in getattr(namespace, "filters", []):
                parser.error("project {0} is both included and excluded".format(argument[len("-@"):]))
            else:
                namespace.filters.append(argument)
        else:
            parser.error("unrecognized arguments: {0}".format(argument))


def is_valid_prefixed_arg(argument_type: str, argument_prefix: str, value: str,
                          parser: argparse.ArgumentParser) -> bool:
    """ Check whether the value is a (valid) prefixed argument. """
    if value.startswith(argument_prefix):
        if len(value) > len(argument_prefix):
            return True
        else:
            parser.error("argument <context|project>: {0} name missing".format(argument_type))
    return False


def filter_type(value: str) -> str:
    """ Return the filter if it's valid, else raise an error. """
    prefixes = ("@", "+", "-@", "-+")
    name = {"@": "context", "-@": "context", "+": "project", "-+": "project"}
    for prefix in prefixes:
        if value.startswith(prefix):
            if len(value) > len(prefix):
                return value
            else:
                raise argparse.ArgumentTypeError("{0} name missing".format(name[prefix]))
    raise argparse.ArgumentTypeError("unrecognized arguments: {0}".format(value))
