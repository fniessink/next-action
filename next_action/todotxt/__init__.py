"""Package for dealing with the todo.txt format."""

import fileinput
from typing import cast, List

from .task import Task
from .tasks import Tasks


def read_todotxt_files(filenames: List[str]) -> Tasks:
    """Read tasks from the Todo.txt files."""
    tasks = Tasks()
    with cast(fileinput.FileInput, fileinput.input(filenames)) as todotxt_file:
        lines = [(line.strip(), todotxt_file.filename()) for line in todotxt_file if line.strip()]
        tasks.extend([Task(line, filename, tasks) for line, filename in lines])  # pylint: disable=no-member
    return tasks
