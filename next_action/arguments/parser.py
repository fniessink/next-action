""" Parser for the command line arguments. """

import argparse
import os
from typing import Dict, List, Optional

import yaml

import next_action


class NextActionArgumentParser(argparse.ArgumentParser):
    """ Command-line argument parser for Next-action. """

    def __init__(self, default_filenames: List[str]) -> None:
        super().__init__(
            description="Show the next action in your todo.txt. The next action is selected from the tasks in the "
                        "todo.txt file based on task properties such as priority, due date, and creation date. Limit "
                        "the tasks from which the next action is selected by specifying contexts the tasks must have "
                        "and/or projects the tasks must belong to.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            usage="next-action [-h] [--version] [-c <config.cfg>] [-f <todo.txt>] [-n <number> | -a] "
                  "[<context|project> ...]")
        self.add_optional_arguments(default_filenames)
        self.add_positional_arguments()

    def add_optional_arguments(self, default_filenames: List[str]) -> None:
        """ Add the optional arguments to the parser. """
        self.add_argument(
            "--version", action="version", version="%(prog)s {0}".format(next_action.__version__))
        self.add_argument(
            "-c", "--config-file", metavar="<config.cfg>", type=str, default="~/.next-action.cfg",
            help="filename of configuration file to read")
        self.add_argument(
            "-f", "--file", action="append", metavar="<todo.txt>", default=default_filenames[:], type=str,
            help="filename of todo.txt file to read; can be '-' to read from standard input; argument can be "
                 "repeated to read tasks from multiple todo.txt files")
        number = self.add_mutually_exclusive_group()
        number.add_argument(
            "-n", "--number", metavar="<number>", help="number of next actions to show", type=int, default=1)
        number.add_argument("-a", "--all", help="show all next actions", action="store_true")

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
        config_filename = self.parse_config_file()
        config = self.read_config_file(config_filename)
        namespace, remaining = self.parse_known_args(args, namespace)
        self.parse_remaining_args(remaining, namespace)
        if namespace.file == self.get_default("file"):
            filenames = config.get("file", []) if isinstance(config, dict) else []
            if isinstance(filenames, str):
                filenames = [filenames]
            if not isinstance(filenames, list):
                self.error("invalid filenames in '{0}': {1}".format(config_filename, filenames))
            for filename in filenames:
                if not isinstance(filename, str):
                    self.error("invalid filenames in '{0}': {1}".format(config_filename, filename))
            getattr(namespace, "file").extend(filenames)
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

    def parse_config_file(self) -> Optional[str]:
        """ Parse the config file argument from the command line arguments. """
        parser = argparse.ArgumentParser(add_help=False, usage=self.usage)
        parser.add_argument("-c", "--config-file", dest="config_file", default=self.get_default("config_file"),
                            type=str)
        namespace, _ = parser.parse_known_args()
        return namespace.config_file

    def read_config_file(self, filename: str) -> Dict[str, List[str]]:
        """ Read and parse the configuration file. """
        try:
            with open(os.path.expanduser(filename), "r") as config_file:
                return yaml.safe_load(config_file.read())
        except FileNotFoundError as reason:
            if filename == self.get_default("config_file"):
                return dict()  # Don't complain if there's no configuration file at the default location
            else:
                self.error("can't open configuration file: {0}".format(reason))
        except OSError as reason:
            self.error("can't open configuration file: {0}".format(reason))
        except yaml.YAMLError as reason:
            self.error("can't parse configuration file '{0}': {1}".format(filename, reason))


def filter_type(value: str) -> str:
    """ Return the filter if it's valid, else raise an error. """
    if value.startswith("@") or value.startswith("+"):
        if len(value) > 1:
            return value
        else:
            value_type = "context" if value.startswith("@") else "project"
            raise argparse.ArgumentTypeError("{0} name missing".format(value_type))
    raise argparse.ArgumentTypeError("unrecognized arguments: {0}".format(value))
