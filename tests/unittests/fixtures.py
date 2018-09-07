"""Fixtures for unit tests."""

import argparse
import unittest
import sys


class TestCaseWithNamespace(unittest.TestCase):
    """Test case for unit tests that need a argparse.Namespace."""

    def setUp(self):
        """Set up the namespace with default arguments for all unit tests."""
        self.namespace = argparse.Namespace()
        self.namespace.contexts = set()
        self.namespace.projects = set()
        self.namespace.excluded_contexts = set()
        self.namespace.excluded_projects = set()
        self.namespace.overdue = False
        self.namespace.due = None
        self.namespace.priority = None
        self.namespace.time_travel = None
        self.namespace.number = sys.maxsize
