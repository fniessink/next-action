"""Unit tests for the url module in the output package."""

import unittest
from unittest.mock import patch

from next_action import todotxt
from next_action.output import open_urls


class TestOpenUrls(unittest.TestCase):
    """Unit tests for the open urls function."""

    def test_url(self):
        with patch("webbrowser.open") as mock_open:
            open_urls([todotxt.Task("https://google.com")])
        mock_open.assert_called_once_with("https://google.com")
