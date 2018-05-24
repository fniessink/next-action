""" Package for parsing command line arguments. """

import argparse
import os
import shutil
from typing import Tuple

from .arguments import Arguments
from .parser import NextActionArgumentParser


def parse_arguments() -> Tuple[argparse.ArgumentParser, Arguments]:
    """ Build the argument parser, parse the command line arguments, and post-process them. """
    # Ensure that the help info is printed using all columns available
    os.environ['COLUMNS'] = str(shutil.get_terminal_size().columns)
    default_filenames = ["~/todo.txt"]
    parser = NextActionArgumentParser(default_filenames)
    arguments = Arguments(default_filenames)
    namespace = parser.parse_args()
    arguments.filenames = namespace.file
    arguments.number = namespace.number
    arguments.show_all(namespace.all)
    arguments.overdue = namespace.overdue
    arguments.filters = namespace.filters
    return parser, arguments
