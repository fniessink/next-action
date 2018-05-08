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
