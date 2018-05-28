""" Unit test for the next action algorithm. """

import argparse
import unittest

from next_action import todotxt, pick_action


class PickActionTestCase(unittest.TestCase):
    """ Base class for pick action unit tests. """

    def setUp(self):
        self.namespace = argparse.Namespace()
        self.namespace.filters = []
        self.namespace.overdue = False
        self.namespace.priority = None


class PickActionTest(PickActionTestCase):
    """ Unit tests for the pick action algorithm. """

    def test_no_tasks(self):
        """ Test that no tasks means no next action. """
        self.assertEqual([], pick_action.next_actions([], self.namespace))

    def test_one_task(self):
        """ If there is one task, that one is the next action. """
        task = todotxt.Task("Todo")
        self.assertEqual([task], pick_action.next_actions([task], self.namespace))

    def test_multiple_tasks(self):
        """ If there are multiple tasks, the first is the next action. """
        task1 = todotxt.Task("Todo 1")
        task2 = todotxt.Task("Todo 2")
        self.assertEqual([task1, task2], pick_action.next_actions([task1, task2], self.namespace))

    def test_higher_prio_goes_first(self):
        """ If there are multiple tasks with different priorities, the task with the
            highest priority is the next action. """
        task1 = todotxt.Task("Todo 1")
        task2 = todotxt.Task("(B) Todo 2")
        task3 = todotxt.Task("(A) Todo 3")
        self.assertEqual([task3, task2, task1], pick_action.next_actions([task1, task2, task3], self.namespace))

    def test_creation_dates(self):
        """ Test that a task with an older creation date takes precedence. """
        no_creation_date = todotxt.Task("Task 1")
        newer_task = todotxt.Task("2018-02-02 Task 2")
        older_task = todotxt.Task("2017-01-01 Task 3")
        self.assertEqual([older_task, newer_task, no_creation_date],
                         pick_action.next_actions([no_creation_date, newer_task, older_task], self.namespace))

    def test_priority_and_creation_date(self):
        """ Test that priority takes precedence over creation date. """
        priority = todotxt.Task("(C) Task 1")
        newer_task = todotxt.Task("2018-02-02 Task 2")
        older_task = todotxt.Task("2017-01-01 Task 3")
        self.assertEqual([priority, older_task, newer_task],
                         pick_action.next_actions([priority, newer_task, older_task], self.namespace))

    def test_due_dates(self):
        """ Test that a task with an earlier due date takes precedence. """
        no_due_date = todotxt.Task("Task 1")
        earlier_task = todotxt.Task("Task 2 due:2018-02-02")
        later_task = todotxt.Task("Task 3 due:2019-01-01")
        self.assertEqual([earlier_task, later_task, no_due_date],
                         pick_action.next_actions([no_due_date, later_task, earlier_task], self.namespace))

    def test_due_and_creation_dates(self):
        """ Test that a task with a due date takes precedence over creation date. """
        task1 = todotxt.Task("2018-1-1 Task 1")
        task2 = todotxt.Task("Task 2 due:2018-1-1")
        self.assertEqual([task2, task1], pick_action.next_actions([task1, task2], self.namespace))

    def test_project(self):
        """ Test that a task with a project takes precedence over a task without a project. """
        task1 = todotxt.Task("Task 1")
        task2 = todotxt.Task("Task 2 +Project")
        self.assertEqual([task2, task1], pick_action.next_actions([task1, task2], self.namespace))

    def test_projects(self):
        """ Test that a task with more projects takes precedence over a task with less projects. """
        task1 = todotxt.Task("Task 1 +Project")
        task2 = todotxt.Task("Task 2 +Project1 +Project2")
        self.assertEqual([task2, task1], pick_action.next_actions([task1, task2], self.namespace))


class FilterTasksTest(PickActionTestCase):
    """ Test that the tasks from which the next action is picked, can be filtered. """

    def test_context(self):
        """ Test that the next action can be limited to a specific context. """
        task1 = todotxt.Task("Todo 1 @work")
        task2 = todotxt.Task("(B) Todo 2 @work")
        task3 = todotxt.Task("(A) Todo 3 @home")
        self.namespace.filters = ["@work"]
        self.assertEqual([task2, task1], pick_action.next_actions([task1, task2, task3], self.namespace))

    def test_contexts(self):
        """ Test that the next action can be limited to a set of contexts. """
        task1 = todotxt.Task("Todo 1 @work @computer")
        task2 = todotxt.Task("(B) Todo 2 @work @computer")
        task3 = todotxt.Task("(A) Todo 3 @home @computer")
        self.namespace.filters = ["@work", "@computer"]
        self.assertEqual([task2, task1], pick_action.next_actions([task1, task2, task3], self.namespace))

    def test_excluded_context(self):
        """ Test that contexts can be excluded. """
        task = todotxt.Task("(A) Todo @computer")
        self.namespace.filters = ["-@computer"]
        self.assertEqual([], pick_action.next_actions([task], self.namespace))

    def test_excluded_contexts(self):
        """ Test that contexts can be excluded. """
        task = todotxt.Task("(A) Todo @computer @work")
        task = todotxt.Task("(A) Todo @computer")
        self.namespace.filters = ["-@computer"]
        self.assertEqual([], pick_action.next_actions([task], self.namespace))

    def test_not_excluded_context(self):
        """ Test that a task is not excluded if it doesn't belong to the excluded category. """
        task = todotxt.Task("(A) Todo @computer")
        self.namespace.filters = ["-@phone"]
        self.assertEqual([task], pick_action.next_actions([task], self.namespace))

    def test_project(self):
        """ Test that the next action can be limited to a specific project. """
        task1 = todotxt.Task("Todo 1 +ProjectX")
        task2 = todotxt.Task("(B) Todo 2 +ProjectX")
        task3 = todotxt.Task("(A) Todo 3 +ProjectY")
        self.namespace.filters = ["+ProjectX"]
        self.assertEqual([task2, task1], pick_action.next_actions([task1, task2, task3], self.namespace))

    def test_excluded_project(self):
        """ Test that projects can be excluded. """
        task = todotxt.Task("(A) Todo +DogHouse")
        self.namespace.filters = ["-+DogHouse"]
        self.assertEqual([], pick_action.next_actions([task], self.namespace))

    def test_excluded_projects(self):
        """ Test that projects can be excluded. """
        task = todotxt.Task("(A) Todo +DogHouse +PaintHouse")
        self.namespace.filters = ["-+DogHouse"]
        self.assertEqual([], pick_action.next_actions([task], self.namespace))

    def test_not_excluded_project(self):
        """ Test that a task is not excluded if it doesn't belong to the excluded project. """
        task = todotxt.Task("(A) Todo +DogHouse")
        self.namespace.filters = ["-+PaintHouse"]
        self.assertEqual([task], pick_action.next_actions([task], self.namespace))

    def test_project_and_context(self):
        """ Test that the next action can be limited to a specific project and context. """
        task1 = todotxt.Task("Todo 1 +ProjectX @office")
        task2 = todotxt.Task("(B) Todo 2 +ProjectX")
        task3 = todotxt.Task("(A) Todo 3 +ProjectY")
        self.namespace.filters = ["+ProjectX", "@office"]
        self.assertEqual([task1], pick_action.next_actions([task1, task2, task3], self.namespace))


class IgnoredTasksTest(PickActionTestCase):
    """ Test that certain tasks are ignored when picking the next action. """

    def test_ignore_completed_task(self):
        """ If there's one completed and one uncompleted task, the uncompleted one is the next action. """
        completed_task = todotxt.Task("x Completed")
        uncompleted_task = todotxt.Task("Todo")
        self.assertEqual(
            [uncompleted_task], pick_action.next_actions([completed_task, uncompleted_task], self.namespace))

    def test_ignore_future_task(self):
        """ Ignore tasks with a start date in the future. """
        future_task = todotxt.Task("(A) 9999-01-01 Start preparing for five-digit years")
        regular_task = todotxt.Task("(B) Look busy")
        self.assertEqual([regular_task], pick_action.next_actions([future_task, regular_task], self.namespace))

    def test_ignore_these_tasks(self):
        """ If all tasks are completed or future tasks, there's no next action. """
        completed_task1 = todotxt.Task("x Completed")
        completed_task2 = todotxt.Task("x Completed too")
        future_task = todotxt.Task("(A) 9999-01-01 Start preparing for five-digit years")
        self.assertEqual([], pick_action.next_actions([completed_task1, completed_task2, future_task], self.namespace))


class OverdueTasks(PickActionTestCase):
    """ Unit tests for the overdue filter. """
    def test_overdue_tasks(self):
        """ Test that tasks that not overdue are filtered. """
        no_duedate = todotxt.Task("Task")
        future_duedate = todotxt.Task("Task due:9999-01-01")
        overdue = todotxt.Task("Task due:2000-01-01")
        self.namespace.overdue = True
        self.assertEqual([overdue], pick_action.next_actions([no_duedate, future_duedate, overdue], self.namespace))


class MinimimPriorityTest(PickActionTest):
    """ Unit test for the mininum priority filter. """
    def test_priority(self):
        """ Test that tasks without priority are filtered. """
        no_priority = todotxt.Task("Task")
        high_priority = todotxt.Task("(A) Task")
        low_priority = todotxt.Task("(Z) Task")
        self.namespace.priority = "K"
        self.assertEqual(
            [high_priority], pick_action.next_actions([no_priority, low_priority, high_priority], self.namespace))
