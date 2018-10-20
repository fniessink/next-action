"""Create a random todo.txt file for testing purposes."""

import random
import string


def random_bool():
    """Random True/False choice."""
    return random.choice([True, False])  # nosec


def random_string():
    """Return a random string."""
    return random.choice(string.ascii_lowercase)  # nosec


def context():
    """Return a random context."""
    return " @" + random_string() if random_bool() else ""


def project():
    """Return a random project."""
    return " +" + random_string() if random_bool() else ""


def prio():
    """Return a random priority."""
    return f"({random.choice(string.ascii_uppercase)}) " if random_bool() else ""  # nosec


def due_date():
    """Return a random due date."""
    return f" due:2018-{random.randint(1, 12)}-1" if random_bool() else ""  # nosec


def task_id(index):
    """Return a task identifier for 50% of the tasks."""
    return f" id:task{index}" if random_bool() else ""


def create_random_todo_txt():
    """Create a Todo.txt file with random tasks."""
    ids = []
    with open("todo.txt", "w") as todo_txt:
        for i in range(10000):
            before = after = ""
            if len(ids) > 3:
                sample = random.sample(ids, 3)
                while sample and random_bool() and random_bool():
                    before += f" before:task{sample.pop()}" if random_bool() else ""
            id_ = task_id(i)
            todo_txt.write(f"{prio()}Task {i}{id_}{due_date()}{before}{after}{context()}{project()}\n")
            if id_:
                ids.append(i)


if __name__ == "__main__":
    create_random_todo_txt()
