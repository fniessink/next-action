"""Insert the output of console commands into the README.md file."""

import datetime
import os
import shlex
import subprocess  # nosec
import sys


def do_command(line):
    """Run the command on the line and return its stdout and stderr."""
    command = shlex.split(line[2:])
    if command[0] == "next-action" and "--write-config-file" not in command:
        command.insert(1, "--config")
        command.insert(2, "docs/.next-action.cfg")
    command_output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    universal_newlines=True)
    stdout = command_output.stdout.strip()
    if command[0] in ("mypy", "pycodestyle", "pydocstyle") and stdout == "":
        stdout = "(no findings hence no output)"
    stderr = "" if command[0] == "pylint" else command_output.stderr.strip()
    return stdout, stderr


def create_toc(lines, toc_header, min_level=2, max_level=3):
    """Create the table of contents."""
    result = []
    for line in lines:
        level = line.count("#", 0, 6)
        if level < min_level or level > max_level or line.startswith(toc_header):
            continue
        indent = (level - min_level) * 2
        title = line.split(" ", 1)[1].rstrip()
        slug = title.lower().replace(" ", "-").replace("*", "").replace(".", "")
        result.append("{0}- [{1}](#{2})".format(" " * indent, title, slug))
    return "\n".join(result)


class StateMachine(object):
    """State machine for processing the lines in the README.md.

    Console commands are executed and the output is inserted. The table of contents is inserted and the old
    table of contents is skipped.
    """

    def __init__(self, toc, toc_header):
        """Initialize the state machine with the table of contents to insert and its header."""
        self.toc = toc
        self.toc_header = toc_header

    def default(self, line):
        """In the default state: print the line."""
        print(line)
        if line == "```console":
            return self.in_console
        elif line.startswith(self.toc_header):
            return self.start_toc
        return self.default

    def in_console(self, line):
        """In a console section: execute commands. Skip old output."""
        if line.startswith("$ "):
            print(line)
            stdout, stderr = do_command(line)
            if stdout:
                print(stdout)
            if stderr:
                print(stderr)
            return self.in_console
        elif line == "```":
            print(line)
            return self.default
        return self.in_console

    def start_toc(self, line):
        """Start of the table of contents."""
        print(line)
        return self.print_toc

    def print_toc(self, line):
        """Print the table of contents."""
        print(self.toc)
        if "- [" in line:
            return self.in_old_toc
        print(line)
        return self.default

    def in_old_toc(self, line):
        """Skip the old table of contents."""
        if "- [" in line:
            return self.in_old_toc
        print(line)
        return self.default


def update_readme():
    """Read the README markdown line by line and update table of contents and console commands."""
    start = datetime.datetime.now()
    with open("README.md") as readme:
        lines = readme.readlines()
    toc_header = "## Table of contents"
    machine = StateMachine(create_toc(lines, toc_header), toc_header)
    process = machine.default
    for line in lines:
        sys.stderr.write(".")
        sys.stderr.flush()
        process = process(line.rstrip())
    duration = datetime.datetime.now() - start
    sys.stderr.write("\n" + "-" * 40 + "\nProcessed {0} lines in {1}s.\n".format(len(lines), duration.seconds))


if __name__ == "__main__":
    os.environ['COLUMNS'] = "110"  # Fake that the terminal is wide enough.
    update_readme()
