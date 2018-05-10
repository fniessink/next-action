import os
import sys
import unittest
from unittest.mock import patch, mock_open, call

from next_action.cli import next_action
from next_action import __version__


class CLITest(unittest.TestCase):
    """ Unit tests for the command-line interface. """

    @patch.object(sys, "argv", ["next_action"])
    @patch("next_action.cli.open", mock_open(read_data=""))
    @patch.object(sys.stdout, "write")
    def test_empty_task_file(self, mock_stdout_write):
        """ Test the response when the task file is empty. """
        next_action()
        self.assertEqual([call("Nothing to do!"), call("\n")], mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next_action"])
    @patch("next_action.cli.open", mock_open(read_data="Todo\n"))
    @patch.object(sys.stdout, "write")
    def test_one_task(self, mock_stdout_write):
        """ Test the response when the task file has one task. """
        next_action()
        self.assertEqual([call("Todo"), call("\n")], mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next_action"])
    @patch("next_action.cli.open")
    @patch.object(sys.stdout, "write")
    def test_missing_file(self, mock_stdout_write, mock_open):
        """ Test the response when the task file can't be found. """
        mock_open.side_effect = FileNotFoundError
        next_action()
        self.assertEqual([call("Can't find todo.txt"), call("\n")], mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next_action", "--help"])
    @patch.object(sys.stdout, "write")
    def test_help(self, mock_stdout_write):
        """ Test the help message. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, next_action)
        self.assertEqual(call("""usage: next_action [-h] [--version] [-f FILE] [@CONTEXT]

Show the next action in your todo.txt

positional arguments:
  @CONTEXT              Show the next action in the specified context (default: None)

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -f FILE, --file FILE  filename of the todo.txt file to read (default: todo.txt)
"""),
                        mock_stdout_write.call_args_list[0])

    @patch.object(sys, "argv", ["next_action", "--version"])
    @patch.object(sys.stdout, "write")
    def test_version(self, mock_stdout_write):
        """ Test that --version shows the version number. """
        self.assertRaises(SystemExit, next_action)
        self.assertEqual([call("Next-action {0}\n".format(__version__))], mock_stdout_write.call_args_list)