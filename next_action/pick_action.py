""" Algorithm for deciding the next action(s). """

from typing import Set, Sequence

from .todotxt import Task


def next_actions(tasks: Sequence[Task], contexts: Set[str] = None, projects: Set[str] = None) -> Sequence[Task]:
    """ Return the next action(s) from the collection of tasks. """
    # First, get the potential next actions by filtering out completed tasks and tasks with a future creation date
    actionable_tasks = [task for task in tasks if not task.is_completed() and not task.is_future()]
    # Then, select the tasks that belong to all given contexts, if any
    tasks_in_context = filter(lambda task: contexts <= task.contexts() if contexts else True, actionable_tasks)
    # Next, select the tasks that belong to at least one of the given projects, if any
    tasks_in_project = filter(lambda task: projects & task.projects() if projects else True, tasks_in_context)
    # Finally, sort by priority
    return sorted(tasks_in_project, key=lambda task: task.priority() or "ZZZ")
