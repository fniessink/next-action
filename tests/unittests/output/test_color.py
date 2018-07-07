"""Unit tests for the color module in the output package."""

import unittest

from next_action.output import colorize


class ColorizeTest(unittest.TestCase):
    """Unit tests for the colorize method."""

    def test_no_style(self):
        """Test that the output is unchanged when no style is passed."""
        task = "(A) Task @home +Project"
        self.assertEqual(task, colorize(task, ""))

    def test_default_style(self):
        """Test that the output is styled when a style is passed."""
        task = "(A) Task @home +Project"
        self.assertEqual('\x1b[38;5;18;01m(A)\x1b[39;00m Task \x1b[38;5;124m@home\x1b[39m \x1b[38;5;9m+Project\x1b[39m',
                         colorize(task, "default"))

    def test_strip_added_linebreak(self):
        """Test that the linebreak added by Pygments is removed."""
        task = "(A) Task @home +Project\n"
        self.assertEqual(
            '\x1b[38;5;18;01m(A)\x1b[39;00m Task \x1b[38;5;124m@home\x1b[39m \x1b[38;5;9m+Project\x1b[39m\n',
            colorize(task, "default"))
