import unittest

from next_action import todotxt, pick_action


class PickActionTest(unittest.TestCase):
    """ Unit tests for the pick action algorithm. """

    def test_no_tasks(self):
        """ Test that no tasks means no next action. """
        self.assertEqual(None, pick_action.next_action_based_on_priority([]))

    def test_one_task(self):
        """ If there is one task, that one is the next action. """
        task = todotxt.Task("Todo")
        self.assertEqual(task, pick_action.next_action_based_on_priority([task]))

    def test_multiple_tasks(self):
        """ If there are multiple tasks, the first is the next action. """
        task1 = todotxt.Task("Todo 1")
        task2 = todotxt.Task("Todo 2")
        self.assertEqual(task1, pick_action.next_action_based_on_priority([task1, task2]))

    def test_higher_prio_goes_first(self):
        """ If there are multiple tasks with different priorities, the task with the
            highest priority is the next action. """
        task1 = todotxt.Task("Todo 1")
        task2 = todotxt.Task("(B) Todo 2")
        task3 = todotxt.Task("(A) Todo 3")
        self.assertEqual(task3, pick_action.next_action_based_on_priority([task1, task2, task3]))

    def test_completed_tasks_are_not_next_action_based_on_priority(self):
        """ If all tasks are completed, there's no next action. """
        completed_task1 = todotxt.Task("x Completed")
        completed_task2 = todotxt.Task("x Completed too")
        self.assertEqual(None, pick_action.next_action_based_on_priority([completed_task1, completed_task2]))

    def test_completed_task_is_not_next_action_based_on_priority(self):
        """ If there's one completed and one uncompleted task, the uncompleted one is the next action. """
        completed_task = todotxt.Task("x Completed")
        uncompleted_task = todotxt.Task("Todo")
        self.assertEqual(uncompleted_task,
                         pick_action.next_action_based_on_priority([completed_task, uncompleted_task]))

    def test_next_action_limited_to_context(self):
        """ Test that the next action can be limited to a specific context. """
        task1 = todotxt.Task("Todo 1 @work")
        task2 = todotxt.Task("(B) Todo 2 @work")
        task3 = todotxt.Task("(A) Todo 3 @home")
        self.assertEqual(task2, pick_action.next_action_based_on_priority([task1, task2, task3], context="work"))
