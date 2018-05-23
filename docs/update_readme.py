""" Insert the output of console commands into the README.md file. """

import os
import subprocess  # nosec


def update_readme():
    """ Read the README markdown line by line and insert the output of any console commands. """
    with open("README.md") as readme:
        in_console_section = False
        for line in readme:
            line = line.rstrip()
            if line == "```console":
                print(line)
                in_console_section = True
            elif line == "```":
                print(line)
                in_console_section = False
            elif line.startswith("$ "):
                print(line)
                command = line[2:].split(" ")
                if command[0] == "next-action":
                    command.extend(["--file", "docs/todo.txt", "--config", "docs/.next-action.cfg"])
                command_output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                check=True, universal_newlines=True)
                stdout, stderr = command_output.stdout.strip(), command_output.stderr.strip()
                if stdout:
                    print(stdout)
                if stderr:
                    print(stderr)
            elif not in_console_section:
                print(line)


if __name__ == "__main__":
    os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.
    update_readme()
