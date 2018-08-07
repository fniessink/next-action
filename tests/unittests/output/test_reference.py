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
        self.namespace.reference = "multiple"

    def test_always(self):
        """Test that the source filename is added."""
        self.namespace.reference = "always"
        self.assertEqual("Todo [todo.txt]", reference(todotxt.Task("Todo", "todo.txt"), self.namespace))

    def test_never(self):
        """Test that the source filename is not added."""
        self.namespace.reference = "never"
        self.assertEqual("Todo", reference(todotxt.Task("Todo", "todo.txt"), self.namespace))

    def test_multiple(self):
        """Test that the source filename is added."""
        self.namespace.file = ["todo.txt", "project.txt"]
        self.assertEqual("Todo [todo.txt]", reference(todotxt.Task("Todo", "todo.txt"), self.namespace))
