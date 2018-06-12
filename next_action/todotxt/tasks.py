""" Collection of Todo.txt tasks. """

from typing import List, Set

from .task import Task


class Tasks(List[Task]):
    """ Collection of Todo.txt tasks. """

    def contexts(self) -> Set[str]:
        """ Return the contexts used in the collection of tasks. """
        return set().union(*[task.contexts() for task in self])

    def projects(self) -> Set[str]:
        """ Return the projects used in the collection of tasks. """
        return set().union(*[task.projects() for task in self])
