"""Package for parsing command line arguments."""

import argparse
import os
import shutil
from typing import Tuple

from .parser import NextActionArgumentParser


def parse_arguments(version: str = "?") -> Tuple[argparse.ArgumentParser, argparse.Namespace]:
    """Build the argument parser and parse the command line arguments."""
    # Ensure that the help info is printed using all columns available
    os.environ['COLUMNS'] = str(shutil.get_terminal_size().columns)
    parser = NextActionArgumentParser(version)
    return parser, parser.parse_args()
