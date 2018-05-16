""" Package for parsing command line arguments. """

import argparse
import os
import shutil
import sys

from .parser import build_parser, parse_remaining_args


def parse_arguments() -> argparse.Namespace:
    """ Build the argument parser, paerse the command line arguments, and post-process them. """
    # Ensure that the help info is printed using all columns available
    os.environ['COLUMNS'] = str(shutil.get_terminal_size().columns)
    default_filenames = ["todo.txt"]
    parser = build_parser(default_filenames)
    namespace, remaining = parser.parse_known_args()
    namespace.excluded_contexts, namespace.excluded_projects = parse_remaining_args(
        parser, remaining, namespace.contexts, namespace.projects)
    # Work around the issue that the "append" action doesn't overwrite defaults.
    # See https://bugs.python.org/issue16399.
    if default_filenames != namespace.filenames:
        for default_filename in default_filenames:
            namespace.filenames.remove(default_filename)
    # Remove duplicate filenames while maintaining order.
    namespace.filenames = list(dict.fromkeys(namespace.filenames))
    # If the user wants to see all next actions, set the number to something big.
    if namespace.all:
        namespace.number = sys.maxsize
    return namespace
