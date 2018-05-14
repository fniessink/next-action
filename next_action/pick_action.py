""" Algorithm for deciding the next action(s). """

import datetime
from typing import Set, Sequence, Tuple

from .todotxt import Task


def sort_key(task: Task) -> Tuple[str, datetime.date]:
    """ Return the sort key for a task. """
    return (task.priority() or "ZZZ", task.due_date() or datetime.date.max, task.creation_date() or datetime.date.max)


def next_actions(tasks: Sequence[Task], contexts: Set[str] = None, projects: Set[str] = None,
                 excluded_contexts: Set[str] = None) -> Sequence[Task]:
    """ Return the next action(s) from the collection of tasks. """
    # First, get the potential next actions by filtering out completed tasks and tasks with a future creation date
    actionable_tasks = [task for task in tasks if task.is_actionable()]
    # Then, exclude tasks that have an excluded context
    eligible_tasks = filter(lambda task: not excluded_contexts & task.contexts() if excluded_contexts else True,
                            actionable_tasks)
    # Then, select the tasks that belong to all given contexts, if any
    tasks_in_context = filter(lambda task: contexts <= task.contexts() if contexts else True, eligible_tasks)
    # Next, select the tasks that belong to at least one of the given projects, if any
    tasks_in_project = filter(lambda task: projects & task.projects() if projects else True, tasks_in_context)
    # Finally, sort by priority, due date and creation date
    return sorted(tasks_in_project, key=sort_key)
