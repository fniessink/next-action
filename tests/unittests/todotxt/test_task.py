""" Unit tests for the todo.txt Task class. """

import datetime
import unittest
import string
from next_action import todotxt


class TodoTest(unittest.TestCase):
    """ Unit tests for the Task class that represents one task item. """

    def test_task_text(self):
        """ Test that the task text can be retrieved. """
        self.assertEqual("Todo", todotxt.Task("Todo").text)

    def test_task_repr(self):
        """ Test the task repr(). """
        self.assertEqual("Task<Todo>", repr(todotxt.Task("Todo")))


class TodoContextTest(unittest.TestCase):
    """ Unit tests for Task contexts. """

    def test_no_context(self):
        """ Test that a task without contexts has no contexts. """
        self.assertEqual(set(), todotxt.Task("Todo").contexts())

    def test_one_context(self):
        """ Test that the task context can be retrieved. """
        self.assertEqual({"home"}, todotxt.Task("Todo @home").contexts())

    def test_two_contexts(self):
        """ Test that multiple task contexts can be retrieved. """
        self.assertEqual({"home", "work"}, todotxt.Task("Todo @home @work").contexts())

    def test_no_space_before_at_sign(self):
        """ Test that a context with a space before the @-sign is not considered a context. """
        self.assertEqual(set(), todotxt.Task("Todo@home").contexts())


class TaskProjectTest(unittest.TestCase):
    """ Unit tests for task projects. """

    def test_no_projects(self):
        """ Test a task without projects. """
        self.assertEqual(set(), todotxt.Task("Todo").projects())

    def test_one_project(self):
        """ Test that the task project can be retrieved. """
        self.assertEqual({"projectx"}, todotxt.Task("Todo +projectx").projects())

    def test_two_projects(self):
        """ Test that multiple task projects can be retrieved. """
        self.assertEqual({"projectx", "projecty"}, todotxt.Task("Todo +projectx +projecty").projects())

    def test_no_space_before_at_sign(self):
        """ Test that a project with a space before the +-sign is not considered a project. """
        self.assertEqual(set(), todotxt.Task("Todo+project").projects())


class TaskPriorityTest(unittest.TestCase):
    """ Unit test for task priority. """

    def test_no_priority(self):
        """ Test a task without priority. """
        self.assertEqual(None, todotxt.Task("Todo").priority())

    def test_priorities(self):
        """ Test a task with a priority.  """
        for priority in string.ascii_uppercase:
            self.assertEqual(priority, todotxt.Task("({0}) Todo".format(priority)).priority())

    def test_faulty_priorities(self):
        """ Test that priorities must be one upper case letter. """
        for todo_txt in ("(a) Todo", " (a) Todo", "(A1) Todo", "(A Todo", "Todo (A)", "(A)Todo"):
            self.assertEqual(None, todotxt.Task(todo_txt).priority())


class CreationDateTest(unittest.TestCase):
    """ Unit tests for task creation dates. """

    def test_no_creation_date(self):
        """ Test that tasks have no creation date by default. """
        self.assertEqual(None, todotxt.Task("Todo").creation_date())

    def test_creation_date(self):
        """ Test a valid creation date. """
        self.assertEqual(datetime.date(2018, 1, 2), todotxt.Task("2018-01-02 Todo").creation_date())

    def test_creation_date_after_priority(self):  # pylint:disable=invalid-name
        """ Test a valid creation date after the priority. """
        self.assertEqual(datetime.date(2018, 12, 3), todotxt.Task("(B) 2018-12-03 Todo").creation_date())

    def test_invalid_creation_date(self):
        """ Test an invalid creation date. """
        self.assertEqual(None, todotxt.Task("2018-14-02 Todo").creation_date())

    def test_no_space_after(self):
        """ Test a creation date without a word boundary. """
        self.assertEqual(None, todotxt.Task("2018-10-10Todo").creation_date())

    def test_single_digits(self):
        """ Test a creation date with single digits for day and/or month. """
        self.assertEqual(datetime.date(2018, 12, 3), todotxt.Task("(B) 2018-12-3 Todo").creation_date())
        self.assertEqual(datetime.date(2018, 1, 13), todotxt.Task("(B) 2018-1-13 Todo").creation_date())
        self.assertEqual(datetime.date(2018, 1, 1), todotxt.Task("(B) 2018-1-1 Todo").creation_date())

    def test_is_future_task(self):
        """ Test that a task with a creation date in the future is a future task. """
        self.assertTrue(todotxt.Task("9999-01-01 Prepare for five-digit years").is_future())


class DueDateTest(unittest.TestCase):
    """ Unit tests for the due date of tasks. """

    def test_no_due_date(self):
        """ Test that tasks have no due date by default. """
        self.assertEqual(None, todotxt.Task("Todo").due_date())

    def test_due_date(self):
        """ Test a valid due date. """
        self.assertEqual(datetime.date(2018, 1, 2), todotxt.Task("Todo due:2018-01-02").due_date())

    def test_invalid_date(self):
        """ Test an invalid due date. """
        self.assertEqual(None, todotxt.Task("Todo due:2018-01-32").due_date())

    def test_no_space_after(self):
        """ Test a due date without a word boundary following it. """
        self.assertEqual(None, todotxt.Task("Todo due:2018-01-023").due_date())

    def test_single_digits(self):
        """ Test a due date with single digits for day and/or month. """
        self.assertEqual(datetime.date(2018, 12, 3), todotxt.Task("(B) due:2018-12-3 Todo").due_date())
        self.assertEqual(datetime.date(2018, 1, 13), todotxt.Task("(B) due:2018-1-13 Todo").due_date())
        self.assertEqual(datetime.date(2018, 1, 1), todotxt.Task("(B) due:2018-1-1 Todo").due_date())


class TaskCompletionTest(unittest.TestCase):
    """ Unit tests for the completion status of tasks. """

    def test_not_completed(self):
        """ Test that a task that doesn't start with an x isn't completed. """
        self.assertFalse(todotxt.Task("Task x").is_completed())

    def test_completed(self):
        """ Test that a task that does start with an x is completed. """
        self.assertTrue(todotxt.Task("x Completed task").is_completed())

    def test_space_after_x(self):
        """ Test that a task that does start with an x is completed. """
        self.assertFalse(todotxt.Task("xNotCompleted").is_completed())

    def test_x_must_be_lowercase(self):
        """ Test that a task that starts with an X isn't completed. """
        self.assertFalse(todotxt.Task("X Not completed").is_completed())


class ActionableTest(unittest.TestCase):
    """ Unit tests for the actionable status of tasks. """

    def test_default(self):
        """ Test that a default task is actionable. """
        self.assertTrue(todotxt.Task("Todo").is_actionable())

    def test_past_creation_date(self):
        """ Test that a task with a past creation date is actionable. """
        self.assertTrue(todotxt.Task("2018-01-01 Todo").is_actionable())

    def test_future_creation_date(self):
        """ Test that a task with a future creation date is not actionable. """
        self.assertFalse(todotxt.Task("9999-01-01 Todo").is_actionable())

    def test_completed_task(self):
        """ Test that a completed task is not actionable. """
        self.assertFalse(todotxt.Task("x 2018-01-01 Todo").is_actionable())

    def test_two_dates(self):
        """ Test that a completed task with a past creation date is not actionable. """
        self.assertFalse(todotxt.Task("x 2018-01-01 2018-01-01 Todo").is_actionable())
