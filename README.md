# Next-action

[![PyPI](https://img.shields.io/pypi/v/next-action.svg)](https://img.shields.io/pypi/v/next-action.svg)
[![Updates](https://pyup.io/repos/github/fniessink/next-action/shield.svg)](https://pyup.io/repos/github/fniessink/next-action/)
[![Python 3](https://pyup.io/repos/github/fniessink/next-action/python-3-shield.svg)](https://pyup.io/repos/github/fniessink/next-action/)
[![Build Status](https://travis-ci.com/fniessink/next-action.svg?branch=master)](https://travis-ci.com/fniessink/next-action)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/746457c462cd4d9fa23f05424fa932b4)](https://www.codacy.com/app/frank_10/next-action?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=fniessink/next-action&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/746457c462cd4d9fa23f05424fa932b4)](https://www.codacy.com/app/frank_10/next-action?utm_source=github.com&utm_medium=referral&utm_content=fniessink/next-action&utm_campaign=Badge_Coverage)

Determine the next action to work on from a list of actions in a todo.txt file. *Next-action* is pre-alpha-stage at the moment, so its functionality is still rather limited.

Don't know what *Todo.txt* is? See <https://github.com/todotxt/todo.txt> for the *Todo.txt* specification.

*Next-action* is not a tool for editing todo.txt files, see <http://todotxt.org> for available options.

## Demo

![gif](demo.gif)

## Installation

*Next-action* requires Python 3.6 or newer.

`pip install next-action`

## Usage

```console
$ next-action --help
usage: next-action [-h] [--version] [-f FILE] [-n N | -a] [@CONTEXT [@CONTEXT ...]] [+PROJECT [+PROJECT ...]]

Show the next action in your todo.txt

positional arguments:
  @CONTEXT              show the next action in the specified contexts (default: None)
  +PROJECT              show the next action for the specified projects (default: None)

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -f FILE, --file FILE  todo.txt file to read; argument can be repeated (default: ['todo.txt'])
  -n N, --number N      number of next actions to show (default: 1)
  -a, --all             show all next actions (default: False)
```

Assuming your todo.txt file is in the current folder, running *Next-action* without arguments will show the next action you should do. Given this [todo.txt](todo.txt), calling mom would be the next action:

```console
$ next-action
(A) Call mom @phone
```

The next action is determined using priority. Creation date is considered after priority, with older tasks getting precedence over newer tasks.

Completed tasks (~~`x This is a completed task`~~) and tasks with a creation date in the future (`9999-01-01 Start preparing for five-digit years`) are not considered when determining the next action.

### Limit next actions

You can limit the tasks from which *Next-action* picks the next action by passing contexts and/or projects:

```console
$ next-action @work
(C) Finish proposal for important client @work

$ next-action +DogHouse
(G) Buy wood for new +DogHouse @store

$ next-action +DogHouse @home
Get rid of old +DogHouse @home
```

When you supply multiple contexts and/or projects, the next action belongs to all of the contexts and at least one of the projects:

```console
$ next-action +DogHouse +PaintHouse @store @weekend
(B) Buy paint to +PaintHouse @store @weekend
```

### Extend next actions

To show more than one next action, supply the number you think you can handle:

```console
$ next-action --number 3
(A) Call mom @phone
(B) Buy paint to +PaintHouse @store @weekend
(C) Finish proposal for important client @work
```

Or show all next actions, e.g. for a specific context:

```console
$ next-action --all @store
(B) Buy paint to +PaintHouse @store @weekend
(G) Buy wood for new +DogHouse @store
```

Note again that completed tasks and task with a future creation date are never shown since they can't be a next action.

*Next-action* being still pre-alpha-stage, this is it for the moment. Stay tuned for more options.

## Develop

Clone the repository and run the unit tests with `python setup.py test` or `python -m unittest`.

To create the unit test coverage report install the development dependencies with `pip install -r requirements-dev.txt` and run the unit tests under coverage with `coverage run --branch -m unittest; coverage html --fail-under=100 --directory=build/htmlcov`.

Quality checks can be run with `pylint next_action` and `pycodestyle next_action`.
