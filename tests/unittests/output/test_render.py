"""Unit tests for the render functions."""

import argparse
import unittest

from hypothesis import given, strategies
from pygments.styles import get_all_styles

from next_action import todotxt
from next_action.output import render_next_action, render_arguments, render_grouped_tasks


class RenderNextActionTestCase(unittest.TestCase):
    """Base class for render unit tests."""

    def setUp(self):
        """Set up the namespace with default arguments for all unit tests."""
        self.filename1 = "todo.txt"
        self.namespace = argparse.Namespace()
        self.namespace.blocked = False
        self.namespace.line_number = False
        self.namespace.reference = "multiple"
        self.namespace.file = [self.filename1]
        self.namespace.style = None
        self.namespace.groupby = None


class RenderNextActionTest(RenderNextActionTestCase):
    """Unit tests for the render next action method."""

    def setUp(self):
        """Set up the namespace with default arguments for all unit tests."""
        super().setUp()
        self.line_number1 = 42
        self.filename2 = "work.txt"
        self.call_mom = todotxt.Task("Call mom", filename=self.filename1, line_number=self.line_number1)
        self.paint_house = todotxt.Task(
            "(A) Paint house @home +HomeImprovement due:2018-10-10", filename=self.filename2)
        self.fix_lamp = todotxt.Task("(A) Fix lamp @home +HomeImprovement due:2018-10-10", filename=self.filename2)

    def test_line_number(self):
        """Test that the line number is added if line_number is true."""
        self.namespace.line_number = True
        self.assertEqual(
            f"{self.call_mom.text} [{self.line_number1}]", render_next_action([self.call_mom], [], self.namespace))

    def test_reference_always(self):
        """Test that the source filename is added if reference is always."""
        self.namespace.reference = "always"
        self.assertEqual(
            f"{self.call_mom.text} [{self.filename1}]", render_next_action([self.call_mom], [], self.namespace))

    def test_reference_multiple(self):
        """Test that the source filename is added if reference is multiple and there are multiple todo.txt files."""
        self.namespace.file.append("work.txt")
        self.assertEqual(
            f"{self.call_mom.text} [{self.filename1}]\nProposal [{self.filename2}]",
            render_next_action([self.call_mom, todotxt.Task("Proposal", self.filename2)], [], self.namespace))

    def test_reference_never(self):
        """Test that the source filename is not added if reference is never."""
        self.namespace.reference = "never"
        self.namespace.file.append(self.filename2)
        self.assertEqual(
            f"{self.call_mom.text}\nProposal",
            render_next_action([self.call_mom, todotxt.Task("Proposal", self.filename2)], [], self.namespace))

    def test_line_number_and_filename(self):
        """Test that the line number and filename are added if line_number is true and reference is always."""
        self.namespace.reference = "always"
        self.namespace.line_number = True
        self.assertEqual(
            f"{self.call_mom.text} [{self.filename1}:{self.line_number1}]",
            render_next_action([self.call_mom], [], self.namespace))

    def test_groupby_context(self):
        """Test that next actions can be grouped by context."""
        self.namespace.groupby = "context"
        self.assertEqual(
            f"No context:\n- {self.call_mom.text}\nhome:\n- {self.paint_house.text}\n- {self.fix_lamp.text}",
            render_grouped_tasks([self.call_mom, self.paint_house, self.fix_lamp], self.namespace))

    def test_groupby_project(self):
        """Test that next actions can be grouped by project."""
        self.namespace.groupby = "project"
        self.assertEqual(
            f"No project:\n- {self.call_mom.text}\nHomeImprovement:\n- {self.paint_house.text}\n"
            f"- {self.fix_lamp.text}",
            render_grouped_tasks([self.call_mom, self.paint_house, self.fix_lamp], self.namespace))

    def test_groupby_priority(self):
        """Test that next actions can be grouped by priority."""
        self.namespace.groupby = "priority"
        self.assertEqual(
            f"No priority:\n- {self.call_mom.text}\nA:\n- {self.paint_house.text}\n- {self.fix_lamp.text}",
            render_grouped_tasks([self.call_mom, self.paint_house, self.fix_lamp], self.namespace))

    def test_groupby_due_date(self):
        """Test that next actions can be grouped by due date."""
        self.namespace.groupby = "duedate"
        self.assertEqual(
            f"No due date:\n- {self.call_mom.text}\n2018-10-10:\n- {self.paint_house.text}\n"
            f"- {self.fix_lamp.text}",
            render_grouped_tasks([self.call_mom, self.paint_house, self.fix_lamp], self.namespace))

    def test_groupby_source(self):
        """Test that next actions can be grouped by source file."""
        self.namespace.groupby = "source"
        self.assertEqual(
            f"{self.call_mom.filename}:\n- {self.call_mom.text}\n{self.paint_house.filename}:\n"
            f"- {self.paint_house.text}\n- {self.fix_lamp.text}",
            render_grouped_tasks([self.call_mom, self.paint_house, self.fix_lamp], self.namespace))


class RenderBlockedNextActionTest(RenderNextActionTestCase):
    """Unit tests for rendering blocked next actions."""

    def setUp(self):
        """Set up the namespace with default arguments for all unit tests."""
        super().setUp()
        self.repeat = todotxt.Task("Repeat id:repeat")

    def test_blocked(self):
        """Test that the blocked task is rendered."""
        self.namespace.blocked = True
        rinse = todotxt.Task("Rinse before:repeat")
        rinse.add_blocked_task(self.repeat)
        self.assertEqual(
            f"Rinse before:repeat\nblocks:\n- {self.repeat.text}", render_next_action([rinse], [], self.namespace))

    def test_blocked_multiple(self):
        """Test that multiple blocked tasks are rendered."""
        self.namespace.blocked = True
        lather = todotxt.Task("Rinse before:repeat before:rinse")
        rinse = todotxt.Task("Rinse id:rinse")
        lather.add_blocked_task(self.repeat)
        lather.add_blocked_task(rinse)
        self.assertEqual(
            f"Rinse before:repeat before:rinse\nblocks:\n- {self.repeat.text}\n- Rinse id:rinse",
            render_next_action([lather], [], self.namespace))

    def test_blocked_recursive(self):
        """Test that the blocked tasks are rendered, recursively."""
        self.namespace.blocked = True
        lather = todotxt.Task("Lather before:rinse")
        rinse = todotxt.Task("Rinse id:rinse before:repeat")
        lather.add_blocked_task(rinse)
        rinse.add_blocked_task(self.repeat)
        self.assertEqual(
            f"Lather before:rinse\nblocks:\n- Rinse id:rinse before:repeat\n  blocks:\n  - {self.repeat.text}",
            render_next_action([lather], [], self.namespace))


class RenderArgumentsTest(unittest.TestCase):
    """Unit tests for the render arguments method."""

    def test_arguments(self):
        """Test that the base arguments are rendered correctly."""
        self.assertEqual(
            "+ -+ --all --blocked --config-file --due --file --groupby --help --number --open-urls "
            "--overdue --priority --reference --style --version -@ -V -a -b -c -d -f -g -h -n -o -p -r -s -u @",
            render_arguments("all", todotxt.Tasks()))

    @given(strategies.sampled_from(["__groupby", "_g"]))
    def test_groupby(self, argument):
        """Test that the groupby arguments are rendered correctly."""
        self.assertEqual("context duedate priority project source", render_arguments(argument, todotxt.Tasks()))

    @given(strategies.sampled_from(["__reference", "_r"]))
    def test_reference(self, argument):
        """Test that the reference arguments are rendered correctly."""
        self.assertEqual("always multiple never", render_arguments(argument, todotxt.Tasks()))

    @given(strategies.sampled_from(["__style", "_s"]))
    def test_style(self, argument):
        """Test that the style arguments are rendered correctly."""
        self.assertEqual(" ".join(sorted(get_all_styles())), render_arguments(argument, todotxt.Tasks()))

    @given(strategies.sampled_from(["__priority", "_p"]))
    def test_priority_no_prios(self, argument):
        """Test that the priority arguments are rendered correctly."""
        self.assertEqual("", render_arguments(argument, todotxt.Tasks()))

    @given(strategies.sampled_from(["__priority", "_p"]))
    def test_priority(self, argument):
        """Test that the priority arguments are rendered correctly."""
        self.assertEqual("A C",
                         render_arguments(argument, todotxt.Tasks([todotxt.Task("(A) A"), todotxt.Task("(C) C")])))
