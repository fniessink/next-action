"""Unit tests for the render function."""

import argparse
import unittest

from next_action import todotxt
from next_action.output import render_next_action


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
        self.assertEqual("Todo [todo.txt]", render_next_action([todotxt.Task("Todo", "todo.txt")], [], self.namespace))

    def test_reference_multiple(self):
        """Test that the source filename is added if reference is multiple and there are multiple todo.txt files."""
        self.namespace.file.append("work.txt")
        self.assertEqual(
            "Todo [todo.txt]\nProposal [work.txt]",
            render_next_action([todotxt.Task("Todo", "todo.txt"), todotxt.Task("Proposal", "work.txt")], [],
                               self.namespace))

    def test_reference_never(self):
        """Test that the source filename is not added if reference is never."""
        self.namespace.reference = "never"
        self.namespace.file.append("work.txt")
        self.assertEqual(
            "Todo\nProposal",
            render_next_action([todotxt.Task("Todo", "todo.txt"), todotxt.Task("Proposal", "work.txt")], [],
                               self.namespace))

    def test_blocked(self):
        """Test that the blocked task is rendered."""
        self.namespace.blocked = True
        rinse = todotxt.Task("Rinse before:repeat")
        repeat = todotxt.Task("Repeat id:repeat")
        rinse.add_blocked_task(repeat)
        self.assertEqual(
            "Rinse before:repeat\nblocks:\n- Repeat id:repeat",
            render_next_action([rinse], [], self.namespace))

    def test_blocked_multiple(self):
        """Test that multiple blocked tasks are rendered."""
        self.namespace.blocked = True
        lather = todotxt.Task("Rinse before:repeat before:rinse")
        repeat = todotxt.Task("Repeat id:repeat")
        rinse = todotxt.Task("Rinse id:rinse")
        lather.add_blocked_task(repeat)
        lather.add_blocked_task(rinse)
        self.assertEqual(
            "Rinse before:repeat before:rinse\nblocks:\n- Repeat id:repeat\n- Rinse id:rinse",
            render_next_action([lather], [], self.namespace))

    def test_blocked_recursive(self):
        """Test that the blocked tasks are rendered, recursively."""
        self.namespace.blocked = True
        lather = todotxt.Task("Lather before:rinse")
        rinse = todotxt.Task("Rinse id:rinse before:repeat")
        repeat = todotxt.Task("Repeat id:repeat")
        lather.add_blocked_task(rinse)
        rinse.add_blocked_task(repeat)
        self.assertEqual(
            "Lather before:rinse\nblocks:\n- Rinse id:rinse before:repeat\n  blocks:\n  - Repeat id:repeat",
            render_next_action([lather], [], self.namespace))
