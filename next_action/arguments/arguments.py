""" Argument data class for transfering command line arguments. """

import argparse
import os.path
import sys
from typing import List, Set


class Arguments(object):
    """ Argument data class. """
    def __init__(self, parser: argparse.ArgumentParser, default_filenames: List[str]) -> None:
        self.parser = parser
        self.__default_filenames = default_filenames
        self.__filenames: List[str] = []
        self.__filters: List[Set[str]] = []
        self.number = 1

    @property
    def filenames(self) -> List[str]:
        """ Return the filenames. """
        return self.__filenames or self.__default_filenames

    @filenames.setter
    def filenames(self, filenames: List[str]) -> None:
        """ Set the filenames. """
        # Work around the issue that the "append" action doesn't overwrite defaults.
        # See https://bugs.python.org/issue16399.
        if self.__default_filenames != filenames:
            for default_filename in self.__default_filenames:
                if default_filename in filenames:
                    filenames.remove(default_filename)
        # Remove duplicate filenames while maintaining order.
        self.__filenames = [os.path.expanduser(filename) for filename in list(dict.fromkeys(filenames))]

    def show_all(self, show_all: bool) -> None:
        """ If the user wants to see all next actions, set the number to something big. """
        if show_all:
            self.number = sys.maxsize

    @property
    def filters(self) -> List[Set[str]]:
        """ Return the filters: contexts, projects, excluded_contexts, excluded_projects. """
        return self.__filters

    @filters.setter
    def filters(self, filters: List[str]) -> None:
        """ Process the context and projects into separate filters. """

        def subset(filters: List[str], prefix: str) -> Set[str]:
            """ Return a subset of the filters based on prefix. """
            return set([f.strip(prefix) for f in filters if f.startswith(prefix)])

        self.__filters = [subset(filters, prefix) for prefix in ("@", "+", "-@", "-+")]
