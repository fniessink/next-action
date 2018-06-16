""" Entry point for Next-action's command-line interface. """

import argparse
import os

from next_action.arguments import parse_arguments
from next_action.pick_action import next_actions
from next_action.todotxt import read_todotxt_files, Tasks
from next_action.output import render


def validate_arguments(namespace: argparse.Namespace, tasks: Tasks) -> str:
    """ Check whether the context and projects given on the command line actually exist in the task file. """
    unknown_contexts = (namespace.contexts | namespace.excluded_contexts) - tasks.contexts()
    unknown_projects = (namespace.projects | namespace.excluded_projects) - tasks.projects()
    error_messages = []
    if unknown_contexts:
        plural = "s" if len(unknown_contexts) > 1 else ""
        error_messages.append("unknown context{0}: {1}".format(plural, ", ".join(sorted(unknown_contexts))))
    if unknown_projects:
        plural = "s" if len(unknown_projects) > 1 else ""
        error_messages.append("unknown project{0}: {1}".format(plural, ", ".join(sorted(unknown_projects))))
    return (" (warning: {0})".format("; ".join(error_messages))) if error_messages else ""


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
    actions = next_actions(tasks, namespace)
    print(render(actions, namespace) if actions else "Nothing to do!" + validate_arguments(namespace, tasks))
