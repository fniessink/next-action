""" Unit tests for the command-line interface entry point. """

import os
import sys
import unittest
from unittest.mock import patch, mock_open, call

from next_action.cli import next_action
from next_action import __version__


class CLITest(unittest.TestCase):
    """ Unit tests for the command-line interface. """

    @patch.object(sys, "argv", ["next-action"])
    @patch("next_action.cli.open", mock_open(read_data=""))
    @patch.object(sys.stdout, "write")
    def test_empty_task_file(self, mock_stdout_write):
        """ Test the response when the task file is empty. """
        next_action()
        self.assertEqual([call("Nothing to do!"), call("\n")], mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next-action"])
    @patch("next_action.cli.open", mock_open(read_data="Todo\n"))
    @patch.object(sys.stdout, "write")
    def test_one_task(self, mock_stdout_write):
        """ Test the response when the task file has one task. """
        next_action()
        self.assertEqual([call("Todo"), call("\n")], mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "@work"])
    @patch("next_action.cli.open", mock_open(read_data="Todo @home\nTodo @work\n"))
    @patch.object(sys.stdout, "write")
    def test_context(self, mock_stdout_write):
        """ Test the response when the user passes a context. """
        next_action()
        self.assertEqual([call("Todo @work"), call("\n")], mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "+DogHouse"])
    @patch("next_action.cli.open", mock_open(read_data="Walk the dog @home\nBuy wood +DogHouse\n"))
    @patch.object(sys.stdout, "write")
    def test_project(self, mock_stdout_write):
        """ Test the response when the user passes a project. """
        next_action()
        self.assertEqual([call("Buy wood +DogHouse"), call("\n")], mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next-action"])
    @patch("next_action.cli.open")
    @patch.object(sys.stdout, "write")
    def test_missing_file(self, mock_stdout_write, mock_file_open):
        """ Test the response when the task file can't be found. """
        mock_file_open.side_effect = FileNotFoundError
        next_action()
        self.assertEqual([call("Can't find todo.txt"), call("\n")], mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--help"])
    @patch.object(sys.stdout, "write")
    def test_help(self, mock_stdout_write):
        """ Test the help message. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, next_action)
        self.assertEqual(call("""usage: next-action [-h] [--version] [-f FILE] [@CONTEXT] [+PROJECT]

Show the next action in your todo.txt

positional arguments:
  @CONTEXT              show the next action in the specified context (default: None)
  +PROJECT              show the next action for the specified project (default: None)

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -f FILE, --file FILE  filename of the todo.txt file to read (default: todo.txt)
"""),
                         mock_stdout_write.call_args_list[0])

    @patch.object(sys, "argv", ["next-action", "--version"])
    @patch.object(sys.stdout, "write")
    def test_version(self, mock_stdout_write):
        """ Test that --version shows the version number. """
        self.assertRaises(SystemExit, next_action)
        self.assertEqual([call("next-action {0}\n".format(__version__))], mock_stdout_write.call_args_list)
