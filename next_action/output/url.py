"""Module for opening urls."""

import webbrowser

from .. import todotxt


def open_urls(tasks: todotxt.Tasks):
    """Open the urls of the tasks."""
    for task in tasks:
        for url in task.urls():
            webbrowser.open(url)
