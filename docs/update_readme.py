""" Insert the output of console commands into the README.md file. """

import os
import subprocess  # nosec


def do_command(line):
    """ Run the command on the line and return its stdout and stderr. """
    command = line[2:].split(" ")
    if command[0] == "next-action" and "--write-config-file" not in command:
        command.extend(["--config", "docs/.next-action.cfg"])
    command_output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    check=True, universal_newlines=True)
    return command_output.stdout.strip(), command_output.stderr.strip()


def create_toc(lines, toc_header):
    """ Create the table of contents. """
    result = []
    for line in lines:
        if line.startswith("##") and not line.startswith(toc_header):
            indent = line.count("#") * 2 - 2
            title = line.split(" ", 1)[1].rstrip()
            slug = title.lower().replace(" ", "-").replace("*", "")
            result.append("{0}- [{1}](#{2})".format(" " * indent, title, slug))
    return "\n".join(result)


class StateMachine(object):
    """ State machine for processing the lines in the README.md. Console commands are executed and the output is
        inserted. The table of contents is inserted and the old table of contents is skipped. """

    def __init__(self, toc, toc_header):
        self.toc = toc
        self.toc_header = toc_header

    def default(self, line):
        """ Default action: print the line. """
        print(line)
        if line == "```console":
            return self.in_console
        elif line.startswith(self.toc_header):
            return self.start_toc
        return self.default

    def in_console(self, line):
        """ In a console section: execute commands. Skip old output. """
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
        """ Start of the table of contents. """
        print(line)
        return self.print_toc

    def print_toc(self, line):
        """ Print the table of contents. """
        print(self.toc)
        if line.startswith("  "):
            return self.in_old_toc
        print(line)
        return self.default

    def in_old_toc(self, line):
        """ Skip the old table of contents. """
        if line.startswith("  "):
            return self.in_old_toc
        if line:
            print(line)
        return self.default


def update_readme():
    """ Read the README markdown line by line and update table of contents and console commands. """
    with open("README.md") as readme:
        lines = readme.readlines()
    toc_header = "## Table of contents"
    machine = StateMachine(create_toc(lines, toc_header), toc_header)
    process = machine.default
    for line in lines:
        process = process(line.rstrip())


if __name__ == "__main__":
    os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
    update_readme()
