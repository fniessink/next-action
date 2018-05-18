""" Insert the output of console commands into the README.md file. """

import os
import subprocess


os.environ['COLUMNS'] = "120"  # Fake that the terminal is wide enough.


with open("README.md") as readme:
    skipping_old_output = False 
    for line in readme:
        line = line.rstrip()
        if line.startswith("$ "):
            print(line)
            skipping_old_output = True
            command = line[2:].split(" ")
            print(subprocess.run(command, stdout=subprocess.PIPE, universal_newlines=True).stdout.rstrip())
        elif line == "```":
            skipping_old_output = False
            print(line)
        else:
            if not skipping_old_output:
                print(line)

