""" Parser for the command line arguments. """

import argparse
import datetime
import shutil
import string
import sys
import textwrap
from typing import List

import dateparser
from pygments.styles import get_all_styles

import next_action
from .config import read_config_file, write_config_file, validate_config_file


class NextActionArgumentParser(argparse.ArgumentParser):
    """ Command-line argument parser for Next-action. """

    def __init__(self) -> None:
        super().__init__(
            description="Show the next action in your todo.txt. The next action is selected from the tasks in the "
                        "todo.txt file based on task properties such as priority, due date, and creation date. Limit "
                        "the tasks from which the next action is selected by specifying contexts the tasks must have "
                        "and/or projects the tasks must belong to.",
            usage=textwrap.fill("next-action [-h] [--version] [-c [<config.cfg>]] [-f <todo.txt>] "
                                "[-n <number> | -a] [-d [<due date>] | -o] [-p [<priority>]] [-s [<style>]] "
                                "[<context|project> ...]",
                                width=shutil.get_terminal_size().columns - len("usage: ")))
        self.__default_filenames = ["~/todo.txt"]
        self.add_optional_arguments()
        self.add_positional_arguments()

    def add_optional_arguments(self) -> None:
        """ Add the optional arguments to the parser. """
        self.add_argument(
            "--version", action="version", version="%(prog)s {0}".format(next_action.__version__))
        config_file = self.add_mutually_exclusive_group()
        config_file.add_argument(
            "--write-config-file", help="generate a sample configuration file and exit", action="store_true")
        config_file.add_argument(
            "-c", "--config-file", metavar="<config.cfg>", type=str, default="~/.next-action.cfg", nargs="?",
            help="filename of configuration file to read (default: %(default)s); omit filename to not read any "
                 "configuration file")
        self.add_argument(
            "-f", "--file", action="append", metavar="<todo.txt>", default=self.__default_filenames[:], type=str,
            help="filename of todo.txt file to read; can be '-' to read from standard input; argument can be "
                 "repeated to read tasks from multiple todo.txt files (default: ~/todo.txt)")
        number = self.add_mutually_exclusive_group()
        number.add_argument(
            "-n", "--number", metavar="<number>", type=int, default=1,
            help="number of next actions to show (default: %(default)s)")
        number.add_argument(
            "-a", "--all", help="show all next actions", action="store_const", dest="number", const=sys.maxsize)
        date = self.add_mutually_exclusive_group()
        date.add_argument(
            "-d", "--due", metavar="<due date>", type=date_type, nargs="?", const=datetime.date.max,
            help="show only next actions with a due date; if a date is given, show only next actions due on or "
                 "before that date")
        date.add_argument("-o", "--overdue", help="show only overdue next actions", action="store_true")
        self.add_argument(
            "-p", "--priority", metavar="<priority>", choices=string.ascii_uppercase, nargs="?",
            help="minimum priority (A-Z) of next actions to show (default: %(default)s)")
        styles = sorted(list(get_all_styles()))
        self.add_argument(
            "-s", "--style", metavar="<style>", choices=styles, default=None, nargs="?",
            help="colorize the output; available styles: {0} (default: %(default)s)".format(", ".join(styles)))

    def add_positional_arguments(self) -> None:
        """ Add the positional arguments to the parser. """
        filters = self.add_argument_group("optional context and project arguments; these can be repeated")
        # Collect all context and project arguments in one list:
        filters.add_argument(
            "filters", metavar="<context|project>", help=argparse.SUPPRESS, nargs="*", type=filter_type)
        # Add two dummy arguments for the help info:
        filters.add_argument(
            "dummy", metavar="@<context>", help="context the next action must have", nargs="*",
            default=argparse.SUPPRESS)
        filters.add_argument(
            "dummy", metavar="+<project>", help="project the next action must be part of", nargs="*",
            default=argparse.SUPPRESS)
        # These arguments won't be collected because they start with a -. They'll be parsed by parse_remaining_args
        # below
        filters.add_argument(
            "dummy", metavar="-@<context>", help="context the next action must not have", nargs="*",
            default=argparse.SUPPRESS)
        filters.add_argument(
            "dummy", metavar="-+<project>", help="project the next action must not be part of", nargs="*",
            default=argparse.SUPPRESS)

    def parse_args(self, args=None, namespace=None) -> argparse.Namespace:
        """ Parse the command-line arguments. """
        namespace, remaining = self.parse_known_args(args, namespace)
        self.parse_remaining_args(remaining, namespace)
        if getattr(namespace, "config_file", self.get_default("config_file")) is not None:
            self.process_config_file(namespace)
        if namespace.write_config_file:
            write_config_file()
            self.exit()
        self.fix_filenames(namespace)
        return namespace

    def parse_remaining_args(self, remaining: List[str], namespace: argparse.Namespace) -> None:
        """ Parse the remaining command line arguments. """
        for value in remaining:
            if value.startswith("-@") or value.startswith("-+"):
                argument_type = "context" if value.startswith("-@") else "project"
                if len(value) == 2:
                    self.error("argument <context|project>: {0} name missing".format(argument_type))
                elif value[1:] in namespace.filters:
                    self.error("{0} {1} is both included and excluded".format(argument_type, value[2:]))
                else:
                    namespace.filters.append(value)
            else:
                self.error("unrecognized arguments: {0}".format(value))

    def process_config_file(self, namespace: argparse.Namespace) -> None:
        """ Process the configuration file. """
        config_filename = namespace.config_file
        config = read_config_file(config_filename, self.get_default("config_file"), self.error)
        if not config:
            return
        validate_config_file(config, config_filename, self.error)
        if self.arguments_not_specified("-f", "--file"):
            filenames = config.get("file", [])
            if isinstance(filenames, str):
                filenames = [filenames]
            getattr(namespace, "file").extend(filenames)
        if self.arguments_not_specified("-n", "--number", "-a", "--all"):
            number = sys.maxsize if config.get("all", False) else config.get("number", 1)
            setattr(namespace, "number", number)
        if self.arguments_not_specified("-s", "--style"):
            style = config.get("style", self.get_default("style"))
            setattr(namespace, "style", style)
        if self.arguments_not_specified("-p", "--priority"):
            priority = config.get("priority", self.get_default("priority"))
            setattr(namespace, "priority", priority)

    @staticmethod
    def arguments_not_specified(*arguments: str) -> bool:
        """ Return whether any of the arguments was specified on the command line. """
        return all([argument not in sys.argv for argument in arguments])

    def fix_filenames(self, namespace: argparse.Namespace) -> None:
        """ Fix the filenames. """
        # Work around the issue that the "append" action doesn't overwrite defaults.
        # See https://bugs.python.org/issue16399.
        filenames = namespace.file[:]
        default_filenames = self.__default_filenames
        if default_filenames != filenames:
            for default_filename in default_filenames:
                filenames.remove(default_filename)
        # Remove duplicate filenames while maintaining order.
        namespace.file = list(dict.fromkeys(filenames))


def filter_type(value: str) -> str:
    """ Return the filter if it's valid, else raise an error. """
    if value.startswith("@") or value.startswith("+"):
        if len(value) > 1:
            return value
        else:
            value_type = "context" if value.startswith("@") else "project"
            raise argparse.ArgumentTypeError("{0} name missing".format(value_type))
    raise argparse.ArgumentTypeError("unrecognized arguments: {0}".format(value))


def date_type(value: str) -> datetime.date:
    """ Return the date if it's valid, else raise an error. """
    date_time = dateparser.parse(value, languages=["en"],
                                 settings={"PREFER_DAY_OF_MONTH": "last", "PREFER_DATES_FROM": "future"})
    if date_time:
        return date_time.date()
    raise argparse.ArgumentTypeError("invalid date: {0}".format(value))
