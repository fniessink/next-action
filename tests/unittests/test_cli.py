"""Unit tests for the command-line interface entry point."""

import os
import sys
import unittest
from unittest.mock import patch, mock_open, call

from next_action import next_action, __version__
from next_action.arguments import config

from .arguments.test_parser import USAGE_MESSAGE


@patch.object(config, "open", mock_open(read_data=""))
class CLITest(unittest.TestCase):
    """Unit tests for the command-line interface."""

    @patch.object(sys, "argv", ["next-action"])
    @patch("fileinput.open", mock_open(read_data=""))
    @patch.object(sys.stdout, "write")
    def test_empty_task_file(self, mock_stdout_write):
        """Test the response when the task file is empty."""
        next_action()
        self.assertEqual([call("Nothing to do! 😴"), call("\n")], mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next-action"])
    @patch("fileinput.open", mock_open(read_data="Todo\n"))
    @patch.object(sys.stdout, "write")
    def test_one_task(self, mock_stdout_write):
        """Test the response when the task file has one task."""
        next_action()
        self.assertEqual([call("Todo"), call("\n")], mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "@work"])
    @patch("fileinput.open", mock_open(read_data="Todo @home\nTodo @work\n"))
    @patch.object(sys.stdout, "write")
    def test_context(self, mock_stdout_write):
        """Test the response when the user passes a context."""
        next_action()
        self.assertEqual([call("Todo @work"), call("\n")], mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "+DogHouse"])
    @patch("fileinput.open", mock_open(read_data="Walk the dog @home\nBuy wood +DogHouse\n"))
    @patch.object(sys.stdout, "write")
    def test_project(self, mock_stdout_write):
        """Test the response when the user passes a project."""
        next_action()
        self.assertEqual([call("Buy wood +DogHouse"), call("\n")], mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next-action"])
    @patch("fileinput.open")
    @patch.object(sys.stderr, "write")
    def test_missing_file(self, mock_stderr_write, mock_file_open):
        """Test the response when the task file can't be found."""
        mock_file_open.side_effect = OSError("some problem")
        self.assertRaises(SystemExit, next_action)
        self.assertEqual([call(USAGE_MESSAGE), call("next-action: error: can't open file: some problem\n")],
                         mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--help"])
    @patch.object(sys.stdout, "write")
    def test_help(self, mock_stdout_write):
        """Test the help message."""
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, next_action)
        self.assertEqual(call("""\
Usage: next-action [-h] [-V] [-c [<config.cfg>] | -w] [-f <todo.txt> ...] [-t [<date>]] [-b] [-r <ref>] [-s [<style>]]
[-a | -n <number>] [-d [<due date>] | -o] [-p [<priority>]] [--] [<context|project> ...]

Show the next action in your todo.txt. The next action is selected from the tasks in the todo.txt file based on task
properties such as priority, due date, and creation date. Limit the tasks from which the next action is selected by
specifying contexts the tasks must have and/or projects the tasks must belong to.

Optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit

Configuration options:
  -c [<config.cfg>], --config-file [<config.cfg>]
                        filename of configuration file to read (default: ~/.next-action.cfg); omit filename to not
                        read any configuration file
  -w, --write-config-file
                        generate a sample configuration file and exit

Input options:
  -f <todo.txt>, --file <todo.txt>
                        filename of todo.txt file to read; can be '-' to read from standard input; argument can be
                        repeated to read tasks from multiple todo.txt files (default: ~/todo.txt)
  -t [<date>], --time-travel [<date>]
                        time travel to the given date and show the next action(s) at that date (default: tomorrow)

Output options:
  -b, --blocked         show the tasks blocked by the next action, if any (default: False)
  -r {always,never,multiple}, --reference {always,never,multiple}
                        reference next actions with the name of their todo.txt file (default: when reading multiple
                        todo.txt files)
  -s [<style>], --style [<style>]
                        colorize the output; available styles: abap, algol, algol_nu, arduino, autumn, borland, bw,
                        colorful, default, emacs, friendly, fruity, igor, lovelace, manni, monokai, murphy, native,
                        paraiso-dark, paraiso-light, pastie, perldoc, rainbow_dash, rrt, tango, trac, vim, vs, xcode
                        (default: None)

Show multiple next actions:
  -a, --all             show all next actions
  -n <number>, --number <number>
                        number of next actions to show (default: 1)

Limit the tasks from which the next actions are selected:
  -d [<due date>], --due [<due date>]
                        show only next actions with a due date; if a date is given, show only next actions due on or
                        before that date
  -o, --overdue         show only overdue next actions
  -p [<priority>], --priority [<priority>]
                        minimum priority (A-Z) of next actions to show (default: None)
  @<context> ...        contexts the next action must have
  +<project> ...        projects the next action must be part of; if repeated the next action must be part of at least
                        one of the projects
  -@<context> ...       contexts the next action must not have
  -+<project> ...       projects the next action must not be part of

Use -- to separate options with optional arguments from contexts and projects, in order to handle cases where a
context or project is mistaken for an argument to an option.
"""),
                         mock_stdout_write.call_args_list[0])

    @patch.object(sys, "argv", ["next-action", "--version"])
    @patch.object(sys.stdout, "write")
    def test_version(self, mock_stdout_write):
        """Test that --version shows the version number."""
        self.assertRaises(SystemExit, next_action)
        self.assertEqual([call(f"next-action {__version__}\n")], mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--number", "2"])
    @patch("fileinput.open", mock_open(read_data="Walk the dog @home\n(A) Buy wood +DogHouse\n(B) Call mom\n"))
    @patch.object(sys.stdout, "write")
    def test_number(self, mock_stdout_write):
        """Test that the number of next actions can be specified."""
        next_action()
        self.assertEqual([call("(A) Buy wood +DogHouse\n(B) Call mom"), call("\n")], mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--number", "3"])
    @patch("fileinput.open", mock_open(read_data="\nWalk the dog @home\n   \n(B) Call mom\n"))
    @patch.object(sys.stdout, "write")
    def test_ignore_empty_lines(self, mock_stdout_write):
        """Test that empty lines in the todo.txt file are ignored."""
        next_action()
        self.assertEqual([call("(B) Call mom\nWalk the dog @home"), call("\n")], mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--all"])
    @patch("fileinput.open", mock_open(read_data="\nWalk the dog @home\nBuy beer\n(B) Call mom\n"))
    @patch.object(sys.stdout, "write")
    def test_show_all_actions(self, mock_stdout_write):
        """Test that all actions in the todo.txt file are shown."""
        next_action()
        self.assertEqual([call("(B) Call mom\nWalk the dog @home\nBuy beer"), call("\n")],
                         mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--file", "-"])
    @patch.object(sys.stdin, "readline")
    @patch.object(sys.stdout, "write")
    def test_reading_stdin(self, mock_stdout_write, mock_stdin_readline):
        """Test that tasks can be read from stdin works."""
        mock_stdin_readline.side_effect = ["(B) Call mom\n", "Walk the dog\n", StopIteration]
        next_action()
        self.assertEqual([call("(B) Call mom"), call("\n")], mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--all", "--file", "todo.txt", "--file", "other.txt"])
    @patch("fileinput.open", mock_open(read_data="Call mom\n"))
    @patch.object(sys.stdout, "write")
    def test_reading_two_files(self, mock_stdout_write):
        """Test that tasks can be read from stdin works."""
        next_action()
        self.assertEqual([call("Call mom [todo.txt]\nCall mom [other.txt]"), call("\n")],
                         mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--reference", "always"])
    @patch("fileinput.open", mock_open(read_data="\nWalk the dog @home\nBuy beer\n(B) Call mom\n"))
    @patch.object(sys.stdout, "write")
    def test_reference_filename(self, mock_stdout_write):
        """Test that the printed next actions reference their filename."""
        expected_filename = os.path.expanduser("~/todo.txt")
        next_action()
        self.assertEqual([call(f"(B) Call mom [{expected_filename}]"),
                          call("\n")], mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "@home"])
    @patch("fileinput.open", mock_open(read_data="\nWalk the dog @park\n(B) Call mom\n"))
    @patch.object(sys.stdout, "write")
    def test_unknown_context(self, mock_stdout_write):
        """Test the response when the context is unknown."""
        next_action()
        self.assertEqual([call("Nothing to do! (warning: unknown context: home)"), call("\n")],
                         mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "+SpringCleaning", "+AutumnCleaning"])
    @patch("fileinput.open", mock_open(read_data="\nWalk the dog @park\n(B) Call mom\n"))
    @patch.object(sys.stdout, "write")
    def test_unknown_project(self, mock_stdout_write):
        """Test the response when the project is unknown."""
        next_action()
        self.assertEqual(
            [call("Nothing to do! (warning: unknown projects: AutumnCleaning, SpringCleaning)"), call("\n")],
            mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--list-arguments", "@"])
    @patch("fileinput.open", mock_open(read_data="\nWalk the dog @park\nWrite proposal +NewProject\n"))
    @patch.object(sys.stdout, "write")
    def test_list_contexts(self, mock_stdout_write):
        """Test that the contexts are listed."""
        next_action()
        self.assertEqual(
            [call("@park"), call("\n")], mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--list-arguments", "+"])
    @patch("fileinput.open", mock_open(read_data="\nWalk the dog @park\nWrite proposal +NewProject\n"))
    @patch.object(sys.stdout, "write")
    def test_list_projects(self, mock_stdout_write):
        """Test that the projects are listed."""
        next_action()
        self.assertEqual(
            [call("+NewProject"), call("\n")], mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--list-arguments", "_@"])
    @patch("fileinput.open", mock_open(read_data="\nWalk the dog @park\nWrite proposal +NewProject\n"))
    @patch.object(sys.stdout, "write")
    def test_list_excluded_contexts(self, mock_stdout_write):
        """Test that the excluded contexts are listed."""
        next_action()
        self.assertEqual(
            [call("-@park"), call("\n")], mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--list-arguments", "_+"])
    @patch("fileinput.open", mock_open(read_data="\nWalk the dog @park\nWrite proposal +NewProject\n"))
    @patch.object(sys.stdout, "write")
    def test_list_excluded_projects(self, mock_stdout_write):
        """Test that the excluded projects are listed."""
        next_action()
        self.assertEqual(
            [call("-+NewProject"), call("\n")], mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--list-arguments", "__priority"])
    @patch("fileinput.open", mock_open(read_data="\nWalk the dog @park\n(A) Write proposal\n(C) Get permit"))
    @patch.object(sys.stdout, "write")
    def test_list_priorities(self, mock_stdout_write):
        """Test that the priorities are listed."""
        next_action()
        self.assertEqual(
            [call("A C"), call("\n")], mock_stdout_write.call_args_list)
