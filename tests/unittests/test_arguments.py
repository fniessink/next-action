import unittest
from unittest.mock import patch
import sys

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
