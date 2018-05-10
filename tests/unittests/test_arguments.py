import os
import sys
import unittest
from unittest.mock import patch, call

from next_action.arguments import parse_arguments


class ArgumentParserTest(unittest.TestCase):
    """ Unit tests for the argument parses. """

    @patch.object(sys, "argv", ["next_action"])
    def test_default_filename(self):
        """ Test that the argument parser has a default filename. """
        self.assertEqual("todo.txt", parse_arguments().file)

    @patch.object(sys, "argv", ["next_action", "-f", "my_todo.txt"])
    def test_filename_argument(self):
        """ Test that the argument parser accepts a filename. """
        self.assertEqual("my_todo.txt", parse_arguments().file)

    @patch.object(sys, "argv", ["next_action", "--file", "my_other_todo.txt"])
    def test_long_filename_argument(self):
        """ Test that the argument parser accepts a filename. """
        self.assertEqual("my_other_todo.txt", parse_arguments().file)

    @patch.object(sys, "argv", ["next_action"])
    def test_no_context(self):
        """ Test that the argument parser returns no context if the user doesn't pass one. """
        self.assertEqual(None, parse_arguments().context)

    @patch.object(sys, "argv", ["next_action", "@home"])
    def test_one_context(self):
        """ Test that the argument parser returns the context if the user passes one. """
        self.assertEqual("@home", parse_arguments().context)

    @patch.object(sys, "argv", ["next_action", "home"])
    @patch.object(sys.stderr, "write")
    def test_faulty_context(self, mock_stderr_write):
        """ Test that the argument parser exits if the context is faulty. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual([call("usage: next_action [-h] [--version] [-f FILE] [@CONTEXT]\n"),
                          call("next_action: error: Contexts should start with an @.\n")],
                         mock_stderr_write.call_args_list)