"""Unit tests for the render function."""

import argparse
import unittest

from next_action import todotxt
from next_action.output import render


class RenderTest(unittest.TestCase):
    """Unit tests for the render method."""

    def setUp(self):
        """Set up the namespace with default arguments for all unit tests."""
        self.namespace = argparse.Namespace()
        self.namespace.reference = "multiple"
        self.namespace.file = ["todo.txt"]
        self.namespace.style = None
        self.namespace.blocked = False

    def test_reference_always(self):
        """Test that the source filename is added if reference is always."""
        self.namespace.reference = "always"
        self.assertEqual("Todo [todo.txt]", render([todotxt.Task("Todo", "todo.txt")], self.namespace))

    def test_reference_multiple(self):
        """Test that the source filename is added if reference is multiple and there are multiple todo.txt files."""
        self.namespace.file.append("work.txt")
        self.assertEqual(
            "Todo [todo.txt]\nProposal [work.txt]",
            render([todotxt.Task("Todo", "todo.txt"), todotxt.Task("Proposal", "work.txt")], self.namespace))

    def test_reference_never(self):
        """Test that the source filename is not added if reference is never."""
        self.namespace.reference = "never"
        self.namespace.file.append("work.txt")
        self.assertEqual(
            "Todo\nProposal",
            render([todotxt.Task("Todo", "todo.txt"), todotxt.Task("Proposal", "work.txt")], self.namespace))

    def test_blocked(self):
        """Test that the blocked task is rendered."""
        self.namespace.blocked = True
        self.assertEqual(
            "Rinse before:repeat\nblocks:\n- Repeat id:repeat",
            render([todotxt.Task("Rinse before:repeat", tasks=[todotxt.Task("Repeat id:repeat")])],
                   self.namespace))

    def test_blocked_multiple(self):
        """Test that multiple blocked tasks are rendered."""
        self.namespace.blocked = True
        self.assertEqual(
            "Rinse before:repeat before:rinse\nblocks:\n- Repeat id:repeat\n- Rinse id:rinse",
            render([todotxt.Task("Rinse before:repeat before:rinse",
                                 tasks=[todotxt.Task("Repeat id:repeat"), todotxt.Task("Rinse id:rinse")])],
                   self.namespace))

    def test_blocked_recursive(self):
        """Test that the blocked tasks are rendered, recursively."""
        self.namespace.blocked = True
        self.assertEqual(
            "Lather before:rinse\nblocks:\n- Rinse id:rinse before:repeat\n  blocks:\n  - Repeat id:repeat",
            render([todotxt.Task("Lather before:rinse",
                                 tasks=[todotxt.Task("Rinse id:rinse before:repeat",
                                                     tasks=[todotxt.Task("Repeat id:repeat")])])],
                   self.namespace))
