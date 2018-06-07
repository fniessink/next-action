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
    # First, get the potential next actions by filtering out completed tasks and tasks with a future creation date or
    # future threshold date
    actionable_tasks = [task for task in tasks if task.is_actionable()]
    # Then, exclude tasks that have an excluded context
    eligible_tasks = filter(lambda task: not excluded_contexts & task.contexts() if excluded_contexts else True,
                            actionable_tasks)
    # And, tasks that have an excluded project
    eligible_tasks = filter(lambda task: not excluded_projects & task.projects() if excluded_projects else True,
                            eligible_tasks)
    # Then, select the tasks that belong to all given contexts, if any
    eligible_tasks = filter(lambda task: contexts <= task.contexts() if contexts else True, eligible_tasks)
    # Next, select the tasks that belong to at least one of the given projects, if any
    eligible_tasks = filter(lambda task: projects & task.projects() if projects else True, eligible_tasks)
    # If the user only wants to see overdue tasks, filter out non-overdue tasks
    eligible_tasks = filter(lambda task: task.is_overdue() if arguments.overdue else True, eligible_tasks)
    # If the user only wants to see tasks due before a due date, filter out non-due tasks
    eligible_tasks = filter(lambda task: task.is_due(arguments.due) if arguments.due else True, eligible_tasks)
    # If the user specified a minimum priority, filter out tasks with a lower priority or no priority
    eligible_tasks = filter(lambda task: task.priority_at_least(arguments.priority), eligible_tasks)
    # Finally, sort by priority, due date and creation date
    return sorted(eligible_tasks, key=sort_key)
