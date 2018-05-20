""" Unit tests for the argument data class. """

import unittest
from unittest.mock import Mock

from next_action.arguments import Arguments


class FilenameArgumentsTest(unittest.TestCase):
    """ Unit tests for the filename field of the arguments data class. """

    def test_default_filenames(self):
        """ Test that the default file name is returned when no filenames are set. """
        self.assertEqual(["todo.txt"], Arguments(Mock(), ["todo.txt"]).filenames)

    def test_set_filenames(self):
        """ Test that the set file names are returned when filenames are set. """
        arguments = Arguments(Mock(), ["todo.txt"])
        arguments.filenames = ["foo.txt"]
        self.assertEqual(["foo.txt"], arguments.filenames)

    def test_remove_default(self):
        """ Test that the default filename is removed when it is the filenames. """
        arguments = Arguments(Mock(), ["todo.txt"])
        arguments.filenames = ["todo.txt", "foo.txt"]
        self.assertEqual(["foo.txt"], arguments.filenames)

    def test_remove_default_once(self):
        """ Test that the default filename is removed when it is the filenames, but only one time. """
        arguments = Arguments(Mock(), ["todo.txt"])
        arguments.filenames = ["todo.txt", "todo.txt", "foo.txt"]
        self.assertEqual(["todo.txt", "foo.txt"], arguments.filenames)
