"""Setuptools setup script for Next-action."""

from setuptools import setup, find_packages

import next_action


setup(
    name=next_action.__title__,
    version=next_action.__version__,
    description="Command-line application to show the next action to work on from a todo.txt file",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Frank Niessink",
    author_email="frank@niessink.com",
    url="https://github.com/fniessink/next-action",
    license="Apache License, Version 2.0",
    python_requires=">=3.6",
    install_requires=["python-dateutil", "Cerberus", "PyYAML", "Pygments"],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "next-action=next_action:next_action",
        ],
    },
    zip_safe=True,
    test_suite="tests",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Office/Business :: Scheduling"],
    keywords=["todo.txt", "task management", "todolist"])
