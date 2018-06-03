""" Unit tests for the reference module in the output package. """

import unittest

from next_action import todotxt
from next_action.output import reference


class ReferenceTest(unittest.TestCase):
    """ Unit tests for the reference method. """
    def test_reference(self):
        """ Test that the source filename is added. """
        self.assertEqual("Todo [todo.txt]", reference(todotxt.Task("Todo", "todo.txt")))
