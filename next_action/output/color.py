"""Colorize the output."""

import argparse

from pygments import lexers, formatters, highlight


def colorize(todotxt: str, namespace: argparse.Namespace) -> str:
    """Colorize the todotxt text according to the style."""
    if not namespace.style:
        return todotxt
    lexer = lexers.get_lexer_by_name("todotxt")
    formatter = formatters.get_formatter_by_name("terminal256", style=namespace.style)
    result = highlight(todotxt, lexer, formatter)
    if not todotxt.endswith("\n"):
        # Remove the line break that Pygments added
        result = result[:-1]  # pragma: no cover-behave
    return result
