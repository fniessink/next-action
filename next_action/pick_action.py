from typing import Optional, Iterable

from .todotxt import Task


def next_action_based_on_priority(tasks: Iterable[Task]) -> Optional[Task]:
    """ Return the next action from the collection of tasks. """
    uncompleted_tasks = [task for task in tasks if not task.is_completed()]
    sorted_tasks = sorted(uncompleted_tasks, key=lambda task: task.priority() or "ZZZ")
    return sorted_tasks[0] if sorted_tasks else None
