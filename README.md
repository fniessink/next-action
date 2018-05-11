# Next-action

[![PyPI](https://img.shields.io/pypi/v/next-action.svg)](https://img.shields.io/pypi/v/next-action.svg)
[![Updates](https://pyup.io/repos/github/fniessink/next-action/shield.svg)](https://pyup.io/repos/github/fniessink/next-action/)
[![Python 3](https://pyup.io/repos/github/fniessink/next-action/python-3-shield.svg)](https://pyup.io/repos/github/fniessink/next-action/)
[![Build Status](https://travis-ci.com/fniessink/next-action.svg?branch=master)](https://travis-ci.com/fniessink/next-action)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/746457c462cd4d9fa23f05424fa932b4)](https://www.codacy.com/app/frank_10/next-action?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=fniessink/next-action&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/746457c462cd4d9fa23f05424fa932b4)](https://www.codacy.com/app/frank_10/next-action?utm_source=github.com&utm_medium=referral&utm_content=fniessink/next-action&utm_campaign=Badge_Coverage)

Determine the next action to work on from a list of actions in a todo.txt file. Next-action is alpha-stage at the moment, so its options are rather limited at the moment.

Don't know what todo.txt is? See <https://github.com/todotxt/todo.txt> for the todo.txt specification.

Next-action is not a tool for editing todo.txt files, see <http://todotxt.org> for available options.

## Installation

Next-action requires Python 3.6 or newer.

`pip install next-action`

## Usage

```console
$ next-action --help
usage: next-action [-h] [--version] [-f FILE] [@CONTEXT] [+PROJECT]

Show the next action in your todo.txt

positional arguments:
  @CONTEXT              show the next action in the specified context (default: None)
  +PROJECT              show the next action for the specified project (default: None)

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -f FILE, --file FILE  filename of the todo.txt file to read (default: todo.txt)
```

Assuming your todo.txt file is in the current folder, running Next-action without arguments will show the next action you should do based on your tasks' priorities:

```console
$ next-action
(A) Call mom @phone
```

You can limit the tasks from which Next-action picks the next action by passing a context and/or a project:

```console
$ next-action @work
(C) Finish proposal for important client @work
$ next-action +DogHouse
(G) Buy wood for +DogHouse @store
$ next-action +DogHouse @home
Get rid of old +DogHouse @home
```

Since Next-action is still alpha-stage, this is it for the moment. Stay tuned for more options.

## Develop

Clone the repository and run the unit tests with `python setup.py test`.

To create the unit test coverage report install the development dependencies with `pip install -r requirements-dev.txt` and run the unit tests under coverage with `coverage run --branch -m unittest; coverage html --fail-under=100 --directory=build/htmlcov`.
