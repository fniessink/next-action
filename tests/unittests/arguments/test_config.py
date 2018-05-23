""" Unit tests for the configration file parsing. """

import os
import sys
import unittest
from unittest.mock import patch, call, mock_open

import yaml

from next_action.arguments import config, parse_arguments

from .test_parser import USAGE_MESSAGE


class ConfigFileTest(unittest.TestCase):
    """ Unit tests for the config file. """

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg"])
    @patch.object(config, "open", mock_open(read_data=""))
    def test_empty_file(self):
        """ Test that an empty config file doesn't change the filenames. """
        self.assertEqual([os.path.expanduser("~/todo.txt")], parse_arguments().filenames)

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open")
    def test_missing_default_config(self, mock_file_open):
        """ Test that a missing config file at the default location is no problem. """
        mock_file_open.side_effect = FileNotFoundError("some problem")
        self.assertEqual([os.path.expanduser("~/todo.txt")], parse_arguments().filenames)

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg"])
    @patch.object(config, "open", mock_open(read_data="- this_is_invalid"))
    @patch.object(sys.stderr, "write")
    def test_invalid_document(self, mock_stderr_write):
        """ Test that a config file that's not valid YAML raises an error. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual([call(USAGE_MESSAGE),
                          call("next-action: error: config.cfg is invalid: '['this_is_invalid']' is not a document, "
                               "must be a dict\n")],
                         mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg"])
    @patch.object(config, "open", mock_open(read_data="foo: bar"))
    @patch.object(sys.stderr, "write")
    def test_no_file_key(self, mock_stderr_write):
        """ Test that a config file without file key doesn't change the filenames. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual([call(USAGE_MESSAGE),
                          call("next-action: error: config.cfg is invalid: {'foo': ['unknown field']}\n")],
                         mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg"])
    @patch.object(config, "open")
    @patch.object(sys.stderr, "write")
    def test_error_opening(self, mock_stderr_write, mock_file_open):
        """ Test a config file that throws an error. """
        mock_file_open.side_effect = OSError("some problem")
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual([call(USAGE_MESSAGE), call("next-action: error: can't open file: some problem\n")],
                         mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg"])
    @patch.object(config, "open")
    @patch.object(sys.stderr, "write")
    def test_error_parsing(self, mock_stderr_write, mock_file_open):
        """ Test a config file that throws a parsing error. """
        mock_file_open.side_effect = yaml.YAMLError("some problem")
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual([call(USAGE_MESSAGE), call("next-action: error: can't parse config.cfg: some problem\n")],
                         mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg"])
    @patch.object(config, "open")
    @patch.object(sys.stderr, "write")
    def test_file_not_found(self, mock_stderr_write, mock_file_open):
        """ Test a config file that throws an error. """
        mock_file_open.side_effect = FileNotFoundError("some problem")
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual([call(USAGE_MESSAGE), call("next-action: error: can't open file: some problem\n")],
                         mock_stderr_write.call_args_list)


class FilenameTest(unittest.TestCase):
    """ Unit tests for the config file parameter. """

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg"])
    @patch.object(config, "open", mock_open(read_data="file: 0"))
    @patch.object(sys.stderr, "write")
    def test_invalid_filename(self, mock_stderr_write):
        """ Test a config file with an invalid file name. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual(
            [call(USAGE_MESSAGE), call("next-action: error: config.cfg is invalid: "
                                       "{'file': [\"must be of ['string', 'list'] type\"]}\n")],
            mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg"])
    @patch.object(config, "open", mock_open(read_data="file:\n- todo.txt\n- 0"))
    @patch.object(sys.stderr, "write")
    def test_valid_and_invalid(self, mock_stderr_write):
        """ Test a config file with an invalid file name. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual(
            [call(USAGE_MESSAGE),
             call("next-action: error: config.cfg is invalid: {'file': [{1: ['must be of string type']}]}\n")],
            mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg"])
    @patch.object(config, "open", mock_open(read_data="file: todo.txt"))
    def test_valid_file(self):
        """ Test that a valid filename changes the filenames. """
        self.assertEqual(["todo.txt"], parse_arguments().filenames)

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg"])
    @patch.object(config, "open", mock_open(read_data="file:\n- todo.txt\n- tada.txt"))
    def test_valid_files(self):
        """ Test that a list of valid filenames changes the filenames. """
        self.assertEqual(["todo.txt", "tada.txt"], parse_arguments().filenames)

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg", "--file", "tada.txt"])
    @patch.object(config, "open", mock_open(read_data="file: todo.txt"))
    def test_cli_takes_precedence(self):
        """ Test that a command line argument overrules the filename in the configuration file. """
        self.assertEqual(["tada.txt"], parse_arguments().filenames)


class NumberTest(unittest.TestCase):
    """ Unit tests for the number and all parameters. """

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg"])
    @patch.object(config, "open", mock_open(read_data="number: not_a_number"))
    @patch.object(sys.stderr, "write")
    def test_invalid_number(self, mock_stderr_write):
        """ Test a config file with an invalid number. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual(
            [call(USAGE_MESSAGE), call("next-action: error: config.cfg is invalid: "
                                       "{'number': [\"must be of ['integer'] type\"]}\n")],
            mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg"])
    @patch.object(config, "open", mock_open(read_data="number: 0"))
    @patch.object(sys.stderr, "write")
    def test_zero(self, mock_stderr_write):
        """ Test a config file with an invalid number. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual(
            [call(USAGE_MESSAGE), call("next-action: error: config.cfg is invalid: {'number': ['min value is 1']}\n")],
            mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg"])
    @patch.object(config, "open", mock_open(read_data="number: 3"))
    def test_valid_number(self):
        """ Test that a valid number changes the number argument. """
        self.assertEqual(3, parse_arguments().number)

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg", "--number", "3"])
    @patch.object(config, "open", mock_open(read_data="number: 2"))
    def test_cli_takes_precedence(self):
        """ Test that a command line argument overrules the number in the configuration file. """
        self.assertEqual(3, parse_arguments().number)

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg"])
    @patch.object(config, "open", mock_open(read_data="all: True"))
    def test_all_true(self):
        """ Test that all is true sets number to the max number. """
        self.assertEqual(sys.maxsize, parse_arguments().number)

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg"])
    @patch.object(config, "open", mock_open(read_data="all: False"))
    @patch.object(sys.stderr, "write")
    def test_all_false(self, mock_stderr_write):
        """ Test a config file with all is false. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual(
            [call(USAGE_MESSAGE),
             call("next-action: error: config.cfg is invalid: {'all': ['unallowed value False']}\n")],
            mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg"])
    @patch.object(config, "open", mock_open(read_data="all: True\nnumber: 3"))
    @patch.object(sys.stderr, "write")
    def test_all_and_number(self, mock_stderr_write):
        """ Test that a config file with both --all and --number is invalid. """
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual(
            [call(USAGE_MESSAGE),
             call("next-action: error: config.cfg is invalid: {'number': "
                  "[\"'all' must not be present with 'number'\"]}\n")],
            mock_stderr_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg", "--number", "3"])
    @patch.object(config, "open", mock_open(read_data="all: True"))
    def test_argument_nr_overrides(self):
        """ Test that --number on the command line overrides --all in the configuration file. """
        self.assertEqual(3, parse_arguments().number)

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg", "--all"])
    @patch.object(config, "open", mock_open(read_data="number: 3"))
    def test_argument_all_overrides(self):
        """ Test that --all on the command line overrides --number in the configuration file. """
        self.assertEqual(sys.maxsize, parse_arguments().number)
