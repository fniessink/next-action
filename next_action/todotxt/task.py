""" Class that represents one task (i.e. one line) from a todo.txt file. """

import datetime
import re
import typing
from typing import Optional, Set


class Task(object):
    """ A task from a line in a todo.txt file. """

    iso_date_reg_exp = r"(\d{4})-(\d{1,2})-(\d{1,2})"

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
        match = re.match(r"(?:\([A-Z]\) )?{0}\b".format(self.iso_date_reg_exp), self.text)
        return self.__create_date(match)

    def due_date(self) -> Optional[datetime.date]:
        """ Return the due date of the task. """
        match = re.search(r"\bdue:{0}\b".format(self.iso_date_reg_exp), self.text)
        return self.__create_date(match)

    def is_completed(self) -> bool:
        """ Return whether the task is completed or not. """
        return self.text.startswith("x ")

    def is_future(self) -> bool:
        """ Return whether the task is a future task, i.e. has a creation date in the future. """
        creation_date = self.creation_date()
        return creation_date > datetime.date.today() if creation_date else False

    def is_actionable(self) -> bool:
        """ Return whether the task is actionable, i.e. whether it's not completed and doesn't have a future creation
            date. """
        return not self.is_completed() and not self.is_future()

    def __prefixed_items(self, prefix: str) -> Set[str]:
        """ Return the prefixed items in the task. """
        return {match.group(1) for match in re.finditer(" {0}([^ ]+)".format(prefix), self.text)}

    @staticmethod
    def __create_date(match: Optional[typing.Match[str]]) -> Optional[datetime.date]:
        """ Create a date from the match, if possible. """
        if match:
            try:
                return datetime.date(*(int(group) for group in match.groups()))
            except ValueError:
                pass
        return None
