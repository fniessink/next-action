# Next-action

[![PyPI](https://img.shields.io/pypi/v/next-action.svg)](https://pypi.org/project/next-action/)
[![Updates](https://pyup.io/repos/github/fniessink/next-action/shield.svg)](https://pyup.io/repos/github/fniessink/next-action/)
[![Python 3](https://pyup.io/repos/github/fniessink/next-action/python-3-shield.svg)](https://pyup.io/repos/github/fniessink/next-action/)
[![Build Status](https://travis-ci.com/fniessink/next-action.svg?branch=master)](https://travis-ci.com/fniessink/next-action)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/746457c462cd4d9fa23f05424fa932b4)](https://www.codacy.com/app/frank_10/next-action?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=fniessink/next-action&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/746457c462cd4d9fa23f05424fa932b4)](https://www.codacy.com/app/frank_10/next-action?utm_source=github.com&utm_medium=referral&utm_content=fniessink/next-action&utm_campaign=Badge_Coverage)

Determine the next action to work on from a list of actions in a todo.txt file. *Next-action* is currently beta-stage so, although it should work pretty well, it may be a bit rough around the edges.

Don't know what *Todo.txt* is? See <https://github.com/todotxt/todo.txt> for the *Todo.txt* specification.

*Next-action* is not a tool for editing todo.txt files, see <http://todotxt.org> for available options.

## Table of contents

- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
  - [Limiting the tasks from which next actions are selected](#limiting-the-tasks-from-which-next-actions-are-selected)
  - [Showing more than one next action](#showing-more-than-one-next-action)
  - [Styling the output](#styling-the-output)
  - [Configuring *Next-action*](#configuring-next-action)
- [Recent changes](#recent-changes)
- [Develop](#develop)

## Demo

![gif](https://raw.githubusercontent.com/fniessink/next-action/master/docs/demo.gif)

## Installation

*Next-action* requires Python 3.6 or newer.

`pip install next-action`

## Usage

```console
$ next-action --help
usage: next-action [-h] [--version] [-c [<config.cfg>]] [-f <todo.txt>] [-n <number> | -a] [-o] [-p [<priority>]] [-s
[<style>]] [<context|project> ...]

Show the next action in your todo.txt. The next action is selected from the tasks in the todo.txt file based on task
properties such as priority, due date, and creation date. Limit the tasks from which the next action is selected by
specifying contexts the tasks must have and/or projects the tasks must belong to.

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --write-config-file   generate a sample configuration file and exit
  -c [<config.cfg>], --config-file [<config.cfg>]
                        filename of configuration file to read (default: ~/.next-action.cfg); omit filename to not
                        read any configuration file
  -f <todo.txt>, --file <todo.txt>
                        filename of todo.txt file to read; can be '-' to read from standard input; argument can be
                        repeated to read tasks from multiple todo.txt files (default: ~/todo.txt)
  -n <number>, --number <number>
                        number of next actions to show (default: 1)
  -a, --all             show all next actions
  -o, --overdue         show only overdue next actions
  -p [<priority>], --priority [<priority>]
                        minimum priority (A-Z) of next actions to show (default: None)
  -s [<style>], --style [<style>]
                        colorize the output; available styles: abap, algol, algol_nu, arduino, autumn, borland, bw,
                        colorful, default, emacs, friendly, fruity, igor, lovelace, manni, monokai, murphy, native,
                        paraiso-dark, paraiso-light, pastie, perldoc, rainbow_dash, rrt, tango, trac, vim, vs, xcode
                        (default: None)

optional context and project arguments; these can be repeated:
  @<context>            context the next action must have
  +<project>            project the next action must be part of
  -@<context>           context the next action must not have
  -+<project>           project the next action must not be part of
```

Assuming your todo.txt file is your home folder, running *Next-action* without arguments will show the next action you should do. Given this [todo.txt](https://raw.githubusercontent.com/fniessink/next-action/master/docs/todo.txt), calling mom would be the next action:

```console
$ next-action
(A) Call mom @phone
```

The next action is determined using priority. Due date is considered after priority, with tasks due earlier getting precedence over tasks due later. Creation date is considered after due date, with older tasks getting precedence over newer tasks. FInally, tasks that belong to more projects get precedence over tasks that belong to fewer projects.

Completed tasks (~~`x This is a completed task`~~) and tasks with a creation date in the future (`9999-01-01 Start preparing for five-digit years`) are not considered when determining the next action.

### Limiting the tasks from which next actions are selected

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

It is also possible to exclude contexts, which means the next action will not have the specified contexts:

```console
$ next-action +PaintHouse -@store
Borrow ladder from the neighbors +PaintHouse @home
```

And of course, in a similar vein, projects can be excluded:

```console
$ next-action -+PaintHouse @store
(G) Buy wood for new +DogHouse @store
```

To make sure you have no overdue actions, or work on overdue actions first, limit the tasks from which the next action is selected to overdue actions:

```console
$ next-action --overdue
Buy flowers due:2018-02-14
```

To make sure you work on important tasks rather than urgent tasks, you can make sure the tasks from which the next action is selected have at least a minimum priority:

```console
$ next-action @work --priority C
(C) Finish proposal for important client @work
```

### Showing more than one next action

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

### Styling the output

The next actions can be colorized using the `--style` argument. Run `next-action --help` to see the list of possible styles.

When you've decided on a style you prefer, it makes sense to configure the style in the configuration file. See the section below on how to configure *Next-action*.

Not passing an argument to `--style` cancels the style that is configured in the configuration file, if any.

### Configuring *Next-action*

In addition to specifying options on the command-line, you can also configure options in a configuration file. By default, *Next-action* tries to read a file called [.next-action.cfg](https://raw.githubusercontent.com/fniessink/next-action/master/docs/.next-action.cfg) in your home folder.

To get started, you can tell *Next-action* to generate a configuration file with the default options:

```console
$ next-action --write-config-file
# Configuration file for Next-action. Edit the settings below as you like.
file: ~/todo.txt
number: 1
style: default
```

To make this the configuration that *Next-action* reads by default, redirect the output to `~/.next-action.cfg` like this: `next-action --write-config-file > ~/.next-action.cfg`.

If you want to use a configuration file that is not in the default location (`~/.next-action.cfg`), you'll need to explicitly specify its location:

```console
$ next-action --config-file docs/.next-action.cfg
(A) Call mom @phone
```

To skip reading the default configuration file, and also not read an alternative configuration file, use the `--config-file` option without arguments.

The configuration file format is [YAML](http://yaml.org). The options currently supported are which todo.txt files must be read, how many next actions should be shown, and the styling.

#### Configuring a default todo.txt

A default todo.txt file to use can be specified like this:

```yaml
file: ~/Dropbox/todo.txt
```

Multiple todo.txt files can be listed, if needed:

```yaml
file:
  - personal-todo.txt
  - work-todo.txt
  - big-project/tasks.txt
```

#### Configuring the number of next actions to show

The number of next actions to show can be specified like this:

```yaml
number: 3
```

Or you can have *Next-action* show all next actions:

```yaml
all: True
```

#### Configuring the minimum priority to show

The minimum priority of next action to show can be specified as well:

```yaml
priority: Z
```

This could be useful if you, for example, keep a backlog of ideas without priority in your todo.txt file and prioritize only the tasks that are actionable.

Specifying a value on the command line overrides the priority in the configuration file, e.g. `next-action --priority C`. To override the priority set in the configuration but not set another minimum priority, use the priority option without argument: `next-action --priority`.

#### Configuring the style to use

The style can be configured using the style keyword:

```yaml:
style: colorful
```

Run `next-action --help` to see the list of possible styles.

#### Precedence of options

Options in the configuration file override the default options. Command-line options in turn override options in the configuration file.

If you have a configuration file with default options that you occasionally want to ignore, you can skip reading the configuration file entirely with the `--no-config-file` option.

## Recent changes

See the [change log](https://raw.githubusercontent.com/fniessink/next-action/master/CHANGELOG.md).

## Develop

Clone the repository, create a virtual environment, install the dependencies with `pip install -r requirements-dev.txt -r requirements.txt`, and install *Next-action* in development mode using `python setup.py develop`.

To run the unit tests:

```console
$ python -m unittest
................................................................................................................................................
----------------------------------------------------------------------
Ran 144 tests in 0.465s

OK
```

Running `python setup.py test` should give the same results.

To create the unit test coverage report run the unit tests under coverage with `coverage run --branch -m unittest; coverage html --fail-under=100 --directory=build/htmlcov`.

Quality checks can be run with `pylint next_action` and `pycodestyle next_action`.
