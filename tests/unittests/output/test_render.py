"""Unit tests for the render functions."""

import argparse
import unittest

from hypothesis import given, strategies
from pygments.styles import get_all_styles

from next_action import todotxt
from next_action.output import render_next_action, render_arguments, render_grouped_tasks


class RenderNextActionTest(unittest.TestCase):
    """Unit tests for the render next action method."""

    def setUp(self):
        """Set up the namespace with default arguments for all unit tests."""
        self.namespace = argparse.Namespace()
        self.namespace.reference = "multiple"
        self.namespace.file = ["todo.txt"]
        self.namespace.style = None
        self.namespace.blocked = False
        self.namespace.groupby = None

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

    def test_groupby_context(self):
        """Test that next actions can be grouped by context."""
        self.namespace.groupby = "context"
        no_context = todotxt.Task("Call mom")
        paint_house = todotxt.Task("Paint house @home")
        fix_lamp = todotxt.Task("Fix lamp @home")
        self.assertEqual(
            "No context:\n- Call mom\nhome:\n- Paint house @home\n- Fix lamp @home",
            render_grouped_tasks([no_context, paint_house, fix_lamp], self.namespace))

    def test_groupby_project(self):
        """Test that next actions can be grouped by project."""
        self.namespace.groupby = "project"
        no_project = todotxt.Task("Call mom")
        paint_house = todotxt.Task("Paint house +HomeImprovement")
        fix_lamp = todotxt.Task("Fix lamp +HomeImprovement")
        self.assertEqual(
            "No project:\n- Call mom\nHomeImprovement:\n- Paint house +HomeImprovement\n- Fix lamp +HomeImprovement",
            render_grouped_tasks([no_project, paint_house, fix_lamp], self.namespace))

    def test_groupby_priority(self):
        """Test that next actions can be grouped by priority."""
        self.namespace.groupby = "priority"
        no_priority = todotxt.Task("Call mom")
        paint_house = todotxt.Task("(A) Paint house")
        fix_lamp = todotxt.Task("(A) Fix lamp")
        self.assertEqual(
            "No priority:\n- Call mom\nA:\n- (A) Paint house\n- (A) Fix lamp",
            render_grouped_tasks([no_priority, paint_house, fix_lamp], self.namespace))

    def test_groupby_due_date(self):
        """Test that next actions can be grouped by due date."""
        self.namespace.groupby = "duedate"
        no_due_date = todotxt.Task("Call mom")
        paint_house = todotxt.Task("Paint house due:2018-10-10")
        fix_lamp = todotxt.Task("Fix lamp due:2018-10-10")
        self.assertEqual(
            "No due date:\n- Call mom\n2018-10-10:\n- Paint house due:2018-10-10\n- Fix lamp due:2018-10-10",
            render_grouped_tasks([no_due_date, paint_house, fix_lamp], self.namespace))

    def test_groupby_source(self):
        """Test that next actions can be grouped by source file."""
        self.namespace.groupby = "source"
        no_due_date = todotxt.Task("Call mom", filename="todo.tsk")
        paint_house = todotxt.Task("Paint house due:2018-10-10", filename="another.tsk")
        fix_lamp = todotxt.Task("Fix lamp due:2018-10-10", filename="another.tsk")
        self.assertEqual(
            f"{no_due_date.filename}:\n- Call mom\n{paint_house.filename}:\n- Paint house due:2018-10-10\n"
            "- Fix lamp due:2018-10-10", render_grouped_tasks([no_due_date, paint_house, fix_lamp], self.namespace))


class RenderArgumentsTest(unittest.TestCase):
    """Unit tests for the render arguments method."""

    def test_arguments(self):
        """Test that the base arguments are rendered correctly."""
        self.assertEqual("+ -+ --all --blocked --config-file --due --file --groupby --help --number --overdue "
                         "--priority --reference --style --version -@ -V -a -b -c -d -f -g -h -n -o -p -r -s @",
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
