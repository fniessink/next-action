"""Parser for the command line arguments."""

import argparse
import datetime
import shutil
import string
import sys
import textwrap
from typing import cast, List, Set, Tuple

from pygments.styles import get_all_styles

from .config import read_config_file, write_config_file, validate_config_file


class NextActionArgumentParser(argparse.ArgumentParser):
    """Command-line argument parser for Next-action."""

    def __init__(self, version: str = "?") -> None:
        """Initialize the parser."""
        super().__init__(
            usage=textwrap.fill("next-action [-h] [--version] [-c [<config.cfg>] | -w] [-f <todo.txt> ...] "
                                "[-t [<date>]] [-b] [-r <ref>] [-s [<style>]] [-a | -n <number>] "
                                "[-d [<due date>] | -o] [-p [<priority>]] [--] [<context|project> ...]",
                                width=shutil.get_terminal_size().columns - len("usage: ")),
            description="Show the next action in your todo.txt. The next action is selected from the tasks in the "
                        "todo.txt file based on task properties such as priority, due date, and creation date. Limit "
                        "the tasks from which the next action is selected by specifying contexts the tasks must have "
                        "and/or projects the tasks must belong to.",
            epilog="Use -- to separate options with optional arguments from contexts and projects, in order to handle "
                   "cases where a context or project is mistaken for an argument to an option.",
            formatter_class=CapitalisedHelpFormatter)
        self.__default_filenames = ["~/todo.txt"]
        self.add_optional_arguments(version)
        self.add_configuration_options()
        self.add_input_options()
        self.add_output_options()
        self.add_number_options()
        self.add_filter_arguments()

    def add_optional_arguments(self, version: str) -> None:
        """Add the optional arguments to the parser."""
        self._optionals.title = self._optionals.title.capitalize() if self._optionals.title else None
        self.add_argument(
            "--version", action="version", version=f"%(prog)s {version}")

    def add_configuration_options(self) -> None:
        """Add the configuration options to the parser."""
        config_group = self.add_argument_group("Configuration options")
        config_group.add_argument(
            "-c", "--config-file", metavar="<config.cfg>", type=str, default="~/.next-action.cfg", nargs="?",
            help="filename of configuration file to read (default: %(default)s); omit filename to not read any "
                 "configuration file")
        config_group.add_argument(
            "-w", "--write-config-file", help="generate a sample configuration file and exit", action="store_true")

    def add_input_options(self) -> None:
        """Add the input options to the parser."""
        input_group = self.add_argument_group("Input options")
        input_group.add_argument(
            "-f", "--file", action="append", metavar="<todo.txt>", default=self.__default_filenames[:], type=str,
            help="filename of todo.txt file to read; can be '-' to read from standard input; argument can be "
                 "repeated to read tasks from multiple todo.txt files (default: ~/todo.txt)")
        input_group.add_argument(
            "-t", "--time-travel", metavar="<date>", type=date_type, nargs="?", const="tomorrow",
            help="time travel to the given date and show the next action(s) at that date (default: tomorrow)")

    def add_output_options(self) -> None:
        """Add the output/styling options to the parser."""
        output_group = self.add_argument_group("Output options")
        output_group.add_argument(
            "-b", "--blocked", help="show the tasks blocked by the next action, if any (default: %(default)s)",
            action="store_true")
        output_group.add_argument(
            "-r", "--reference", choices=["always", "never", "multiple"], default="multiple",
            help="reference next actions with the name of their todo.txt file (default: when reading multiple "
                 "todo.txt files)")
        styles = sorted(list(get_all_styles()))
        output_group.add_argument(
            "-s", "--style", metavar="<style>", choices=styles, default=None, nargs="?",
            help=f"colorize the output; available styles: {', '.join(styles)} (default: %(default)s)")

    def add_number_options(self) -> None:
        """Add the number options to the parser."""
        number_group = self.add_argument_group("Show multiple next actions")
        number = number_group.add_mutually_exclusive_group()
        number.add_argument(
            "-a", "--all", default=1, action="store_const", dest="number", const=sys.maxsize,
            help="show all next actions")
        number.add_argument(
            "-n", "--number", metavar="<number>", type=number_type, default=1,
            help="number of next actions to show (default: %(default)s)")

    def add_filter_arguments(self) -> None:
        """Add the filter arguments to the parser."""
        filters = self.add_argument_group("Limit the tasks from which the next actions are selected")
        date = filters.add_mutually_exclusive_group()
        date.add_argument(
            "-d", "--due", metavar="<due date>", type=date_type, nargs="?", const=datetime.date.max,
            help="show only next actions with a due date; if a date is given, show only next actions due on or "
                 "before that date")
        date.add_argument("-o", "--overdue", help="show only overdue next actions", action="store_true")
        filters.add_argument(
            "-p", "--priority", metavar="<priority>", choices=string.ascii_uppercase, nargs="?",
            help="minimum priority (A-Z) of next actions to show (default: %(default)s)")
        # Collect all context and project arguments in one list:
        filters.add_argument(
            "filters", metavar="<context|project>", help=argparse.SUPPRESS, nargs="*", type=filter_type)
        # Add two dummy arguments for the help info:
        filters.add_argument(
            "dummy", metavar="@<context> ...", nargs="*", default=argparse.SUPPRESS,
            help="contexts the next action must have")
        filters.add_argument(
            "dummy", metavar="+<project> ...", nargs="*", default=argparse.SUPPRESS,
            help="projects the next action must be part of; if repeated the next action must be part of at least one "
                 "of the projects")
        # These arguments won't be collected because they start with a -. They'll be parsed by parse_remaining_args
        # below
        filters.add_argument(
            "dummy", metavar="-@<context> ...", nargs="*", default=argparse.SUPPRESS,
            help="contexts the next action must not have")
        filters.add_argument(
            "dummy", metavar="-+<project> ...", nargs="*", default=argparse.SUPPRESS,
            help="projects the next action must not be part of")

    def parse_args(self, args=None, namespace=None) -> argparse.Namespace:
        """Parse the command-line arguments."""
        namespace, remaining = self.parse_known_args(self.sorted_args(args), namespace)
        self.parse_remaining_args(remaining, namespace)
        if namespace.time_travel and namespace.due:
            # Apply time travel to options that take a date argument (which currently is only --due)
            namespace.due += namespace.time_travel - datetime.date.today()
        if getattr(namespace, "config_file", self.get_default("config_file")) is not None:
            self.process_config_file(namespace)
        self.fix_filenames(namespace)
        if namespace.write_config_file:
            write_config_file(namespace)
            self.exit()
        return namespace

    @classmethod
    def sorted_args(cls, args: List[str] = None) -> List[str]:
        """Sort the arguments so excluded contexts and projects are last and can be parsed by parse_remaining_args."""
        args = args or sys.argv[1:]
        return [arg for arg in args if not cls.is_excluded_filter(arg)] + \
               [arg for arg in args if cls.is_excluded_filter(arg)]

    def parse_remaining_args(self, remaining: List[str], namespace: argparse.Namespace) -> None:
        """Parse the remaining command line arguments."""
        for value in remaining:
            if self.is_excluded_filter(value):
                argument = value[len("-"):]
                if not argument[len("@"):]:
                    argument_type = "context" if argument.startswith("@") else "project"
                    self.error(f"argument <context|project>: {argument_type} name missing")
                elif argument in namespace.filters:
                    self.error(f"{argument} is both included and excluded")
                else:
                    namespace.filters.append(value)
            else:
                self.error(f"unrecognized argument: {value}")
        namespace.contexts = subset(namespace.filters, "@")
        namespace.projects = subset(namespace.filters, "+")
        namespace.excluded_contexts = subset(namespace.filters, "-@")
        namespace.excluded_projects = subset(namespace.filters, "-+")

    def process_config_file(self, namespace: argparse.Namespace) -> None:
        """Process the configuration file."""
        config_filename = namespace.config_file
        config = read_config_file(config_filename, self.get_default("config_file"), self.error)
        if not config:
            return
        validate_config_file(config, config_filename, self.error)
        self.insert_config(config, namespace)

    def insert_config(self, config, namespace: argparse.Namespace) -> None:
        """Insert the configured parameters in the namespace, if no command line arguments are present."""
        if self.arguments_not_specified("-f", "--file"):
            filenames = config.get("file", [])
            if isinstance(filenames, str):
                filenames = [filenames]
            getattr(namespace, "file").extend(filenames)
        if self.arguments_not_specified("-n", "--number", "-a", "--all"):
            number = sys.maxsize if config.get("all", False) else config.get("number", self.get_default("number"))
            setattr(namespace, "number", number)
        if self.arguments_not_specified("-r", "--reference"):
            reference = config.get("reference", self.get_default("reference"))
            setattr(namespace, "reference", reference)
        if self.arguments_not_specified("-s", "--style"):
            style = config.get("style", self.get_default("style"))
            setattr(namespace, "style", style)
        if self.arguments_not_specified("-p", "--priority"):
            priority = config.get("priority", self.get_default("priority"))
            setattr(namespace, "priority", priority)
        if self.arguments_not_specified("-b", "--blocked"):
            blocked = config.get("blocked", self.get_default("blocked"))
            setattr(namespace, "blocked", blocked)
        self.insert_configured_filters(config, namespace)

    def insert_configured_filters(self, config, namespace: argparse.Namespace) -> None:
        """Insert the configured filters in the namespace, if no matching command line filters are present."""
        filters = config.get("filters", [])
        if isinstance(filters, str):
            import re
            filters = re.split(r"\s", filters)
        for prefix, filter_key in (("@", "contexts"), ("+", "projects"),
                                   ("-@", "excluded_contexts"), ("-+", "excluded_projects")):
            for configured_filter in subset(filters, prefix):
                if self.filter_not_specified(prefix + configured_filter):
                    getattr(namespace, filter_key).add(configured_filter)

    @staticmethod
    def arguments_not_specified(*arguments: str) -> bool:
        """Return whether any of the arguments was specified on the command line."""
        return not any([command_line_arg.startswith(argument) for argument in arguments
                        for command_line_arg in sys.argv])

    @staticmethod
    def is_excluded_filter(argument: str) -> bool:
        """Return whether the argument is an excluded context or project."""
        return argument.startswith("-@") or argument.startswith("-+")

    @staticmethod
    def filter_not_specified(filtered: str) -> bool:
        """Return whether the context or project or its opposite were specified on the command line."""
        prefix = "-"
        opposite = filtered[len(prefix):] if filtered.startswith(prefix) else prefix + filtered
        return not (filtered in sys.argv or opposite in sys.argv)

    def fix_filenames(self, namespace: argparse.Namespace) -> None:
        """Fix the filenames."""
        # Work around the issue that the "append" action doesn't overwrite defaults.
        # See https://bugs.python.org/issue16399.
        filenames = namespace.file[:]
        default_filenames = self.__default_filenames
        if default_filenames != filenames:
            for default_filename in default_filenames:
                filenames.remove(default_filename)
        # Remove duplicate filenames while maintaining order.
        namespace.file = list(dict.fromkeys(filenames))


class CapitalisedHelpFormatter(argparse.HelpFormatter):
    """Capitalise the usage string."""

    def add_usage(self, usage, actions, groups, prefix=None):
        """Insert a capitalised usage string."""
        return super().add_usage(usage, actions, groups, prefix or "Usage: ")


def filter_type(value: str) -> str:
    """Return the filter if it's valid, else raise an error."""
    if value.startswith("@") or value.startswith("+"):
        if value[len("@"):]:
            return value
        value_type = "context" if value.startswith("@") else "project"
        raise argparse.ArgumentTypeError(f"{value_type} name missing")
    raise argparse.ArgumentTypeError(f"unrecognized argument: {value}")


def date_type(value: str) -> datetime.date:
    """Return the date if it's valid, else raise an error."""
    relative_days = dict(yesterday=-1, today=0, tomorrow=1)
    if value.lower() in relative_days:
        return datetime.date.today() + datetime.timedelta(days=relative_days[value.lower()])
    from dateutil.parser import parse
    try:
        date_time, remaining_tokens = cast(Tuple, parse(value, fuzzy_with_tokens=True, ignoretz=True))
        if not remaining_tokens:
            return date_time.date()
    except ValueError:
        pass
    raise argparse.ArgumentTypeError(f"invalid date: {value}")


def number_type(value: str) -> int:
    """Return the value if it's positive, else raise an error."""
    try:
        number = int(value)
        if number > 0:
            return number
    except ValueError:
        pass
    raise argparse.ArgumentTypeError(f"invalid number: {value}")


def subset(filters: List[str], prefix: str) -> Set[str]:
    """Return a subset of the filters based on prefix."""
    return set(f.strip(prefix) for f in filters if f.startswith(prefix))
