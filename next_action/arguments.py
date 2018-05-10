import argparse
import os
import shutil

import next_action


class ContextAction(argparse.Action):
    """ A context action that checks whether contexts start with an @. """
    def __call__(self, parser, namespace, values, option_string=None):
        if not values:
            return
        if values.startswith("@"):
            setattr(namespace, self.dest, values)
        else:
            parser.error("Contexts should start with an @.")


def parse_arguments() -> argparse.Namespace:
    """ Parse the command line arguments. """
    # Ensure that the help info is printed using all columns available
    os.environ['COLUMNS'] = str(shutil.get_terminal_size().columns)

    parser = argparse.ArgumentParser(description="Show the next action in your todo.txt",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--version", action="version", version="Next-action {0}".format(next_action.__version__))
    parser.add_argument("-f", "--file", help="filename of the todo.txt file to read",
                        type=str, default="todo.txt")
    parser.add_argument("context", metavar="@CONTEXT", help="Show the next action in the specified context", nargs="?",
                        type=str, action=ContextAction)
    return parser.parse_args()
