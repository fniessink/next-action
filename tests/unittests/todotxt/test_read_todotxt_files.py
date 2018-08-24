"""Unit tests for the read todo.txt files method."""

import unittest
from unittest.mock import patch, mock_open

from next_action.todotxt import read_todotxt_files


class ReadTodoTxtFilesTest(unittest.TestCase):
    """Unit tests for the read todo.txt files method."""

    @patch("fileinput.open", mock_open(read_data="\nWalk the dog\nx (B) Call mom\n"))
    def test_skip_completed_tasks(self):
        """Test that completed tasks are skipped."""
        tasks = read_todotxt_files("todo.txt")
        self.assertEqual(1, len(tasks))
        self.assertEqual("Walk the dog", tasks[0].text)  # pylint: disable=unsubscriptable-object

    @patch("fileinput.open", mock_open(read_data="\nWalk the dog\n   \n\n"))
    def test_skip_empty_lines(self):
        """Test that empty lines are skipped."""
        tasks = read_todotxt_files("todo.txt")
        self.assertEqual(1, len(tasks))
        self.assertEqual("Walk the dog", tasks[0].text)  # pylint: disable=unsubscriptable-object
