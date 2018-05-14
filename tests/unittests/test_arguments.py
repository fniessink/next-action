""" Unit tests for the argument parsing classes. """

import os
import sys
import unittest
from unittest.mock import patch, call

from next_action.arguments import parse_arguments


class ArgumentParserTest(unittest.TestCase):
    """ Unit tests for the argument parses. """

    usage_message = """usage: next-action [-h] [--version] [-f FILE] [-n N | -a]
                   [@CONTEXT [@CONTEXT ...]] [+PROJECT [+PROJECT ...]] [-@CONTEXT [-@CONTEXT ...]]
"""

    @patch.object(sys, "argv", ["next-action"])
    def test_default_filename(self):
        """ Test that the argument parser has a default filename. """
        self.assertEqual(["todo.txt"], parse_arguments().filenames)

    @patch.object(sys, "argv", ["next-action", "-f", "my_todo.txt"])
    def test_filename_argument(self):
        """ Test that the argument parser accepts a filename. """
        self.assertEqual(["my_todo.txt"], parse_arguments().filenames)

    @patch.object(sys, "argv", ["next-action", "--file", "my_other_todo.txt"])
    def test_long_filename_argument(self):
        """ Test that the argument parser accepts a filename. """
        self.assertEqual(["my_other_todo.txt"], parse_arguments().filenames)

    @patch.object(sys, "argv", ["next-action", "-f", "todo.txt"])
    def test_add_default_filename(self):
        """ Test that adding the default filename doesn't get it included twice. """
        self.assertEqual(["todo.txt"], parse_arguments().filenames)

    @patch.object(sys, "argv", ["next-action", "-f", "todo.txt", "-f", "other.txt"])
    def test_default_and_non_default(self):
        """ Test that adding the default filename and another filename gets both included. """
        self.assertEqual(["todo.txt", "other.txt"], parse_arguments().filenames)

    @patch.object(sys, "argv", ["next-action", "-f", "other.txt", "-f", "other.txt"])
    def test__add_filename_twice(self):
        """ Test that adding the same filename twice includes it only once. """
        self.assertEqual(["other.txt"], parse_arguments().filenames)

    @patch.object(sys, "argv", ["next-action"])
    def test_no_context(self):
        """ Test that the argument parser returns no contexts if the user doesn't pass one. """
        self.assertEqual([], parse_arguments().contexts)

    @patch.object(sys, "argv", ["next-action", "@home"])
    def test_one_context(self):
        """ Test that the argument parser returns the context if the user passes one. """
        self.assertEqual(["home"], parse_arguments().contexts)

    @patch.object(sys, "argv", ["next-action", "@home", "@work"])
    def test_multiple_contexts(self):
        """ Test that the argument parser returns all contexts if the user passes multiple contexts. """
        self.assertEqual(["home", "work"], parse_arguments().contexts)

    @patch.object(sys, "argv", ["next-action", "@"])
    @patch.object(sys.stderr, "write")
    def test_empty_context(self, mock_stderr_write):
        """ Test that the argument parser exits if the context is empty. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual([call(self.usage_message), call("next-action: error: context name cannot be empty\n")],
                         mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "-@home"])
    def test_exclude_context(self):
        """ Test that contexts can be excluded. """
        self.assertEqual(["home"], parse_arguments().excluded_contexts)

    @patch.object(sys, "argv", ["next-action", "@home", "-@home"])
    @patch.object(sys.stderr, "write")
    def test_include_exclude_context(self, mock_stderr_write):
        """ Test that contexts cannot be included and excluded. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual([call(self.usage_message),
                          call("next-action: error: context home is both included and excluded\n")],
                         mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "-^"])
    @patch.object(sys.stderr, "write")
    def test_invalid_extra_argument(self, mock_stderr_write):
        """ Test that the argument parser exits if the extra argument is invalid. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual([call(self.usage_message), call("next-action: error: unrecognized arguments: -^\n")],
                         mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "+DogHouse"])
    def test_one_project(self):
        """ Test that the argument parser returns the project if the user passes one. """
        self.assertEqual(["DogHouse"], parse_arguments().projects)

    @patch.object(sys, "argv", ["next-action", "+DogHouse", "+PaintHouse"])
    def test_multiple_projects(self):
        """ Test that the argument parser returns the projects if the user passes multiple projects. """
        self.assertEqual(["DogHouse", "PaintHouse"], parse_arguments().projects)

    @patch.object(sys, "argv", ["next-action", "+"])
    @patch.object(sys.stderr, "write")
    def test_empty_project(self, mock_stderr_write):
        """ Test that the argument parser exits if the project is empty. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual([call(self.usage_message), call("next-action: error: project name cannot be empty\n")],
                         mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "+DogHouse", "@home", "+PaintHouse", "@weekend"])
    def test_contexts_and_projects(self):
        """ Test that the argument parser returns the contexts and the projects, even when mixed. """
        self.assertEqual(["home", "weekend"], parse_arguments().contexts)
        self.assertEqual(["DogHouse", "PaintHouse"], parse_arguments().projects)

    @patch.object(sys, "argv", ["next-action", "home"])
    @patch.object(sys.stderr, "write")
    def test_faulty_option(self, mock_stderr_write):
        """ Test that the argument parser exits if the option is faulty. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual([call(self.usage_message), call("next-action: error: unrecognized argument: home\n")],
                         mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action"])
    def test_default_number(self):
        """ Test that the argument parser has a default number of actions to return. """
        self.assertEqual(1, parse_arguments().number)

    @patch.object(sys, "argv", ["next-action", "--number", "3"])
    def test_number(self):
        """ Test that a number of actions to be shown can be passed. """
        self.assertEqual(3, parse_arguments().number)

    @patch.object(sys, "argv", ["next-action", "--number", "not_a_number"])
    @patch.object(sys.stderr, "write")
    def test_faulty_number(self, mock_stderr_write):
        """ Test that the argument parser exits if the option is faulty. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual([call(self.usage_message),
                          call("next-action: error: argument -n/--number: invalid int value: 'not_a_number'\n")],
                         mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--all"])
    def test_all_actions(self):
        """ Test that --all option also sets the number of actions to show to a very big number. """
        self.assertTrue(parse_arguments().all)
        self.assertEqual(sys.maxsize, parse_arguments().number)

    @patch.object(sys, "argv", ["next-action", "--all", "--number", "3"])
    @patch.object(sys.stderr, "write")
    def test_all_and_number(self, mock_stderr_write):
        """ Test that the argument parser exits if the both --all and --number are used. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual([call(self.usage_message),
                          call("next-action: error: argument -n/--number: not allowed with argument -a/--all\n")],
                         mock_stderr_write.call_args_list)
