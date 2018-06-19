""" Class that represents one task (i.e. one line) from a todo.txt file. """

import datetime
import re
import typing
from typing import Iterable, Optional, Set


class Task(object):
    """ A task from a line in a todo.txt file. """

    iso_date_reg_exp = r"(\d{4})-(\d{1,2})-(\d{1,2})"

    def __init__(self, todo_txt: str, filename: str = "") -> None:
        self.text = todo_txt
        self.filename = filename

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

    def priority_at_least(self, min_priority: Optional[str]) -> bool:
        """ Return whether the priority of task is at least the given priority. """
        if not min_priority:
            return True
        priority = self.priority()
        if not priority:
            return False
        return priority <= min_priority

    def creation_date(self) -> Optional[datetime.date]:
        """ Return the creation date of the task. """
        match = re.match(r"(?:\([A-Z]\) )?{0}\b".format(self.iso_date_reg_exp), self.text)
        return self.__create_date(match)

    def threshold_date(self) -> Optional[datetime.date]:
        """ Return the threshold date of the task. """
        return self.__find_keyed_date("t")

    def due_date(self) -> Optional[datetime.date]:
        """ Return the due date of the task. """
        return self.__find_keyed_date("due")

    def is_due(self, due_date: datetime.date) -> bool:
        """ Return whether the task is due on or before the given due date. """
        task_due_date = self.due_date()
        return task_due_date <= due_date if task_due_date else False

    def is_completed(self) -> bool:
        """ Return whether the task is completed or not. """
        return self.text.startswith("x ")

    def is_future(self) -> bool:
        """ Return whether the task is a future task, i.e. has a creation or threshold date in the future. """
        today = datetime.date.today()
        creation_date = self.creation_date()
        if creation_date:
            return creation_date > today
        threshold_date = self.threshold_date()
        if threshold_date:
            return threshold_date > today
        return False

    def is_actionable(self) -> bool:
        """ Return whether the task is actionable, i.e. whether it's not completed and doesn't have a future creation
            date. """
        return not self.is_completed() and not self.is_future()

    def is_overdue(self) -> bool:
        """ Return whether the task is overdue, i.e. whether it has a due date in the past. """
        due_date = self.due_date()
        return due_date < datetime.date.today() if due_date else False

    def is_blocked(self, tasks: Iterable["Task"]) -> bool:
        """ Return whether a task is blocked, i.e. whether it has uncompleted child tasks. """
        return any([task for task in tasks if not task.is_completed() and
                    (self.task_id() in task.parent_ids() or task.task_id() in self.child_ids())])

    def child_ids(self) -> Set[str]:
        """ Return the ids of the child tasks. """
        return {match.group(1) for match in re.finditer(r"\bafter:(\S+)\b", self.text)}

    def parent_ids(self) -> Set[str]:
        """ Return the ids of the parent tasks. """
        return {match.group(2) for match in re.finditer(r"\b(p|before):(\S+)\b", self.text)}

    def task_id(self) -> str:
        """ Return the id of the task. """
        match = re.search(r"\bid:(\S+)\b", self.text)
        return match.group(1) if match else ""

    def __prefixed_items(self, prefix: str) -> Set[str]:
        """ Return the prefixed items in the task. """
        return {match.group(1) for match in re.finditer(" {0}([^ ]+)".format(prefix), self.text)}

    def __find_keyed_date(self, key: str) -> Optional[datetime.date]:
        """ Find a key:value pair with the supplied key where the value is a date. """
        match = re.search(r"\b{0}:{1}\b".format(key, self.iso_date_reg_exp), self.text)
        return self.__create_date(match)

    @staticmethod
    def __create_date(match: Optional[typing.Match[str]]) -> Optional[datetime.date]:
        """ Create a date from the match, if possible. """
        if match:
            try:
                return datetime.date(*(int(group) for group in match.groups()))
            except ValueError:
                pass
        return None
