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
        match = re.match(r"(?:\([A-Z]\) )?(\d\d\d\d)-(\d\d)-(\d\d)", self.text)
        if match:
            try:
                return datetime.date(*(int(group) for group in match.groups()))
            except ValueError:
                pass
        return None

    def is_completed(self) -> bool:
        """ Return whether the task is completed or not. """
        return self.text.startswith("x ")

    def __prefixed_items(self, prefix: str) -> Set[str]:
        """ Return the prefixed items in the task. """
        return {match.group(1) for match in re.finditer(" {0}([^ ]+)".format(prefix), self.text)}
