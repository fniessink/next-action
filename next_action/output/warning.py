"""Module for warning messages."""

import argparse

from . import todotxt


def invalid_arguments(namespace: argparse.Namespace, tasks: todotxt.Tasks) -> str:
    """Check whether the context and projects given on the command line actually exist in the task file."""
    unknown_contexts = (namespace.contexts | namespace.excluded_contexts) - tasks.contexts()
    unknown_projects = (namespace.projects | namespace.excluded_projects) - tasks.projects()
    error_messages = []
    if unknown_contexts:
        plural = "s" if len(unknown_contexts) > 1 else ""
        error_messages.append(f"unknown context{plural}: {', '.join(sorted(unknown_contexts))}")
    if unknown_projects:
        plural = "s" if len(unknown_projects) > 1 else ""
        error_messages.append(f"unknown project{plural}: {', '.join(sorted(unknown_projects))}")
    return f" (warning: {'; '.join(error_messages)})" if error_messages else ""
