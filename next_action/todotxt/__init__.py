"""Package for dealing with the todo.txt format."""

import fileinput
import os
from typing import cast, List, Sequence

from .task import Task
from .tasks import Tasks


def uncompleted_task_on(line: str) -> bool:
    """Return whether there's an uncompleted task on the line."""
    return bool(line.strip() and not line.startswith("x "))


def unblocked_tasks(tasks: Sequence[Task]) -> Sequence[Task]:
    """Set the blocked status of the tasks and return only the unblocked tasks."""
    task_by_id = {task.task_id(): task for task in tasks if task.task_id()}
    for task in tasks:
        for parent_id in task.parent_ids():
            parent_task = task_by_id.get(parent_id)
            if parent_task:
                parent_task.set_is_blocked()
                task.add_blocked_task(parent_task)
        for child_id in task.child_ids():
            child_task = task_by_id.get(child_id)
            if child_task:
                task.set_is_blocked()
                child_task.add_blocked_task(task)
    return [task for task in tasks if not task.is_blocked()]


def read_todotxt_files(filenames: List[str]) -> Tasks:
    """Read tasks from the Todo.txt files."""
    filenames = [os.path.expanduser(filename) for filename in filenames]
    with cast(fileinput.FileInput, fileinput.input(filenames)) as todotxt_file:
        tasks = [Task(line.strip(), todotxt_file.filename()) for line in todotxt_file if uncompleted_task_on(line)]
    return Tasks(unblocked_tasks(tasks))
