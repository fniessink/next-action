""" Unit tests for the argument parsing classes. """

import os
import sys
import unittest
from unittest.mock import patch, call

from next_action.arguments import parse_arguments


USAGE_MESSAGE = "usage: next-action [-h] [--version] [-f <filename>] [-n <number> | -a] [<context|project> ...]\n"


class NoArgumentTest(unittest.TestCase):
    """ Unit tests for the argument parser, without arguments. """

    @patch.object(sys, "argv", ["next-action"])
    def test_filters(self):
        """ Test that the argument parser returns no filters if the user doesn't pass one. """
        self.assertEqual([set(), set(), set(), set()], parse_arguments().filters)

    @patch.object(sys, "argv", ["next-action"])
    def test_filename(self):
        """ Test that the argument parser returns the default filename if the user doesn't pass one. """
        self.assertEqual([os.path.expanduser("~/todo.txt")], parse_arguments().filenames)


class FilenameTest(unittest.TestCase):
    """ Unit tests for the --filename argument. """

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


class FilterArgumentTest(unittest.TestCase):
    """ Unit tests for the @object and +project filter arguments. """

    @patch.object(sys, "argv", ["next-action", "@home"])
    def test_one_context(self):
        """ Test that the argument parser returns the context if the user passes one. """
        self.assertEqual({"home"}, parse_arguments().filters[0])

    @patch.object(sys, "argv", ["next-action", "@home", "@work"])
    def test_multiple_contexts(self):
        """ Test that the argument parser returns all contexts if the user passes multiple contexts. """
        self.assertEqual({"home", "work"}, parse_arguments().filters[0])

    @patch.object(sys, "argv", ["next-action", "@"])
    @patch.object(sys.stderr, "write")
    def test_empty_context(self, mock_stderr_write):
        """ Test that the argument parser exits if the context is empty. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual([call(USAGE_MESSAGE),
                          call("next-action: error: argument <context|project>: context name missing\n")],
                         mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "-@home"])
    def test_exclude_context(self):
        """ Test that contexts can be excluded. """
        self.assertEqual({"home"}, parse_arguments().filters[2])

    @patch.object(sys, "argv", ["next-action", "@home", "-@home"])
    @patch.object(sys.stderr, "write")
    def test_include_exclude_context(self, mock_stderr_write):
        """ Test that contexts cannot be included and excluded. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual([call(USAGE_MESSAGE),
                          call("next-action: error: context home is both included and excluded\n")],
                         mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "-^"])
    @patch.object(sys.stderr, "write")
    def test_invalid_extra_argument(self, mock_stderr_write):
        """ Test that the argument parser exits if the extra argument is invalid. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual([call(USAGE_MESSAGE), call("next-action: error: unrecognized arguments: -^\n")],
                         mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "+DogHouse"])
    def test_one_project(self):
        """ Test that the argument parser returns the project if the user passes one. """
        self.assertEqual({"DogHouse"}, parse_arguments().filters[1])

    @patch.object(sys, "argv", ["next-action", "+DogHouse", "+PaintHouse"])
    def test_multiple_projects(self):
        """ Test that the argument parser returns the projects if the user passes multiple projects. """
        self.assertEqual({"DogHouse", "PaintHouse"}, parse_arguments().filters[1])

    @patch.object(sys, "argv", ["next-action", "+"])
    @patch.object(sys.stderr, "write")
    def test_empty_project(self, mock_stderr_write):
        """ Test that the argument parser exits if the project is empty. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual([call(USAGE_MESSAGE),
                          call("next-action: error: argument <context|project>: project name missing\n")],
                         mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "-+DogHouse"])
    def test_exclude_project(self):
        """ Test that projects can be excluded. """
        self.assertEqual({"DogHouse"}, parse_arguments().filters[3])

    @patch.object(sys, "argv", ["next-action", "+DogHouse", "-+DogHouse"])
    @patch.object(sys.stderr, "write")
    def test_include_exclude_project(self, mock_stderr_write):
        """ Test that projects cannot be included and excluded. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual([call(USAGE_MESSAGE),
                          call("next-action: error: project DogHouse is both included and excluded\n")],
                         mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "-+"])
    @patch.object(sys.stderr, "write")
    def test_empty_excluded_project(self, mock_stderr_write):
        """ Test that the argument parser exits if the project is empty. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual([call(USAGE_MESSAGE),
                          call("next-action: error: argument <context|project>: project name missing\n")],
                         mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "+DogHouse", "@home", "+PaintHouse", "@weekend"])
    def test_contexts_and_projects(self):
        """ Test that the argument parser returns the contexts and the projects, even when mixed. """
        self.assertEqual({"home", "weekend"}, parse_arguments().filters[0])
        self.assertEqual({"DogHouse", "PaintHouse"}, parse_arguments().filters[1])

    @patch.object(sys, "argv", ["next-action", "home"])
    @patch.object(sys.stderr, "write")
    def test_faulty_option(self, mock_stderr_write):
        """ Test that the argument parser exits if the option is faulty. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual([call(USAGE_MESSAGE),
                          call("next-action: error: argument <context|project>: unrecognized arguments: home\n")],
                         mock_stderr_write.call_args_list)


class NumberTest(unittest.TestCase):
    """ Unit tests for the --number and --all arguments. """

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
        self.assertEqual([call(USAGE_MESSAGE),
                          call("next-action: error: argument -n/--number: invalid int value: 'not_a_number'\n")],
                         mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--all"])
    def test_all_actions(self):
        """ Test that --all option also sets the number of actions to show to a very big number. """
        self.assertEqual(sys.maxsize, parse_arguments().number)

    @patch.object(sys, "argv", ["next-action", "--all", "--number", "3"])
    @patch.object(sys.stderr, "write")
    def test_all_and_number(self, mock_stderr_write):
        """ Test that the argument parser exits if the both --all and --number are used. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual([call(USAGE_MESSAGE),
                          call("next-action: error: argument -n/--number: not allowed with argument -a/--all\n")],
                         mock_stderr_write.call_args_list)
