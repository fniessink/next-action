""" Package for parsing command line arguments. """

import argparse
import os
import shutil
import sys
from typing import Dict, List, Set

from .parser import build_parser, parse_remaining_args


class Arguments(object):
    """ Argument data class. """
    def __init__(self, default_filenames: List[str]) -> None:
        self.__default_filenames = default_filenames
        self.__filenames: List[str] = []
        self.number = 1
        self.filters: List[str] = []

    @property
    def filenames(self) -> List[str]:
        """ Return the filenames. """
        return self.__filenames

    @filenames.setter
    def filenames(self, filenames: List[str]) -> None:
        """ Set the filenames. """
        # Work around the issue that the "append" action doesn't overwrite defaults.
        # See https://bugs.python.org/issue16399.
        if self.__default_filenames != filenames:
            for default_filename in self.__default_filenames:
                filenames.remove(default_filename)
        # Remove duplicate filenames while maintaining order.
        self.__filenames = list(dict.fromkeys(filenames))

    def show_all(self, show_all: bool) -> None:
        """ If the user wants to see all next actions, set the number to something big. """
        if show_all:
            self.number = sys.maxsize


def parse_arguments() -> Arguments:
    """ Build the argument parser, paerse the command line arguments, and post-process them. """
    # Ensure that the help info is printed using all columns available
    os.environ['COLUMNS'] = str(shutil.get_terminal_size().columns)
    default_filenames = ["todo.txt"]
    arguments = Arguments(default_filenames)
    parser = build_parser(default_filenames)
    namespace, remaining = parser.parse_known_args()
    parse_remaining_args(parser, remaining, namespace)
    arguments.filenames = namespace.filenames
    arguments.number = namespace.number
    arguments.show_all(namespace.all)
    arguments.filters = getattr(namespace, "filters", [])
    return arguments
