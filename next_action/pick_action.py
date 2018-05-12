""" Algorithm for deciding the next action. """

from typing import Optional, Set, Sequence

from .todotxt import Task


def next_action_based_on_priority(tasks: Sequence[Task], contexts: Set[str] = None,
                                  projects: Set[str] = None) -> Optional[Task]:
    """ Return the next action from the collection of tasks. """
    contexts = contexts or set()
    projects = projects or set()
    uncompleted_tasks = [task for task in tasks if not task.is_completed()]
    tasks_in_context = filter(lambda task: contexts <= task.contexts(), uncompleted_tasks)
    tasks_in_project = filter(lambda task: projects & task.projects() if projects else True, tasks_in_context)
    sorted_tasks = sorted(tasks_in_project, key=lambda task: task.priority() or "ZZZ")
    return sorted_tasks[0] if sorted_tasks else None
