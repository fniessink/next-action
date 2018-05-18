""" Package for dealing with the todo.txt format. """

from typing import IO, List

from .task import Task


def read_todotxt_file(todoxt_file: IO[str]) -> List[Task]:
    """ Read tasks from a Todo.txt file. """
    with todoxt_file:
        return [Task(line.strip()) for line in todoxt_file if line.strip()]
