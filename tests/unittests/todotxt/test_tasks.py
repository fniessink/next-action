""" Unit tests for the Tasks class. """

import unittest

from next_action.todotxt import Tasks, Task


class ContextsTest(unittest.TestCase):
    """ Unit tests for the contexts methods. """

    def test_no_tasks(self):
        """ Test that an empty tasks collection has no contexts. """
        self.assertEqual(set(), Tasks().contexts())

    def test_task_without_context(self):
        """ Test that a task collection with tasks without contexts has not contexts. """
        self.assertEqual(set(), Tasks([Task("Todo")]).contexts())

    def test_task_with_context(self):
        """ Test that a task collection with a task with a context has that context. """
        self.assertEqual(set(["work"]), Tasks([Task("Todo @work")]).contexts())

    def test_task_with_contexts(self):
        """ Test that a task collection with a task with contexts has those contexts. """
        self.assertEqual(set(["office", "work"]), Tasks([Task("Todo @work @office")]).contexts())

    def test_tasks_with_contexts(self):
        """ Test that a task collection with tasks with contexts has those contexts. """
        self.assertEqual(set(["office", "work", "home"]),
                         Tasks([Task("Todo @work @office"), Task("Todo @home @office")]).contexts())


class ProjectsTest(unittest.TestCase):
    """ Unit tests for the projects method. """

    def test_no_tasks(self):
        """ Test that an empty tasks collection has no projects. """
        self.assertEqual(set(), Tasks().projects())

    def test_task_without_project(self):
        """ Test that a task collection with tasks without projects has not projects. """
        self.assertEqual(set(), Tasks([Task("Todo")]).projects())

    def test_task_with_project(self):
        """ Test that a task collection with a task with a project has that project. """
        self.assertEqual(set(["BigProject"]), Tasks([Task("Todo +BigProject")]).projects())

    def test_task_with_projects(self):
        """ Test that a task collection with a task with projects has those projects. """
        self.assertEqual(set(["This", "That"]), Tasks([Task("Todo +This +That")]).projects())

    def test_tasks_with_projects(self):
        """ Test that a task collection with tasks with projects has those projects. """
        self.assertEqual(set(["Foo", "Bar", "Baz"]),
                         Tasks([Task("Todo +Foo +Bar"), Task("Todo +Foo +Baz")]).projects())
