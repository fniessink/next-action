""" Setuptools setup script for Next-action. """

from setuptools import setup, find_packages

import next_action


setup(
    name=next_action.__title__,
    version=next_action.__version__,
    description="Command-line application to show the next action to work on from a todo.txt file",
    long_description="""Show the next action to work on from a todo.txt file, based on context, priority,
and more.""",
    author="Frank Niessink",
    author_email="frank@niessink.com",
    url="https://github.com/fniessink/next-action",
    license="Apache License, Version 2.0",
    python_requires=">=3.6",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "next-action=next_action.cli:next_action",
        ],
    },
    test_suite="tests",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Topic :: Office/Business :: Scheduling"],
    keywords=["todo.txt", "task management", "todolist"])
