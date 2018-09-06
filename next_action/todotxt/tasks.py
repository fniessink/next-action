"""Collection of Todo.txt tasks."""

from typing import List, Set

from .task import Task


class Tasks(List[Task]):
    """Collection of Todo.txt tasks."""

    # pylint: disable=not-an-iterable

    def contexts(self) -> Set[str]:
        """Return the contexts used in the collection of tasks."""
        return set(context for task in self for context in task.contexts())

    def projects(self) -> Set[str]:
        """Return the projects used in the collection of tasks."""
        return set(project for task in self for project in task.projects())

    def priorities(self) -> Set[str]:
        """Return the priorities used in the collection of tasks."""
        return set(str(task.priority()) for task in self if task.priority())
