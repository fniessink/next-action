"""Unit tests for the configuration file parsing."""

import os
import sys
import unittest
from unittest.mock import patch, call, mock_open

import yaml

from next_action.arguments import config, parse_arguments

from .test_parser import USAGE_MESSAGE


class ConfigTestCase(unittest.TestCase):
    """Base class for configuration file unit tests."""

    def setUp(self):
        """Set the terminal width for all unit tests."""
        os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.

    @patch.object(sys.stderr, "write")
    def assert_parse_error(self, error_message: str, mock_stderr_write):
        """Assert parse_arguments throws a parse error and shows the error message."""
        self.assertRaises(SystemExit, parse_arguments)
        self.assertEqual(
            [call(USAGE_MESSAGE), call(f"next-action: error: {error_message}\n")], mock_stderr_write.call_args_list)


# pylint: disable=no-value-for-parameter


class ReadConfigFileTest(ConfigTestCase):
    """Unit tests for reading the config file."""

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg"])
    @patch.object(config, "open", mock_open(read_data=""))
    def test_empty_file(self):
        """Test that an empty config file doesn't change the filenames."""
        self.assertEqual(["~/todo.txt"], parse_arguments()[1].file)

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open")
    def test_missing_default_config(self, mock_file_open):
        """Test that a missing config file at the default location is no problem."""
        mock_file_open.side_effect = FileNotFoundError("file not found")
        self.assertEqual(["~/todo.txt"], parse_arguments()[1].file)

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="- this_is_invalid"))
    def test_invalid_document(self):
        """Test that a config file that's not valid YAML raises an error."""
        self.assert_parse_error(
            "~/.next-action.cfg is invalid: '['this_is_invalid']' is not a document, must be a dict")

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="foo: bar"))
    def test_no_file_key(self):
        """Test that a config file without file key doesn't change the filenames."""
        self.assert_parse_error("~/.next-action.cfg is invalid: foo: unknown field")

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg"])
    @patch.object(config, "open")
    def test_error_opening(self, mock_file_open):
        """Test a config file that throws an error."""
        mock_file_open.side_effect = OSError("file opening problem")
        self.assert_parse_error("can't open file: file opening problem")

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg"])
    @patch.object(config, "open")
    def test_error_parsing(self, mock_file_open):
        """Test a config file that throws a parsing error."""
        mock_file_open.side_effect = yaml.YAMLError("parse error")
        self.assert_parse_error("can't parse config.cfg: parse error")

    @patch.object(sys, "argv", ["next-action", "--config-file", "config.cfg"])
    @patch.object(config, "open")
    def test_file_not_found(self, mock_file_open):
        """Test a config file that throws an error."""
        mock_file_open.side_effect = FileNotFoundError("file not found")
        self.assert_parse_error("can't open file: file not found")

    @patch.object(sys, "argv", ["next-action", "--config-file"])
    @patch.object(config, "open")
    def test_skip_config(self, mock_file_open):
        """Test that the config file is not read if the user doesn't want to."""
        parse_arguments()
        self.assertEqual([], mock_file_open.call_args_list)


class WriteConfigFileTest(ConfigTestCase):
    """Unit tests for the write-config-file argument."""

    def setUp(self):
        """Set up the configuration file header and default configuration file."""
        super().setUp()
        self.default_configuration = "file: ~/todo.txt\nnumber: 1\nreference: multiple\nstyle: default\n"

    @patch.object(sys.stdout, "write")
    def assert_config(self, configuration: str, mock_stdout_write) -> None:
        """Assert that the configuration file written to stdout equals the specified config."""
        self.assertRaises(SystemExit, parse_arguments)
        config_file = "# Configuration file for Next-action. Edit the settings below as you like.\n" + configuration
        self.assertEqual([call(config_file)], mock_stdout_write.call_args_list)

    @patch.object(sys, "argv", ["next-action", "--write-config-file"])
    @patch.object(config, "open", mock_open(read_data=""))
    def test_default_file(self):
        """Test that a config file can be written to stdout."""
        self.assert_config(self.default_configuration)

    @patch.object(sys, "argv", ["next-action", "--write-config-file", "--number", "3", "--reference", "never",
                                "--style", "fruity", "--file", "~/tasks.txt", "--priority", "Z", "@context", "+project",
                                "-@excluded_context", "-+excluded_project"])
    @patch.object(config, "open", mock_open(read_data=""))
    def test_with_args(self):
        """Test that the config file written to stdout includes the other arguments."""
        self.assert_config(
            "file: ~/tasks.txt\nfilters:\n- '@context'\n- +project\n- -@excluded_context\n- -+excluded_project\n"
            "number: 3\npriority: Z\nreference: never\nstyle: fruity\n")

    @patch.object(sys, "argv", ["next-action", "--write-config-file", "--file", "~/tasks.txt", "--file", "project.txt"])
    @patch.object(config, "open", mock_open(read_data=""))
    def test_multiple_files(self):
        """Test that the config file contains a list of files if multiple file arguments are passed."""
        self.assert_config("file:\n- ~/tasks.txt\n- project.txt\nnumber: 1\nreference: multiple\nstyle: default\n")

    @patch.object(sys, "argv", ["next-action", "--write-config-file", "--all"])
    @patch.object(config, "open", mock_open(read_data=""))
    def test_show_all(self):
        """Test that the config file contains "all" true" instead of a number."""
        self.assert_config("all: true\nfile: ~/todo.txt\nreference: multiple\nstyle: default\n")

    @patch.object(sys, "argv", ["next-action", "--write-config-file", "--priority"])
    @patch.object(config, "open", mock_open(read_data=""))
    def test_priority(self):
        """Test that priority without argument is processed correctly."""
        self.assert_config(self.default_configuration)

    @patch.object(sys, "argv", ["next-action", "--write-config-file", "--blocked"])
    @patch.object(config, "open", mock_open(read_data=""))
    def test_blocked(self):
        """Test that the blocked option is processed correctly."""
        self.assert_config("blocked: true\nfile: ~/todo.txt\nnumber: 1\nreference: multiple\nstyle: default\n")

    @patch.object(sys, "argv", ["next-action", "--write-config-file", "--line-number"])
    @patch.object(config, "open", mock_open(read_data=""))
    def test_line_number(self):
        """Test that the line number option is processed correctly."""
        self.assert_config("file: ~/todo.txt\nline_number: true\nnumber: 1\nreference: multiple\nstyle: default\n")

    @patch.object(sys, "argv", ["next-action", "--write-config-file", "--groupby", "priority"])
    @patch.object(config, "open", mock_open(read_data=""))
    def test_groupby(self):
        """Test that the groupby argument is processed correctly."""
        self.assert_config("file: ~/todo.txt\ngroupby: priority\nnumber: 1\nreference: multiple\nstyle: default\n")

    @patch.object(sys, "argv", ["next-action", "--write-config-file"])
    @patch.object(config, "open", mock_open(read_data="number: 3"))
    def test_read_config(self):
        """Test that the written config file contains the read config file."""
        self.assert_config("file: ~/todo.txt\nnumber: 3\nreference: multiple\nstyle: default\n")

    @patch.object(sys, "argv", ["next-action", "--write-config-file", "--config"])
    @patch.object(config, "open", mock_open(read_data="number: 3"))
    def test_ignore_config(self):
        """Test that the written config file does not contain the read config file."""
        self.assert_config(self.default_configuration)


class FilenameTest(ConfigTestCase):
    """Unit tests for the config file parameter."""

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="file: 0"))
    def test_invalid_filename(self):
        """Test a config file with an invalid file name."""
        self.assert_parse_error("~/.next-action.cfg is invalid: file: must be of ['string', 'list'] type")

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="file:\n- todo.txt\n- 0"))
    def test_valid_and_invalid(self):
        """Test a config file with an invalid file name."""
        self.assert_parse_error("~/.next-action.cfg is invalid: file: 1: must be of string type")

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="file: todo.txt"))
    def test_valid_file(self):
        """Test that a valid filename changes the filenames."""
        self.assertEqual(["todo.txt"], parse_arguments()[1].file)

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="file:\n- todo.txt\n- tada.txt"))
    def test_valid_files(self):
        """Test that a list of valid filenames changes the filenames."""
        self.assertEqual(["todo.txt", "tada.txt"], parse_arguments()[1].file)

    @patch.object(sys, "argv", ["next-action", "--file", "tada.txt"])
    @patch.object(config, "open", mock_open(read_data="file: todo.txt"))
    def test_cli_takes_precedence(self):
        """Test that a command line argument overrules the filename in the configuration file."""
        self.assertEqual(["tada.txt"], parse_arguments()[1].file)


class NumberTest(ConfigTestCase):
    """Unit tests for the number and all parameters."""

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="number: not_a_number"))
    def test_invalid_number(self):
        """Test a config file with an invalid number."""
        self.assert_parse_error("~/.next-action.cfg is invalid: number: must be of integer type")

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="number: 0"))
    def test_zero(self):
        """Test a config file with an invalid number."""
        self.assert_parse_error("~/.next-action.cfg is invalid: number: min value is 1")

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="number: 3"))
    def test_valid_number(self):
        """Test that a valid number changes the number argument."""
        self.assertEqual(3, parse_arguments()[1].number)

    @patch.object(sys, "argv", ["next-action", "--number", "3"])
    @patch.object(config, "open", mock_open(read_data="number: 2"))
    def test_cli_takes_precedence(self):
        """Test that a command line argument overrules the number in the configuration file."""
        self.assertEqual(3, parse_arguments()[1].number)

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="all: True"))
    def test_all_true(self):
        """Test that all is true sets number to the max number."""
        self.assertEqual(sys.maxsize, parse_arguments()[1].number)

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="all: False"))
    def test_all_false(self):
        """Test a config file with all is false."""
        self.assert_parse_error("~/.next-action.cfg is invalid: all: unallowed value False")

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="all: True\nnumber: 3"))
    def test_all_and_number(self):
        """Test that a config file with both --all and --number is invalid."""
        self.assert_parse_error("~/.next-action.cfg is invalid: number: 'all' must not be present with 'number'")

    @patch.object(sys, "argv", ["next-action", "--number", "3"])
    @patch.object(config, "open", mock_open(read_data="all: True"))
    def test_argument_nr_overrides(self):
        """Test that --number on the command line overrides --all in the configuration file."""
        self.assertEqual(3, parse_arguments()[1].number)

    @patch.object(sys, "argv", ["next-action", "--all"])
    @patch.object(config, "open", mock_open(read_data="number: 3"))
    def test_argument_all_overrides(self):
        """Test that --all on the command line overrides --number in the configuration file."""
        self.assertEqual(sys.maxsize, parse_arguments()[1].number)


class ConfigStyleTest(ConfigTestCase):
    """Unit tests for the style parameter."""

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="style: default"))
    def test_valid_style(self):
        """Test that a valid style changes the style argument."""
        self.assertEqual("default", parse_arguments()[1].style)

    @patch.object(sys, "argv", ["next-action", "--style", "vim"])
    @patch.object(config, "open", mock_open(read_data="style: default"))
    def test_override_style(self):
        """Test that a command line style overrides the style in the config file."""
        self.assertEqual("vim", parse_arguments()[1].style)

    @patch.object(sys, "argv", ["next-action", "--style"])
    @patch.object(config, "open", mock_open(read_data="style: default"))
    def test_cancel_style(self):
        """Test that --style without style cancels the style in the config file."""
        self.assertEqual(None, parse_arguments()[1].style)

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="style: invalid_style"))
    def test_invalid_style(self):
        """Test that an invalid style raises an error."""
        self.assert_parse_error("~/.next-action.cfg is invalid: style: unallowed value invalid_style")


class PriorityTest(ConfigTestCase):
    """Unit tests for the priority parameter."""

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="priority: Z"))
    def test_valid_priority(self):
        """Test that a valid priority changes the priority argument."""
        self.assertEqual("Z", parse_arguments()[1].priority)

    @patch.object(sys, "argv", ["next-action", "--priority", "M"])
    @patch.object(config, "open", mock_open(read_data="priority: Z"))
    def test_override_priority(self):
        """Test that a command line option overrides the priority in the config file."""
        self.assertEqual("M", parse_arguments()[1].priority)

    @patch.object(sys, "argv", ["next-action", "-pM"])
    @patch.object(config, "open", mock_open(read_data="priority: Z"))
    def test_override_short(self):
        """Test that a short command line option overrides the priority in the config file."""
        self.assertEqual("M", parse_arguments()[1].priority)

    @patch.object(sys, "argv", ["next-action", "--priority"])
    @patch.object(config, "open", mock_open(read_data="priority: Z"))
    def test_cancel_priority(self):
        """Test that a command line option overrides the priority in the config file."""
        self.assertEqual(None, parse_arguments()[1].priority)

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="priority: ZZZ"))
    def test_invalid_priority(self):
        """Test that an invalid priority raises an error."""
        self.assert_parse_error("~/.next-action.cfg is invalid: priority: unallowed value ZZZ")


class LineNumberTest(ConfigTestCase):
    """Unit tests for the line number parameter."""

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="line_number: true"))
    def test_valid_line_number(self):
        """Test that a valid line number value changes the line number argument."""
        self.assertEqual(True, parse_arguments()[1].line_number)

    @patch.object(sys, "argv", ["next-action", "--line-number"])
    @patch.object(config, "open", mock_open(read_data="line_number: true"))
    def test_override(self):
        """Test that a command line argument overrides the configured value."""
        self.assertEqual(True, parse_arguments()[1].line_number)

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="line_number: false"))
    def test_invalid_line_number(self):
        """Test that an invalid value raises an error."""
        self.assert_parse_error("~/.next-action.cfg is invalid: line_number: unallowed value False")


class ReferenceTest(ConfigTestCase):
    """Unit tests for the reference parameter."""

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="reference: always"))
    def test_valid_reference(self):
        """Test that a valid reference value changes the reference argument."""
        self.assertEqual("always", parse_arguments()[1].reference)

    @patch.object(sys, "argv", ["next-action", "--reference", "never"])
    @patch.object(config, "open", mock_open(read_data="reference: always"))
    def test_override(self):
        """Test that a command line argument overrides the configured value."""
        self.assertEqual("never", parse_arguments()[1].reference)

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="reference: invalid"))
    def test_invalid_reference(self):
        """Test that an invalid value raises an error."""
        self.assert_parse_error("~/.next-action.cfg is invalid: reference: unallowed value invalid")


class GroupByTest(ConfigTestCase):
    """Unit tests for the group by parameter."""

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="groupby: context"))
    def test_valid_group(self):
        """Test that a valid group value changes the group by argument."""
        self.assertEqual("context", parse_arguments()[1].groupby)

    @patch.object(sys, "argv", ["next-action", "--groupby", "duedate"])
    @patch.object(config, "open", mock_open(read_data="groupby: project"))
    def test_override(self):
        """Test that a command line argument overrides the configured value."""
        self.assertEqual("duedate", parse_arguments()[1].groupby)

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="groupby: invalid"))
    def test_invalid_group(self):
        """Test that an invalid value raises an error."""
        self.assert_parse_error("~/.next-action.cfg is invalid: groupby: unallowed value invalid")


class FiltersTest(ConfigTestCase):
    """Unit tests for the filters parameter."""

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="filters: +ImportantProject"))
    def test_project(self):
        """Test that a valid project changes the filters argument."""
        self.assertEqual({"ImportantProject"}, parse_arguments()[1].projects)

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="filters: +ImportantProject +SideProject"))
    def test_projects(self):
        """Test that multiple valid projects change the filters argument."""
        self.assertEqual({"ImportantProject", "SideProject"}, parse_arguments()[1].projects)

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="filters: '@work'"))
    def test_context(self):
        """Test that a valid context changes the filters argument."""
        self.assertEqual({"work"}, parse_arguments()[1].contexts)

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="filters: '@work @desk'"))
    def test_contexts(self):
        """Test that valid contexts change the filters argument."""
        self.assertEqual({"work", "desk"}, parse_arguments()[1].contexts)

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="filters:\n- '@work'\n- -@waiting\n"))
    def test_context_list(self):
        """Test that a valid context changes the filters argument."""
        self.assertEqual({"work"}, parse_arguments()[1].contexts)
        self.assertEqual({"waiting"}, parse_arguments()[1].excluded_contexts)

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="filters: -+SideProject"))
    def test_excluded_project(self):
        """Test that an excluded valid project changes the filters argument."""
        self.assertEqual({"SideProject"}, parse_arguments()[1].excluded_projects)

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="filters: -@home"))
    def test_excluded_context(self):
        """Test that an excluded valid context changes the filters argument."""
        self.assertEqual({"home"}, parse_arguments()[1].excluded_contexts)

    @patch.object(sys, "argv", ["next-action", "+ImportantProject"])
    @patch.object(config, "open", mock_open(read_data="filters: +ImportantProject"))
    def test_same_project(self):
        """Test that the configuration is ignored when the command line specifies the same project."""
        self.assertEqual({"ImportantProject"}, parse_arguments()[1].projects)

    @patch.object(sys, "argv", ["next-action", "+ImportantProject"])
    @patch.object(config, "open", mock_open(read_data="filters: -+ImportantProject"))
    def test_inverse_project(self):
        """Test that the configuration is ignored when the command line specifies the same project."""
        self.assertEqual(set(), parse_arguments()[1].excluded_projects)
        self.assertEqual({"ImportantProject"}, parse_arguments()[1].projects)

    @patch.object(sys, "argv", ["next-action", "+ImportantProject"])
    @patch.object(config, "open", mock_open(read_data="filters: -+ImportantProject @work"))
    def test_ignore_project_not_context(self):
        """Test that the configuration is ignored when the command line specifies the same project."""
        self.assertEqual(set(), parse_arguments()[1].excluded_projects)
        self.assertEqual({"ImportantProject"}, parse_arguments()[1].projects)
        self.assertEqual({"work"}, parse_arguments()[1].contexts)

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="filters:\n- invalid\n"))
    def test_invalid_filter_list(self):
        """Test that an invalid filter raises an error."""
        regex = r"^\-?[@|\+]\S+"
        self.assert_parse_error(f"~/.next-action.cfg is invalid: filters: 0: value does not match regex '{regex}'")

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="filters: invalid\n"))
    def test_invalid_filter_string(self):
        """Test that an invalid filter raises an error."""
        regex = r"^\-?[@|\+]\S+(\s+\-?[@|\+]\S+)*"
        self.assert_parse_error(f"~/.next-action.cfg is invalid: filters: value does not match regex '{regex}'")


class BlockedTest(ConfigTestCase):
    """Unit tests for the blocked parameter."""

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="blocked: true"))
    def test_blocked(self):
        """Test that the configured value changes the blocked argument."""
        self.assertEqual(True, parse_arguments()[1].blocked)

    @patch.object(sys, "argv", ["next-action", "--blocked"])
    @patch.object(config, "open", mock_open(read_data="blocked: true"))
    def test_override(self):
        """Test that a command line argument overrides the configured value."""
        self.assertEqual(True, parse_arguments()[1].blocked)

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="blocked: false"))
    def test_invalid_blocked_value(self):
        """Test that an invalid value raises an error."""
        self.assert_parse_error("~/.next-action.cfg is invalid: blocked: unallowed value False")


class OpenUrlsTest(ConfigTestCase):
    """Unit tests for the open-urls parameter."""

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="open_urls: true"))
    def test_open_urls(self):
        """Test that the configured value changes the open-urls argument."""
        self.assertEqual(True, parse_arguments()[1].open_urls)

    @patch.object(sys, "argv", ["next-action", "--open-urls"])
    @patch.object(config, "open", mock_open(read_data="open_urls: true"))
    def test_override(self):
        """Test that a command line argument overrides the configured value."""
        self.assertEqual(True, parse_arguments()[1].open_urls)

    @patch.object(sys, "argv", ["next-action"])
    @patch.object(config, "open", mock_open(read_data="open_urls: false"))
    def test_invalid_open_urls_value(self):
        """Test that an invalid value raises an error."""
        self.assert_parse_error("~/.next-action.cfg is invalid: open_urls: unallowed value False")
