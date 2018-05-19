""" Parser for the command line arguments. """

import argparse
from typing import List

import next_action


def build_parser(default_filenames: List[str]) -> argparse.ArgumentParser:
    """ Create the arguments parsers. """
    parser = argparse.ArgumentParser(
        description="Show the next action in your todo.txt. The next action is selected from the tasks in the todo.txt \
                     file based on task properties such as priority, due date, and creation date. Limit the tasks from \
                     which the next action is selected by specifying contexts the tasks must have and/or projects the \
                     tasks must belong to.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        usage="%(prog)s [-h] [--version] [-f <filename>] [-n <number> | -a] [<context|project> ...]")
    add_optional_arguments(parser, default_filenames)
    add_positional_arguments(parser)
    return parser


def add_optional_arguments(parser: argparse.ArgumentParser, default_filenames: List[str]) -> None:
    """ Add the optional arguments to the parser. """
    parser.add_argument(
        "--version", action="version", version="%(prog)s {0}".format(next_action.__version__))
    parser.add_argument(
        "-f", "--file", action="append", dest="filenames", metavar="<filename>", default=default_filenames, type=str,
        help="filename of todo.txt file to read; can be - to read from standard input; argument can be repeated to "
             "read tasks from multiple todo.txt files")
    number = parser.add_mutually_exclusive_group()
    number.add_argument(
        "-n", "--number", metavar="<number>", help="number of next actions to show", type=int, default=1)
    number.add_argument("-a", "--all", help="show all next actions", action="store_true")


def add_positional_arguments(parser: argparse.ArgumentParser) -> None:
    """ Add the positional arguments to the parser. """
    filters = parser.add_argument_group("optional context and project arguments; these can be repeated")
    # Collect all context and project arguments in one list:
    filters.add_argument("filters", metavar="<context|project>", help=argparse.SUPPRESS, nargs="*", type=filter_type)
    # Add two dummy arguments for the help info:
    filters.add_argument("dummy", metavar="@<context>", help="context the next action must have",
                         nargs="*", default=argparse.SUPPRESS)
    filters.add_argument("dummy", metavar="+<project>", help="project the next action must be part of",
                         nargs="*", default=argparse.SUPPRESS)
    # These arguments won't be collected because they start with a -. They'll be parsed by parse_remaining_args below
    filters.add_argument("dummy", metavar="-@<context>", help="context the next action must not have",
                         nargs="*", default=argparse.SUPPRESS)
    filters.add_argument("dummy", metavar="-+<project>", help="project the next action must not be part of",
                         nargs="*", default=argparse.SUPPRESS)


def parse_remaining_args(parser: argparse.ArgumentParser, remaining: List[str], namespace: argparse.Namespace) -> None:
    """ Parse the remaining command line arguments. """
    for value in remaining:
        if value.startswith("-@") or value.startswith("-+"):
            argument_type = "context" if value.startswith("-@") else "project"
            if len(value) == 2:
                parser.error("argument <context|project>: {0} name missing".format(argument_type))
            elif value[1:] in namespace.filters:
                parser.error("{0} {1} is both included and excluded".format(argument_type, value[2:]))
            else:
                namespace.filters.append(value)
        else:
            parser.error("unrecognized arguments: {0}".format(value))


def filter_type(value: str) -> str:
    """ Return the filter if it's valid, else raise an error. """
    if value.startswith("@") or value.startswith("+"):
        if len(value) > 1:
            return value
        else:
            value_type = "context" if value.startswith("@") else "project"
            raise argparse.ArgumentTypeError("{0} name missing".format(value_type))
    raise argparse.ArgumentTypeError("unrecognized arguments: {0}".format(value))
