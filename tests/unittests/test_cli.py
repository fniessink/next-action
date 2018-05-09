import unittest
from unittest.mock import patch, mock_open, call
import sys

from next_action.cli import next_action


class CLITest(unittest.TestCase):
    """ Unit tests for the command-line interface. """

    @patch("next_action.cli.open", mock_open(read_data=""))
    @patch.object(sys.stdout, "write")
    def test_empty_task_file(self, mock_stdout_write):
        """ Test the response when the task file is empty. """
        next_action()
        self.assertEqual([call("Nothing to do!"), call("\n")], mock_stdout_write.call_args_list)

    @patch("next_action.cli.open", mock_open(read_data="Todo\n"))
    @patch.object(sys.stdout, "write")
    def test_one_task(self, mock_stdout_write):
        """ Test the response when the task file has one task. """
        next_action()
        self.assertEqual([call("Todo"), call("\n")], mock_stdout_write.call_args_list)

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
        """ Test that the help contains the default filename. """
        try:
            next_action()
        except SystemExit:
            pass
        self.assertEqual(call("""usage: next_action [-h] [-f FILE]

Show the next action in your todo.txt

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Filename of the todo.txt file to read (default:
                        todo.txt)
"""),
                        mock_stdout_write.call_args_list[0])
