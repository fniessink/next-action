from typing import Optional, Iterable

from .todotxt import Task


def next_action_based_on_priority(tasks: Iterable[Task], context: str = "") -> Optional[Task]:
    """ Return the next action from the collection of tasks. """
    uncompleted_tasks = [task for task in tasks if not task.is_completed()]
    if context:
        tasks_in_context = [task for task in tasks if context.strip("@") in task.contexts()]
    else:
        tasks_in_context = uncompleted_tasks
    sorted_tasks = sorted(tasks_in_context, key=lambda task: task.priority() or "ZZZ")
    return sorted_tasks[0] if sorted_tasks else None
