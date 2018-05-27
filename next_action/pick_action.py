""" Algorithm for deciding the next action(s). """

import argparse
import datetime
from typing import List, Sequence, Set, Tuple

from .todotxt import Task


def sort_key(task: Task) -> Tuple[str, datetime.date, datetime.date, int]:
    """ Return the sort key for a task. """
    return (task.priority() or "ZZZ", task.due_date() or datetime.date.max, task.creation_date() or datetime.date.max,
            -len(task.projects()))


def subset(filters: List[str], prefix: str) -> Set[str]:
    """ Return a subset of the filters based on prefix. """
    return set([f.strip(prefix) for f in filters if f.startswith(prefix)])


def next_actions(tasks: Sequence[Task], arguments: argparse.Namespace) -> Sequence[Task]:
    """ Return the next action(s) from the collection of tasks. """
    contexts = subset(arguments.filters, "@")
    projects = subset(arguments.filters, "+")
    excluded_contexts = subset(arguments.filters, "-@")
    excluded_projects = subset(arguments.filters, "-+")
    # First, get the potential next actions by filtering out completed tasks and tasks with a future creation date
    actionable_tasks = [task for task in tasks if task.is_actionable()]
    # Then, exclude tasks that have an excluded context
    eligible_tasks = filter(lambda task: not excluded_contexts & task.contexts() if excluded_contexts else True,
                            actionable_tasks)
    # And, tasks that have an excluded project
    eligible_tasks = filter(lambda task: not excluded_projects & task.projects() if excluded_projects else True,
                            eligible_tasks)
    # Then, select the tasks that belong to all given contexts, if any
    tasks_in_context = filter(lambda task: contexts <= task.contexts() if contexts else True, eligible_tasks)
    # Next, select the tasks that belong to at least one of the given projects, if any
    tasks_in_project = filter(lambda task: projects & task.projects() if projects else True, tasks_in_context)
    # If the user only wants to see overdue tasks, filter out non-overdue tasks
    tasks_in_project = filter(lambda task: task.is_overdue() if arguments.overdue else True, tasks_in_project)
    # Finally, sort by priority, due date and creation date
    return sorted(tasks_in_project, key=sort_key)
