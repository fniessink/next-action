""" Unit tests for the argument parsing classes. """

import os
import sys
import unittest
from unittest.mock import patch, call

from next_action.arguments import parse_arguments


class ArgumentParserTest(unittest.TestCase):
    """ Unit tests for the argument parses. """

    @patch.object(sys, "argv", ["next-action"])
    def test_default_filename(self):
        """ Test that the argument parser has a default filename. """
        self.assertEqual("todo.txt", parse_arguments().file)

    @patch.object(sys, "argv", ["next-action", "-f", "my_todo.txt"])
    def test_filename_argument(self):
        """ Test that the argument parser accepts a filename. """
        self.assertEqual("my_todo.txt", parse_arguments().file)

    @patch.object(sys, "argv", ["next-action", "--file", "my_other_todo.txt"])
    def test_long_filename_argument(self):
        """ Test that the argument parser accepts a filename. """
        self.assertEqual("my_other_todo.txt", parse_arguments().file)

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
        self.assertEqual([call("usage: next-action [-h] [--version] [-f FILE] [@CONTEXT [@CONTEXT ...]] "
                               "[+PROJECT [+PROJECT ...]]\n"),
                          call("next-action: error: Context name cannot be empty.\n")],
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
        self.assertEqual([call("usage: next-action [-h] [--version] [-f FILE] [@CONTEXT [@CONTEXT ...]] "
                               "[+PROJECT [+PROJECT ...]]\n"),
                          call("next-action: error: Project name cannot be empty.\n")],
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
        self.assertEqual([call("usage: next-action [-h] [--version] [-f FILE] [@CONTEXT [@CONTEXT ...]] "
                               "[+PROJECT [+PROJECT ...]]\n"),
                          call("next-action: error: Unrecognized argument 'home'.\n")],
                         mock_stderr_write.call_args_list)
