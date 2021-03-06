"""Unit tests for the read todo.txt files method."""

import unittest
from unittest.mock import patch, mock_open

from next_action.todotxt import read_todotxt_files


class ReadTodoTxtFilesTest(unittest.TestCase):
    """Unit tests for the read todo.txt files method."""

    def setUp(self):
        """Set up filenames."""
        self.filename = "todo.txt"
        self.files = [self.filename]

    # pylint: disable=unsubscriptable-object

    @patch("fileinput.open", mock_open(read_data="\nWalk the dog\nx (B) Call mom\n"))
    def test_skip_completed_tasks(self):
        """Test that completed tasks are skipped."""
        tasks = read_todotxt_files(self.files)
        self.assertEqual(1, len(tasks))
        self.assertEqual("Walk the dog", tasks[0].text)
        self.assertEqual(self.filename, tasks[0].filename)
        self.assertEqual(2, tasks[0].line_number)

    @patch("fileinput.open", mock_open(read_data="\nWalk the dog\n   \n\n"))
    def test_skip_empty_lines(self):
        """Test that empty lines are skipped."""
        tasks = read_todotxt_files(self.files)
        self.assertEqual(1, len(tasks))
        self.assertEqual("Walk the dog", tasks[0].text)
        self.assertEqual(2, tasks[0].line_number)

    @patch("fileinput.open", mock_open(read_data="\nBlocked id:1\nBlocking before:1\n"))
    def test_skip_blocked_before(self):
        """Test that tasks blocked with before are skipped."""
        tasks = read_todotxt_files(self.files)
        self.assertEqual(1, len(tasks))
        self.assertEqual("Blocking before:1", tasks[0].text)
        self.assertEqual(3, tasks[0].line_number)

    @patch("fileinput.open", mock_open(read_data="\nBlocking id:1\nBlocked after:1\n"))
    def test_skip_blocked_after(self):
        """Test that tasks blocked with after are skipped."""
        tasks = read_todotxt_files(self.files)
        self.assertEqual(1, len(tasks))
        self.assertEqual("Blocking id:1", tasks[0].text)

    @patch("fileinput.open", mock_open(read_data="Blocking before:1\n"))
    def test_missing_before_task(self):
        """Test a missing blocked task."""
        tasks = read_todotxt_files(self.files)
        self.assertEqual(1, len(tasks))
        self.assertEqual("Blocking before:1", tasks[0].text)

    @patch("fileinput.open", mock_open(read_data="Blocked after:1\n"))
    def test_missing_after_task(self):
        """Test a missing blocked task."""
        tasks = read_todotxt_files(self.files)
        self.assertEqual(1, len(tasks))
        self.assertEqual("Blocked after:1", tasks[0].text)
