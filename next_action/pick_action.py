""" Algorithm for deciding the next action(s). """

import argparse
import datetime
from typing import Tuple

from .todotxt import Task, Tasks


def sort_key(task: Task) -> Tuple[str, datetime.date, datetime.date, int]:
    """ Return the sort key for a task. """
    return (task.priority() or "ZZZ", task.due_date() or datetime.date.max, task.creation_date() or datetime.date.max,
            -len(task.projects()))


def next_actions(tasks: Tasks, arguments: argparse.Namespace) -> Tasks:
    """ Return the next action(s) from the collection of tasks. """
    contexts = arguments.contexts
    projects = arguments.projects
    excluded_contexts = arguments.excluded_contexts
    excluded_projects = arguments.excluded_projects
    # First, get the potential next actions by filtering out completed tasks and tasks with a future creation date or
    # future threshold date
    eligible_tasks = filter(Task.is_actionable, tasks)
    # Then, exclude tasks that have an excluded context
    if excluded_contexts:
        eligible_tasks = filter(lambda task: not excluded_contexts & task.contexts(), eligible_tasks)
    # And, tasks that have an excluded project
    if excluded_projects:
        eligible_tasks = filter(lambda task: not excluded_projects & task.projects(), eligible_tasks)
    # Then, select the tasks that belong to all given contexts, if any
    if contexts:
        eligible_tasks = filter(lambda task: contexts <= task.contexts(), eligible_tasks)
    # Next, select the tasks that belong to at least one of the given projects, if any
    if projects:
        eligible_tasks = filter(lambda task: projects & task.projects(), eligible_tasks)
    # If the user only wants to see overdue tasks, filter out non-overdue tasks
    if arguments.overdue:
        eligible_tasks = filter(Task.is_overdue, eligible_tasks)
    # If the user only wants to see tasks due before a due date, filter out non-due tasks
    if arguments.due:
        eligible_tasks = filter(lambda task: task.is_due(arguments.due), eligible_tasks)
    # If the user specified a minimum priority, filter out tasks with a lower priority or no priority
    eligible_tasks = filter(lambda task: task.priority_at_least(arguments.priority), eligible_tasks)
    # Remove blocked tasks
    eligible_tasks = filter(lambda task: not task.is_blocked(tasks), eligible_tasks)
    # Finally, sort by priority, due date and creation date
    return Tasks(sorted(eligible_tasks, key=sort_key)[:arguments.number])
