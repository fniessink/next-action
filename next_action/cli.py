""" Entry point for Next-action's command-line interface. """

import argparse
import os

from next_action.arguments import parse_arguments
from next_action.pick_action import next_actions
from next_action.todotxt import read_todotxt_files, Tasks
from next_action.output import render


def validate_arguments(parser: argparse.ArgumentParser, namespace: argparse.Namespace, tasks: Tasks) -> None:
    """ Check whether the context and projects given on the command line actually exist in the task file. """
    unknown_contexts = (namespace.contexts | namespace.excluded_contexts) - tasks.contexts()
    unknown_projects = (namespace.projects | namespace.excluded_projects) - tasks.projects()
    error_messages = []
    if unknown_contexts:
        error_messages.append("unknown contexts: {0}".format(", ".join(unknown_contexts)))
    if unknown_projects:
        error_messages.append("unknown projects: {0}".format(", ".join(unknown_projects)))
    if error_messages:
        parser.error("; ".join(error_messages))


def next_action() -> None:
    """ Entry point for the command-line interface.

        Basic recipe:
        1) parse command-line arguments,
        2) read todo.txt file(s),
        3) determine the next action(s) and,
        4) display them.
    """
    parser, namespace = parse_arguments()
    filenames = [os.path.expanduser(filename) for filename in namespace.file]
    try:
        tasks = read_todotxt_files(filenames)
    except OSError as reason:
        parser.error("can't open file: {0}".format(reason))
    validate_arguments(parser, namespace, tasks)
    actions = next_actions(tasks, namespace)
    print(render(actions, namespace) if actions else "Nothing to do!")
