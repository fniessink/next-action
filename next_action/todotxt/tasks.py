""" Collection of Todo.txt tasks. """

from typing import List, Set

from .task import Task


class Tasks(List[Task]):
    """ Collection of Todo.txt tasks. """

    def contexts(self) -> Set[str]:
        """ Return the contexts used in the collection of tasks. """
        return set([context for task in self for context in task.contexts()])

    def projects(self) -> Set[str]:
        """ Return the projects used in the collection of tasks. """
        return set([project for task in self for project in task.projects()])
