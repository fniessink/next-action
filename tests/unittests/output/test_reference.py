"""Unit tests for the reference module in the output package."""

import argparse
import unittest

from next_action import todotxt
from next_action.output import reference


class ReferenceTest(unittest.TestCase):
    """Unit tests for the reference method."""

    def setUp(self):
        """Set up the namespace with default arguments for all unit tests."""
        self.namespace = argparse.Namespace()
        self.namespace.line_number = False
        self.namespace.reference = "multiple"
        self.filename = "todo.txt"
        self.line_number = 42
        self.namespace.file = [self.filename]
        self.task = todotxt.Task("Todo", self.filename, self.line_number)

    def test_line_number(self):
        """Test that the line number is added if line_number is true."""
        self.namespace.line_number = True
        self.assertEqual(f"Todo [{self.line_number}]", reference(self.task, self.namespace))

    def test_line_number_and_filename(self):
        """Test that the line number and file name are added if line_number is true and reference is always."""
        self.namespace.line_number = True
        self.namespace.reference = "always"
        self.assertEqual(f"Todo [{self.filename}:{self.line_number}]", reference(self.task, self.namespace))

    def test_always(self):
        """Test that the source filename is added."""
        self.namespace.reference = "always"
        self.assertEqual(f"Todo [{self.filename}]", reference(self.task, self.namespace))

    def test_never(self):
        """Test that the source filename is not added."""
        self.namespace.reference = "never"
        self.assertEqual("Todo", reference(self.task, self.namespace))

    def test_multiple(self):
        """Test that the source filename is added."""
        self.namespace.file.append("project.txt")
        self.assertEqual(f"Todo [{self.filename}]", reference(self.task, self.namespace))
