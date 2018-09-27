"""Class that represents one task (i.e. one line) from a todo.txt file."""

import datetime
import functools
import re
import typing
from typing import List, Optional, Sequence, Set


class Task:
    """A task from a line in a todo.txt file."""

    iso_date_reg_exp = r"(\d{4})-(\d{1,2})-(\d{1,2})"

    def __init__(self, todo_txt: str, filename: str = "") -> None:
        """Initialise the task with its Todo.txt text string and originating filename."""
        self.text = todo_txt
        self.filename = filename
        self.__is_blocked = False
        self.__blocked_tasks: List["Task"] = []

    def __repr__(self) -> str:
        """Return a text representation of the task."""
        return f"{self.__class__.__name__}<{self.text}>"

    @functools.lru_cache(maxsize=None)
    def contexts(self) -> Set[str]:
        """Return the contexts of the task."""
        return self.__prefixed_items("@")

    @functools.lru_cache(maxsize=None)
    def projects(self) -> Set[str]:
        """Return the projects of the task."""
        return self.__prefixed_items(r"\+")

    @functools.lru_cache(maxsize=None)
    def priority(self) -> Optional[str]:
        """Return the priority of the task."""
        match = re.match(r"\(([A-Z])\) ", self.text)
        priorities: List[Optional[str]] = [match.group(1)] if match else []
        priorities.extend([blocked_task.priority() for blocked_task in self.blocked_tasks()])
        return min(priorities, default=None, key=lambda priority: priority or "ZZZ")

    def priority_at_least(self, min_priority: str) -> bool:
        """Return whether the priority of task is at least the given priority."""
        priority = self.priority()
        if priority:
            return priority <= min_priority
        return False

    @functools.lru_cache(maxsize=None)
    def creation_date(self) -> Optional[datetime.date]:
        """Return the creation date of the task."""
        match = re.match(fr"(?:\([A-Z]\) )?{self.iso_date_reg_exp}\b", self.text)
        return self.__create_date(match)

    @functools.lru_cache(maxsize=None)
    def threshold_date(self) -> Optional[datetime.date]:
        """Return the threshold date of the task."""
        return self.__find_keyed_date("t")

    @functools.lru_cache(maxsize=None)
    def due_date(self) -> Optional[datetime.date]:
        """Return the due date of the task."""
        due_dates = [self.__find_keyed_date("due")]
        due_dates.extend([blocked_task.due_date() for blocked_task in self.blocked_tasks()])
        return min(due_dates, default=None, key=lambda due_date: due_date or datetime.date.max)

    def is_due(self, due_date: datetime.date) -> bool:
        """Return whether the task is due on or before the given due date."""
        task_due_date = self.due_date()
        return task_due_date <= due_date if task_due_date else False

    def is_future(self, today: datetime.date = None) -> bool:
        """Return whether the task is a future task, i.e. has a creation or threshold date in the future."""
        today = today or datetime.date.today()
        creation_date = self.creation_date()
        if creation_date:
            return creation_date > today
        threshold_date = self.threshold_date()
        if threshold_date:
            return threshold_date > today
        return False

    def is_overdue(self, today: datetime.date = None) -> bool:
        """Return whether the task is overdue, i.e. whether it has a due date in the past."""
        today = today or datetime.date.today()
        due_date = self.due_date()
        return due_date < today if due_date else False

    def is_blocked(self) -> bool:
        """Return whether a task is blocked, i.e. whether it has (uncompleted) child tasks."""
        return self.__is_blocked

    def set_is_blocked(self) -> None:
        """Set the blocked status."""
        self.__is_blocked = True

    def blocked_tasks(self) -> Sequence["Task"]:
        """Return the tasks this task is blocking."""
        return self.__blocked_tasks

    def add_blocked_task(self, task: "Task") -> None:
        """Add the task to the blocked tasks."""
        self.__blocked_tasks.append(task)

    @functools.lru_cache(maxsize=None)
    def child_ids(self) -> Set[str]:
        """Return the ids of the child tasks."""
        return {match.group(1) for match in re.finditer(r"\bafter:(\S+)\b", self.text)}

    @functools.lru_cache(maxsize=None)
    def parent_ids(self) -> Set[str]:
        """Return the ids of the parent tasks."""
        return {match.group(2) for match in re.finditer(r"\b(p|before):(\S+)\b", self.text)}

    @functools.lru_cache(maxsize=None)
    def task_id(self) -> str:
        """Return the id of the task."""
        match = re.search(r"\bid:(\S+)\b", self.text)
        return match.group(1) if match else ""

    def __prefixed_items(self, prefix: str) -> Set[str]:
        """Return the prefixed items in the task."""
        return {match.group(2) for match in re.finditer(fr"(^|\W){prefix}(\w+)", self.text)}

    def __find_keyed_date(self, key: str) -> Optional[datetime.date]:
        """Find a key:value pair with the supplied key where the value is a date."""
        match = re.search(fr"\b{key}:{self.iso_date_reg_exp}\b", self.text)
        return self.__create_date(match)

    @staticmethod
    def __create_date(match: Optional[typing.Match[str]]) -> Optional[datetime.date]:
        """Create a date from the match, if possible."""
        if match:
            try:
                return datetime.date(*(int(group) for group in match.groups()))
            except ValueError:
                pass
        return None
