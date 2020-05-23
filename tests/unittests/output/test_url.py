"""Unit tests for the url module in the output package."""

import unittest
from unittest.mock import call, patch

from next_action import todotxt
from next_action.output import open_urls


@patch("webbrowser.open")
class TestOpenUrls(unittest.TestCase):
    """Unit tests for the open urls function."""

    def setUp(self):
        """Set up a task with one url."""
        self.url = "https://google.com"
        self.task = todotxt.Task(self.url)

    def test_url(self, mock_open):
        """Test that URLs can be opened."""
        open_urls([self.task])
        mock_open.assert_called_once_with(self.url)

    def test_multiple_urls(self, mock_open):
        """Test that multiple URLs can be opened."""
        open_urls([self.task, self.task])
        mock_open.assert_has_calls([call(self.url), call(self.url)])

    def test_multiple_urls_in_one_task(self, mock_open):
        """Test that multiple URLs in one task can be opened."""
        self.task.text += f" {self.url}"
        open_urls([self.task])
        mock_open.assert_has_calls([call(self.url), call(self.url)])
