""" Unit tests for the todo.txt Task class. """

import datetime
import string
import unittest

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

    def test_priority_at_least(self):
        """ Test that the task has a minimum priority. """
        self.assertTrue(todotxt.Task("(A) Task").priority_at_least("A"))
        self.assertTrue(todotxt.Task("(A) Task").priority_at_least("B"))
        self.assertFalse(todotxt.Task("(B) Task").priority_at_least("A"))
        self.assertFalse(todotxt.Task("Task").priority_at_least("Z"))
        self.assertTrue(todotxt.Task("(Z) Task").priority_at_least(None))
        self.assertTrue(todotxt.Task("Task").priority_at_least(None))


class CreationDateTest(unittest.TestCase):
    """ Unit tests for task creation dates. Next-action interprets creation dates in the future as threshold, or
        start date. """

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
        self.assertFalse(todotxt.Task("{0} Todo".format(datetime.date.today().isoformat())).is_future())


class ThresholdDateTest(unittest.TestCase):
    """ Unit tests for the threshold date of a task. The core todo.txt standard only defines creation date, but
        threshold (t:<date>) seems to be a widely used convention. """

    def test_no_threshold(self):
        """ Test that tasks have no threshold by default. """
        task = todotxt.Task("Todo")
        self.assertEqual(None, task.threshold_date())
        self.assertFalse(task.is_future())

    def test_past_threshold(self):
        """ Test a past threshold date. """
        task = todotxt.Task("Todo t:2018-01-02")
        self.assertEqual(datetime.date(2018, 1, 2), task.threshold_date())
        self.assertFalse(task.is_future())

    def test_future_threshold(self):
        """ Test a future threshold date. """
        task = todotxt.Task("Todo t:9999-01-01")
        self.assertEqual(datetime.date(9999, 1, 1), task.threshold_date())
        self.assertTrue(task.is_future())

    def test_threshold_today(self):
        """ Test a task with threshold today. """
        task = todotxt.Task("Todo t:{0}".format(datetime.date.today().isoformat()))
        self.assertEqual(datetime.date.today(), task.threshold_date())
        self.assertFalse(task.is_future())


class DueDateTest(unittest.TestCase):
    """ Unit tests for the due date of tasks. """

    def test_no_due_date(self):
        """ Test that tasks have no due date by default. """
        task = todotxt.Task("Todo")
        self.assertEqual(None, task.due_date())
        self.assertFalse(task.is_overdue())

    def test_past_due_date(self):
        """ Test a past due date. """
        task = todotxt.Task("Todo due:2018-01-02")
        self.assertEqual(datetime.date(2018, 1, 2), task.due_date())
        self.assertTrue(task.is_overdue())

    def test_future_due_date(self):
        """ Test a future due date. """
        task = todotxt.Task("Todo due:9999-01-01")
        self.assertEqual(datetime.date(9999, 1, 1), task.due_date())
        self.assertFalse(task.is_overdue())

    def test_due_today(self):
        """ Test a task due today. """
        task = todotxt.Task("Todo due:{0}".format(datetime.date.today().isoformat()))
        self.assertEqual(datetime.date.today(), task.due_date())
        self.assertFalse(task.is_overdue())

    def test_invalid_date(self):
        """ Test an invalid due date. """
        task = todotxt.Task("Todo due:2018-01-32")
        self.assertEqual(None, task.due_date())
        self.assertFalse(task.is_overdue())

    def test_no_space_after(self):
        """ Test a due date without a word boundary following it. """
        task = todotxt.Task("Todo due:2018-01-023")
        self.assertEqual(None, task.due_date())
        self.assertFalse(task.is_overdue())

    def test_single_digits(self):
        """ Test a due date with single digits for day and/or month. """
        self.assertEqual(datetime.date(2018, 12, 3), todotxt.Task("(B) due:2018-12-3 Todo").due_date())
        self.assertEqual(datetime.date(2018, 1, 13), todotxt.Task("(B) due:2018-1-13 Todo").due_date())
        self.assertEqual(datetime.date(2018, 1, 1), todotxt.Task("(B) due:2018-1-1 Todo").due_date())

    def test_is_due(self):
        """ Test the is_due method. """
        self.assertTrue(todotxt.Task("due:2018-01-01").is_due(datetime.date.today()))
        self.assertTrue(todotxt.Task("due:2018-01-01").is_due(datetime.date(2018, 1, 1)))
        self.assertFalse(todotxt.Task("due:2018-01-01").is_due(datetime.date(2017, 12, 31)))
        self.assertFalse(todotxt.Task("Without due date").is_due(datetime.date(2017, 12, 31)))
        self.assertTrue(todotxt.Task("9999-01-01 due:2018-01-01").is_due(datetime.date(2018, 1, 1)))
        self.assertTrue(todotxt.Task("x Completed due:2018-01-01").is_due(datetime.date(2018, 1, 1)))


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


class ParentTest(unittest.TestCase):
    """ Unit tests for parent/child relations. """

    def test_default(self):
        """ Test that a default task has no parents. """
        default_task = todotxt.Task("Todo")
        self.assertEqual(set(), default_task.parent_ids())
        self.assertEqual("", default_task.task_id())
        self.assertFalse(default_task.is_blocked([]))
        self.assertFalse(default_task.is_blocked([default_task]))

    def test_missing_values(self):
        """ Test parent and id keys without ids. """
        self.assertEqual("", todotxt.Task("Todo id:").task_id())
        self.assertEqual(set(), todotxt.Task("Todo p:").parent_ids())

    def test_one_parent(self):
        """ Test that a task with a parent id return the correct id. """
        self.assertEqual({"1"}, todotxt.Task("Todo p:1").parent_ids())

    def test_two_parents(self):
        """ Test that a task with two parent ids return all ids. """
        self.assertEqual({"1", "123a"}, todotxt.Task("Todo p:1 p:123a").parent_ids())

    def test_task_id(self):
        """ Test a task id. """
        self.assertEqual("foo", todotxt.Task("Todo id:foo").task_id())

    def test_get_parent(self):
        """ Test getting a task's parent. """
        parent = todotxt.Task("Parent id:1")
        child = todotxt.Task("Child p:1")
        self.assertEqual([parent], child.parents([child, parent]))

    def test_get_multiple_parents(self):
        """ Test getting a task's mutiple parents. """
        parent1 = todotxt.Task("Parent 1 id:1")
        parent2 = todotxt.Task("Parent 2 id:2")
        child = todotxt.Task("Child p:1 p:2")
        self.assertEqual([parent1, parent2], child.parents([child, parent1, parent2]))

    def test_is_blocked(self):
        """ Test that a task with children is blocked. """
        parent = todotxt.Task("Parent id:1")
        child = todotxt.Task("Child p:1")
        self.assertTrue(parent.is_blocked([child, parent]))

    def test_completed_child(self):
        """ Test that a task with completed children only is not blocked. """
        parent = todotxt.Task("Parent id:1")
        child = todotxt.Task("x Child p:1")
        self.assertFalse(parent.is_blocked([child, parent]))

    def test_is_blocked_by_mix(self):
        """ Test that a task with completed children and uncompleted children is blocked. """
        parent = todotxt.Task("Parent id:1")
        child1 = todotxt.Task("Child 1 p:1")
        child2 = todotxt.Task("x Child 2 p:1")
        self.assertTrue(parent.is_blocked([child1, child2, parent]))

    def test_is_blocked_by_self(self):
        """ Test that a task can be blocked by itself. This doesn't make sense, but we're not in the business
            of validating todo.txt files. """
        parent = todotxt.Task("Parent id:1 p:1")
        self.assertTrue(parent.is_blocked([parent]))

    def test_block_circle(self):
        """ Test that a task can be blocked by its child who is blocked by the task. This doesn't make sense,
            but we're not in the business of validating todo.txt files. """
        task1 = todotxt.Task("Task 1 id:1 p:2")
        task2 = todotxt.Task("Task 2 id:2 p:1")
        self.assertTrue(task1.is_blocked([task1, task2]))
