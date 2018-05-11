""" Algorithm for deciding the next action. """

from typing import Optional, Sequence

from .todotxt import Task


def next_action_based_on_priority(tasks: Sequence[Task], context: str = "", project: str = "") -> Optional[Task]:
    """ Return the next action from the collection of tasks. """
    context = context.strip("@")
    project = project.strip("+")
    uncompleted_tasks = [task for task in tasks if not task.is_completed()]
    tasks_in_context = filter(lambda task: context in task.contexts() if context else True, uncompleted_tasks)
    tasks_in_project = filter(lambda task: project in task.projects() if project else True, tasks_in_context)
    sorted_tasks = sorted(tasks_in_project, key=lambda task: task.priority() or "ZZZ")
    return sorted_tasks[0] if sorted_tasks else None
