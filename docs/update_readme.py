"""Insert the output of console commands into the README.md file."""

import datetime
import os
import pathlib
import re
import shlex
import subprocess  # nosec
import sys

from asserts import assert_equal, assert_regex


def do_command(line):
    """Run the command on the line and return its stdout and stderr."""
    command = shlex.split(line[2:])
    if command[0] == "next-action":
        command.insert(1, "--config")
        if "--write-config-file" not in command:
            command.insert(2, "docs/.next-action.cfg")
    command_output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    return "\n".join([line.rstrip() for line in command_output.stdout.rstrip().split("\n")])


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
        result.append(f"{' ' * indent}- [{title}](#{slug})")
    return "\n".join(result) + "\n"


class StateMachine():
    """State machine for processing the lines in the README.md.

    Console commands are executed and the output is inserted. The table of contents is inserted and the old
    table of contents is skipped.
    """

    def __init__(self, toc, toc_header):
        """Initialize the state machine with the table of contents to insert and its header."""
        self.toc = toc
        self.toc_header = toc_header
        self.lines = []
        self.output = ""
        self.expected_output = ""

    def default(self, line):
        """In the default state: print the line."""
        self.write_lines(line)
        if line == "```console":
            return self.in_console
        if line.startswith(self.toc_header):
            return self.start_toc
        return self.default

    def in_console(self, line):
        """In a console section: execute commands. Skip old output."""
        if line.startswith("$ "):
            self.expected_output = ""  # Reset the expected output
            self.write_lines(line)
            self.output = do_command(line)
            if self.output:
                self.write_lines(self.output)
            return self.in_console
        if line == "```":
            if self.expected_output.strip().startswith("re: "):
                regex = re.compile(self.expected_output[len("re: "):].strip(), re.MULTILINE)
                assert_regex(self.output.strip(), regex)
            else:
                assert_equal(self.expected_output.strip(), self.output.strip())
            self.write_lines(line)
            return self.default
        self.expected_output += "\n" + line
        return self.in_console

    def start_toc(self, line):
        """Start of the table of contents."""
        self.write_lines(line)
        return self.print_toc

    def print_toc(self, line):
        """Print the table of contents."""
        self.write_lines(self.toc)
        self.write_lines(line)
        return self.default

    def write_lines(self, line):
        """Write the line to the collection of lines for the README.md."""
        self.lines.append(line)


def update_readme():
    """Read the README markdown template line by line and update table of contents and console commands."""
    start = datetime.datetime.now()
    with open("README.in.md") as readme_in:
        lines = readme_in.readlines()
    toc_header = "## Table of contents"
    machine = StateMachine(create_toc(lines, toc_header), toc_header)
    process = machine.default
    for line in lines:
        sys.stderr.write(".")
        sys.stderr.flush()
        process = process(line.rstrip())
    pathlib.Path("README.md").write_text("\n".join(machine.lines) + "\n")
    duration = datetime.datetime.now() - start
    sys.stderr.write("\n" + "-" * 40 + f"\nProcessed {len(lines)} lines in {duration.seconds}s.\n")


if __name__ == "__main__":
    os.environ['COLUMNS'] = "110"  # Fake that the terminal is wide enough.
    update_readme()
