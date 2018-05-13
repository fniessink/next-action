""" Class that represents one task (i.e. one line) from a todo.txt file. """

import datetime
import re
from typing import Optional, Set


class Task(object):
    """ A task from a line in a todo.txt file. """
    def __init__(self, todo_txt: str) -> None:
        self.text = todo_txt

    def __repr__(self) -> str:
        return "{0}<{1}>".format(self.__class__.__name__, self.text)

    def contexts(self) -> Set[str]:
        """ Return the contexts of the task. """
        return self.__prefixed_items("@")

    def projects(self) -> Set[str]:
        """ Return the projects of the task. """
        return self.__prefixed_items(r"\+")

    def priority(self) -> Optional[str]:
        """ Return the priority of the task """
        match = re.match(r"\(([A-Z])\) ", self.text)
        return match.group(1) if match else None

    def creation_date(self) -> Optional[datetime.date]:
        """ Return the creation date of the task. """
        match = re.match(r"(?:\([A-Z]\) )?(\d{4})-(\d{1,2})-(\d{1,2})", self.text)
        if match:
            try:
                return datetime.date(*(int(group) for group in match.groups()))
            except ValueError:
                pass
        return None

    def is_completed(self) -> bool:
        """ Return whether the task is completed or not. """
        return self.text.startswith("x ")

    def is_future(self) -> bool:
        """ Return whether the task is a future task, i.e. has a creation date in the future. """
        creation_date = self.creation_date()
        return creation_date > datetime.date.today() if creation_date else False

    def __prefixed_items(self, prefix: str) -> Set[str]:
        """ Return the prefixed items in the task. """
        return {match.group(1) for match in re.finditer(" {0}([^ ]+)".format(prefix), self.text)}
