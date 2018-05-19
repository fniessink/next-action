""" Package for parsing command line arguments. """

import argparse
import os
import shutil
import sys
from typing import cast, Dict, List, Set, Tuple

from .arguments import Arguments
from .parser import build_parser, parse_remaining_args


def parse_arguments() -> Arguments:
    """ Build the argument parser, paerse the command line arguments, and post-process them. """
    # Ensure that the help info is printed using all columns available
    os.environ['COLUMNS'] = str(shutil.get_terminal_size().columns)
    default_filenames = ["~/todo.txt"]
    parser = build_parser(default_filenames)
    arguments = Arguments(parser, default_filenames)
    namespace, remaining = parser.parse_known_args()
    parse_remaining_args(parser, remaining, namespace)
    arguments.filenames = namespace.filenames
    arguments.number = namespace.number
    arguments.show_all(namespace.all)
    arguments.filters = namespace.filters
    return arguments
