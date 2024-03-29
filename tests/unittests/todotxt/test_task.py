"""Unit tests for the todo.txt Task class."""

import datetime
import string
import unittest

from hypothesis import given, strategies

from next_action import todotxt

# pylint: disable=no-member


class TodoTest(unittest.TestCase):
    """Unit tests for the Task class that represents one task item."""

    def test_task_text(self):
        """Test that the task text can be retrieved."""
        self.assertEqual("Todo", todotxt.Task("Todo").text)

    def test_task_repr(self):
        """Test the task repr()."""
        self.assertEqual("Task<Todo>", repr(todotxt.Task("Todo")))


BRACKETS = ["()", "<>", "{}", "[]", "''", '""']


class TodoContextTest(unittest.TestCase):
    """Unit tests for Task contexts."""

    def test_no_context(self):
        """Test that a task without contexts has no contexts."""
        self.assertEqual(set(), todotxt.Task("Todo").contexts())

    def test_one_context(self):
        """Test that the task context can be retrieved."""
        self.assertEqual({"home"}, todotxt.Task("Todo @home").contexts())

    def test_two_contexts(self):
        """Test that multiple task contexts can be retrieved."""
        self.assertEqual({"home", "work"}, todotxt.Task("Todo @home @work").contexts())

    def test_no_space_before_at_sign(self):
        """Test that a context with a space before the @-sign is not considered a context."""
        self.assertEqual(set(), todotxt.Task("Todo@home").contexts())

    def test_at_start_of_line(self):
        """Test that a context at the start of a line is considered a context."""
        self.assertEqual({"Home"}, todotxt.Task("@Home fix leak").contexts())

    @given(strategies.sampled_from(BRACKETS))
    def test_brackets(self, brackets):
        """Test that a brackted context is considered a context."""
        opening, closing = brackets[0], brackets[1]
        self.assertEqual({"home"}, todotxt.Task(f"Clean desk {opening}@home{closing}").contexts())


class TaskProjectTest(unittest.TestCase):
    """Unit tests for task projects."""

    def test_no_projects(self):
        """Test a task without projects."""
        self.assertEqual(set(), todotxt.Task("Todo").projects())

    def test_one_project(self):
        """Test that the task project can be retrieved."""
        self.assertEqual({"projectx"}, todotxt.Task("Todo +projectx").projects())

    def test_two_projects(self):
        """Test that multiple task projects can be retrieved."""
        self.assertEqual({"projectx", "projecty"}, todotxt.Task("Todo +projectx +projecty").projects())

    def test_no_space_before_at_sign(self):
        """Test that a project with a space before the +-sign is not considered a project."""
        self.assertEqual(set(), todotxt.Task("Todo+project").projects())

    def test_at_start_of_line(self):
        """Test that a project at the start of a line is considered a project."""
        self.assertEqual({"Maintenance"}, todotxt.Task("+Maintenance fix leak").projects())

    @given(strategies.sampled_from(BRACKETS))
    def test_brackets(self, brackets):
        """Test that a bracketed project is considered a project."""
        opening, closing = brackets[0], brackets[1]
        self.assertEqual({"GarageSale"}, todotxt.Task(f"Organize {opening}+GarageSale{closing} @home").projects())


class TaskPriorityTest(unittest.TestCase):
    """Unit test for task priority."""

    def test_no_priority(self):
        """Test a task without priority."""
        self.assertEqual(None, todotxt.Task("Todo").priority())

    def test_priorities(self):
        """Test a task with a priority."""
        for priority in string.ascii_uppercase:
            self.assertEqual(priority, todotxt.Task(f"({priority}) Todo").priority())

    def test_faulty_priorities(self):
        """Test that priorities must be one upper case letter."""
        for todo_txt in ("(a) Todo", " (a) Todo", "(A1) Todo", "(A Todo", "Todo (A)", "(A)Todo"):
            self.assertEqual(None, todotxt.Task(todo_txt).priority())

    def test_priority_at_least(self):
        """Test that the task has a minimum priority."""
        self.assertTrue(todotxt.Task("(A) Task").priority_at_least("A"))
        self.assertTrue(todotxt.Task("(A) Task").priority_at_least("B"))
        self.assertFalse(todotxt.Task("(B) Task").priority_at_least("A"))
        self.assertTrue(todotxt.Task("(Z) Task").priority_at_least("Z"))
        self.assertFalse(todotxt.Task("Task").priority_at_least("Z"))

    def test_blocking(self):
        """Test the priority of a task without its own priority.

        Test that the priority of a task without its own priority equals the priority of the task it is
        blocking.
        """
        after = todotxt.Task("(A) After id:1")
        before = todotxt.Task("Before before:1")
        after.set_is_blocked()
        before.add_blocked_task(after)
        self.assertEqual("A", before.priority())

    def test_blocking_multiple(self):
        """Test the priority of a task without its own priority.

        Test that the priority of a task without its own priority equals the highest priority of the tasks it is
        blocking.
        """
        after1 = todotxt.Task("(A) After id:1")
        after2 = todotxt.Task("(B) After after:before")
        before = todotxt.Task("Before before:1 id:before")
        before.add_blocked_task(after1)
        before.add_blocked_task(after2)
        after1.set_is_blocked()
        after2.set_is_blocked()
        self.assertEqual("A", before.priority())


class CreationDateTest(unittest.TestCase):
    """Unit tests for task creation dates.

    Next-action interprets creation dates in the future as threshold, or start date.
    """

    def test_no_creation_date(self):
        """Test that tasks have no creation date by default."""
        self.assertEqual(None, todotxt.Task("Todo").creation_date())

    def test_creation_date(self):
        """Test a valid creation date."""
        self.assertEqual(datetime.date(2018, 1, 2), todotxt.Task("2018-01-02 Todo").creation_date())

    def test_creation_date_after_priority(self):  # pylint:disable=invalid-name
        """Test a valid creation date after the priority."""
        self.assertEqual(datetime.date(2018, 12, 3), todotxt.Task("(B) 2018-12-03 Todo").creation_date())

    def test_invalid_creation_date(self):
        """Test an invalid creation date."""
        self.assertEqual(None, todotxt.Task("2018-14-02 Todo").creation_date())

    def test_no_space_after(self):
        """Test a creation date without a word boundary."""
        self.assertEqual(None, todotxt.Task("2018-10-10Todo").creation_date())

    def test_single_digits(self):
        """Test a creation date with single digits for day and/or month."""
        self.assertEqual(datetime.date(2018, 12, 3), todotxt.Task("(B) 2018-12-3 Todo").creation_date())
        self.assertEqual(datetime.date(2018, 1, 13), todotxt.Task("(B) 2018-1-13 Todo").creation_date())
        self.assertEqual(datetime.date(2018, 1, 1), todotxt.Task("(B) 2018-1-1 Todo").creation_date())

    def test_is_future_task(self):
        """Test that a task with a creation date in the future is a future task."""
        self.assertTrue(todotxt.Task("9999-01-01 Prepare for five-digit years").is_future())
        self.assertFalse(todotxt.Task(f"{datetime.date.today().isoformat()} Todo").is_future())


class ThresholdDateTest(unittest.TestCase):
    """Unit tests for the threshold date of a task.

    The core todo.txt standard only defines creation date, but threshold (t:<date>) seems to be a widely used
    convention.
    """

    def test_no_threshold(self):
        """Test that tasks have no threshold by default."""
        task = todotxt.Task("Todo")
        self.assertEqual(None, task.threshold_date())
        self.assertFalse(task.is_future())

    def test_past_threshold(self):
        """Test a past threshold date."""
        task = todotxt.Task("Todo t:2018-01-02")
        self.assertEqual(datetime.date(2018, 1, 2), task.threshold_date())
        self.assertFalse(task.is_future())

    def test_future_threshold(self):
        """Test a future threshold date."""
        task = todotxt.Task("Todo t:9999-01-01")
        self.assertEqual(datetime.date(9999, 1, 1), task.threshold_date())
        self.assertTrue(task.is_future())

    def test_threshold_today(self):
        """Test a task with threshold today."""
        task = todotxt.Task(f"Todo t:{datetime.date.today().isoformat()}")
        self.assertEqual(datetime.date.today(), task.threshold_date())
        self.assertFalse(task.is_future())


class DueDateTest(unittest.TestCase):
    """Unit tests for the due date of tasks."""

    def test_no_due_date(self):
        """Test that tasks have no due date by default."""
        task = todotxt.Task("Todo")
        self.assertEqual(None, task.due_date())
        self.assertFalse(task.is_overdue())

    def test_past_due_date(self):
        """Test a past due date."""
        task = todotxt.Task("Todo due:2018-01-02")
        self.assertEqual(datetime.date(2018, 1, 2), task.due_date())
        self.assertTrue(task.is_overdue())

    def test_future_due_date(self):
        """Test a future due date."""
        task = todotxt.Task("Todo due:9999-01-01")
        self.assertEqual(datetime.date(9999, 1, 1), task.due_date())
        self.assertFalse(task.is_overdue())

    def test_due_today(self):
        """Test a task due today."""
        task = todotxt.Task(f"Todo due:{datetime.date.today().isoformat()}")
        self.assertEqual(datetime.date.today(), task.due_date())
        self.assertFalse(task.is_overdue())

    def test_invalid_date(self):
        """Test an invalid due date."""
        task = todotxt.Task("Todo due:2018-01-32")
        self.assertEqual(None, task.due_date())
        self.assertFalse(task.is_overdue())

    def test_no_space_after(self):
        """Test a due date without a word boundary following it."""
        task = todotxt.Task("Todo due:2018-01-023")
        self.assertEqual(None, task.due_date())
        self.assertFalse(task.is_overdue())

    @given(strategies.sampled_from(["2018-01-1", "2018-1-01", "2018-1-1"]))
    def test_single_digits(self, due_date):
        """Test a due date with single digits for day and/or month."""
        self.assertEqual(datetime.date(2018, 1, 1), todotxt.Task(f"(B) due:{due_date} Todo").due_date())

    def test_is_due(self):
        """Test the is_due method."""
        self.assertTrue(todotxt.Task("due:2019-01-01").is_due(datetime.date.today()))
        self.assertTrue(todotxt.Task("due:2019-01-01").is_due(datetime.date(2019, 1, 1)))
        self.assertTrue(todotxt.Task("9999-01-01 due:2018-01-01").is_due(datetime.date(2018, 1, 1)))
        self.assertFalse(todotxt.Task("due:2018-01-01").is_due(datetime.date(2017, 12, 31)))
        self.assertFalse(todotxt.Task("Without due date").is_due(datetime.date(2017, 12, 31)))

    def test_blocking(self):
        """Test the due date of a task without its own due date.

        Test that the due date of a task without its own due date equals the due date of the task it is blocking.
        """
        after = todotxt.Task("After id:after due:2018-01-01")
        before = todotxt.Task("Before before:after")
        after.set_is_blocked()
        before.add_blocked_task(after)
        self.assertEqual(datetime.date(2018, 1, 1), before.due_date())

    def test_blocking_multiple(self):
        """Test the due date of a task without its own due date.

        Test that the due date of a task without its own due date equals the earliest due date of the tasks it is
        blocking.
        """
        after1 = todotxt.Task("After id:after due:2018-10-01")
        after2 = todotxt.Task("After after:before due:2018-01-01")
        before = todotxt.Task("Before before:after id:before")
        after1.set_is_blocked()
        after2.set_is_blocked()
        before.add_blocked_task(after1)
        before.add_blocked_task(after2)
        self.assertEqual(datetime.date(2018, 1, 1), before.due_date())


class DependenciesTest(unittest.TestCase):
    """Unit tests for dependency relations."""

    def setUp(self):
        """Set up some tasks."""
        self.task = todotxt.Task("Todo")
        self.blocked = todotxt.Task("Blocked")

    def test_unblocked_task(self):
        """Test that a task without dependencies is not blocked."""
        self.assertFalse(self.task.is_blocked())

    def test_set_blocked(self):
        """Test that a task can be blocked."""
        self.task.set_is_blocked()
        self.assertTrue(self.task.is_blocked())

    def test_blocked_tasks(self):
        """Test that a task can have tasks it blocks."""
        self.task.add_blocked_task(self.blocked)
        self.assertEqual([self.blocked], self.task.blocked_tasks())

    def test_block_self(self):
        """Test that a task can be blocked by itself.

        This doesn't make sense, but we're not in the business of validating todo.txt files.
        """
        self.task.add_blocked_task(self.task)
        self.assertEqual([self.task], self.task.blocked_tasks())

    def test_block_self_indirectly(self):
        """Test that a task can be blocked by a second task that is blocked by the first task.

        This doesn't make sense, but we're not in the business of validating todo.txt files.
        """
        self.task.add_blocked_task(self.blocked)
        self.blocked.add_blocked_task(self.task)
        self.assertEqual([self.task], self.blocked.blocked_tasks())
        self.assertEqual([self.blocked], self.task.blocked_tasks())


class TaskHiddenessTest(unittest.TestCase):
    """Unit tests for hidden tasks."""

    def test_visible_task(self):
        """Test that a regular task is not hidden."""
        task = todotxt.Task("A task")
        self.assertFalse(task.is_hidden())

    def test_hidden_task(self):
        """Test that a task with h:1 is hidden."""
        task = todotxt.Task("A task h:1")
        self.assertTrue(task.is_hidden())


class TaskURLsTest(unittest.TestCase):
    """Unit tests for URLs in tasks."""

    def test_no_urls(self):
        """Test that a task without URLs returns no URLs."""
        task = todotxt.Task("A task")
        self.assertEqual([], task.urls())

    def test_one_url(self):
        """Test that a task with a URLs returns the URL."""
        task = todotxt.Task("Search for things https://www.google.com")
        self.assertEqual(["https://www.google.com"], task.urls())

    def test_multiple_urls(self):
        """Test that a task with multiple URLs returns the URLs."""
        task = todotxt.Task("Search for things using https://www.google.com and https://duckduckgo.com")
        self.assertEqual(["https://www.google.com", "https://duckduckgo.com"], task.urls())

    def test_weird_urls(self):
        """Test that a task with weird URLs returns the URLs."""
        task = todotxt.Task("Check out https://www.google.com/check#/foo")
        self.assertEqual(["https://www.google.com/check#/foo"], task.urls())
