""" Algorithm for deciding the next action(s). """

from typing import Set, Sequence

from .todotxt import Task


def next_actions(tasks: Sequence[Task], contexts: Set[str] = None, projects: Set[str] = None) -> Sequence[Task]:
    """ Return the next action(s) from the collection of tasks. """
    uncompleted_tasks = [task for task in tasks if not task.is_completed()]
    tasks_in_context = filter(lambda task: contexts <= task.contexts() if contexts else True, uncompleted_tasks)
    tasks_in_project = filter(lambda task: projects & task.projects() if projects else True, tasks_in_context)
    return sorted(tasks_in_project, key=lambda task: task.priority() or "ZZZ")
