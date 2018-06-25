""" Package for dealing with the todo.txt format. """

import fileinput
from typing import cast, List

from .task import Task
from .tasks import Tasks


def read_todotxt_files(filenames: List[str]) -> Tasks:
    """ Read tasks from the Todo.txt files. """
    tasks = Tasks()
    with cast(fileinput.FileInput, fileinput.input(filenames)) as todotxt_file:
        tasks.extend([Task(line.strip(), todotxt_file.filename(), tasks) for line in todotxt_file if line.strip()])
    return tasks
