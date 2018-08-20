"""Colorize the output."""

import argparse
import functools

from pygments import lexers, formatters, highlight


@functools.lru_cache(maxsize=None)
def lexer():
    """Return the Todo.txt lexer."""
    return lexers.get_lexer_by_name("todotxt")


@functools.lru_cache(maxsize=None)
def formatter(style: str):
    """Return the formatter for the style."""
    return formatters.get_formatter_by_name("terminal256", style=style)


def colorize(todotxt: str, namespace: argparse.Namespace) -> str:
    """Colorize the todotxt text according to the style."""
    if not namespace.style:
        return todotxt
    result = highlight(todotxt, lexer(), formatter(namespace.style))
    if not todotxt.endswith("\n"):
        # Remove the line break that Pygments added
        result = result[:-1]  # pragma: no cover-behave
    return result
