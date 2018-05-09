import argparse


def parse_arguments() -> argparse.Namespace:
    """ Parse the command line arguments. """
    parser = argparse.ArgumentParser(description="Show the next action in your todo.txt",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-f", "--file", help="Filename of the todo.txt file to read",
                        type=str, default="todo.txt")
    return parser.parse_args()
