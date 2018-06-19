# Next-action

[![PyPI](https://img.shields.io/pypi/v/next-action.svg)](https://pypi.org/project/next-action/)
[![Updates](https://pyup.io/repos/github/fniessink/next-action/shield.svg)](https://pyup.io/repos/github/fniessink/next-action/)
[![Build Status](https://travis-ci.com/fniessink/next-action.svg?branch=master)](https://travis-ci.com/fniessink/next-action)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/746457c462cd4d9fa23f05424fa932b4)](https://www.codacy.com/app/frank_10/next-action?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=fniessink/next-action&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/746457c462cd4d9fa23f05424fa932b4)](https://www.codacy.com/app/frank_10/next-action?utm_source=github.com&utm_medium=referral&utm_content=fniessink/next-action&utm_campaign=Badge_Coverage)
[![SonarQube Badge](https://sonarcloud.io/api/project_badges/measure?project=fniessink%3Anext-action&metric=alert_status)](https://sonarcloud.io/api/project_badges/measure?project=fniessink%3Anext-action&metric=alert_status)

Determine the next action to work on from a list of actions in a todo.txt file.

Don't know what *Todo.txt* is? See <https://github.com/todotxt/todo.txt> for the *Todo.txt* specification.

*Next-action* is not a tool for editing todo.txt files, see <http://todotxt.org> for available options.

## Table of contents

- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
  - [Limiting the tasks from which next actions are selected](#limiting-the-tasks-from-which-next-actions-are-selected)
  - [Showing more than one next action](#showing-more-than-one-next-action)
  - [Task dependencies](#task-dependencies)
  - [Styling the output](#styling-the-output)
  - [Configuring *Next-action*](#configuring-next-action)
  - [Option details](#option-details)
- [Recent changes](#recent-changes)
- [Developing *Next-action*](#developing-next-action)
  - [Installing the development environment](#installing-the-development-environment)
  - [Running unit tests](#running-unit-tests)
  - [Running quality checks](#running-quality-checks)

## Demo

![gif](https://raw.githubusercontent.com/fniessink/next-action/master/docs/demo.gif)

## Installation

*Next-action* requires Python 3.6 or newer.

`pip install next-action`

## Usage

```console
$ next-action --help
Usage: next-action [-h] [--version] [-c [<config.cfg>] | -w] [-f <todo.txt> ...] [-r <ref>] [-s [<style>]] [-a
| -n <number>] [-d [<due date>] | -o] [-p [<priority>]] [--] [<context|project> ...]

Show the next action in your todo.txt. The next action is selected from the tasks in the todo.txt file based
on task properties such as priority, due date, and creation date. Limit the tasks from which the next action
is selected by specifying contexts the tasks must have and/or projects the tasks must belong to.

Optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit

Configuration options:
  -c [<config.cfg>], --config-file [<config.cfg>]
                        filename of configuration file to read (default: ~/.next-action.cfg); omit filename
                        to not read any configuration file
  -w, --write-config-file
                        generate a sample configuration file and exit

Input options:
  -f <todo.txt>, --file <todo.txt>
                        filename of todo.txt file to read; can be '-' to read from standard input; argument
                        can be repeated to read tasks from multiple todo.txt files (default: ~/todo.txt)

Output options:
  -r {always,never,multiple}, --reference {always,never,multiple}
                        reference next actions with the name of their todo.txt file (default: when reading
                        multiple todo.txt files)
  -s [<style>], --style [<style>]
                        colorize the output; available styles: abap, algol, algol_nu, arduino, autumn,
                        borland, bw, colorful, default, emacs, friendly, fruity, igor, lovelace, manni,
                        monokai, murphy, native, paraiso-dark, paraiso-light, pastie, perldoc, rainbow_dash,
                        rrt, tango, trac, vim, vs, xcode (default: None)

Show multiple next actions:
  -a, --all             show all next actions
  -n <number>, --number <number>
                        number of next actions to show (default: 1)

Limit the tasks from which the next actions are selected:
  -d [<due date>], --due [<due date>]
                        show only next actions with a due date; if a date is given, show only next actions
                        due on or before that date
  -o, --overdue         show only overdue next actions
  -p [<priority>], --priority [<priority>]
                        minimum priority (A-Z) of next actions to show (default: None)
  @<context> ...        contexts the next action must have
  +<project> ...        projects the next action must be part of; if repeated the next action must be part
                        of at least one of the projects
  -@<context> ...       contexts the next action must not have
  -+<project> ...       projects the next action must not be part of

Use -- to separate options with optional arguments from contexts and projects, in order to handle cases
where a context or project is mistaken for an argument to an option.
```

Assuming your todo.txt file is your home folder, running *Next-action* without arguments will show the next action you should do. Given this [todo.txt](https://raw.githubusercontent.com/fniessink/next-action/master/docs/todo.txt), calling mom would be the next action:

```console
$ next-action
(A) Call mom @phone
```

The next action is determined using priority. Due date is considered after priority, with tasks due earlier getting precedence over tasks due later. Creation date is considered after due date, with older tasks getting precedence over newer tasks. Finally, tasks that belong to more projects get precedence over tasks that belong to fewer projects.

Several types of tasks are not considered when determining the next action:

- completed tasks (~~`x This is a completed task`~~),
- tasks with a creation date in the future (`9999-01-01 Start preparing for five-digit years`),
- tasks with a future threshold date (`Start preparing for emigration to Mars t:3000-01-01`), and
- blocked tasks (see [task dependencies](#task-dependencies) below).

### Limiting the tasks from which next actions are selected

#### By contexts and/or projects

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

If no tasks match the combination of tasks and projects, it's time to get some coffee:

```console
$ next-action +DogHouse @weekend
Nothing to do!
```

But, if there's nothing to do because you use contexts or projects that aren't present in the todo.txt file, *Next-action* will warn you:

```console
$ next-action +PaintGarage @freetime
Nothing to do! (warning: unknown context: freetime; unknown project: PaintGarage)
```

#### By due date

To limit the the tasks from which the next action is selected to actions with a due date, use the `--due` option:

```console
$ next-action @home --due
(K) Pay July invoice @home due:2018-07-28
```

Add a due date to select a next action from tasks due on or before that date:

```console
$ next-action @home --due "june 2018"
(L) Pay June invoice @home due:2018-06-28
```

To make sure you have no overdue actions, or work on overdue actions first, limit the tasks from which the next action is selected to overdue actions:

```console
$ next-action --overdue
Buy flowers due:2018-02-14
```

#### By priority

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
Buy groceries @store +DinnerParty before:meal
```

Note again that completed tasks, tasks with a future creation or threshold date, and blocked tasks are never shown since they can't be a next action.

### Task dependencies

*Next-action* takes task dependencies into account when determining the next actions. For example, that cooking a meal depends on buying groceries and that doing the dishes comes after cooking the meal can be specified as follows:

```text
Buy groceries @store +DinnerParty before:meal
Cook meal @home +DinnerParty id:meal
Do the dishes @home +DinnerParty after:meal
```

This means that buying groceries blocks cooking the meal; cooking, and thus doing the dishes as well, can't be done until buying the groceries has been completed:

```console
$ next-action --all +DinnerParty
Buy groceries @store +DinnerParty before:meal
```

Notes:

- The ids can be any string without whitespace.
- Instead of `before` you can also use `p` (for "parent") because some other tools that work with *Todo.txt* files use that.
- A task can come before multiple other tasks by repeating the before key, e.g. `Buy groceries before:cooking and before:sending_invites`.
- A task can come after multiple other tasks by repeating the after key, e.g. `Eat meal after:cooking and after:setting_the_table`.

### Styling the output

By default, *Next-action* references the todo.txt file from which actions were read if you read tasks from multiple todo.txt files. The `--reference` option controls this:

```console
$ next-action --reference always
(A) Call mom @phone [docs/todo.txt]
```

Use `--reference never` to turn off this behavior. To permanently change this, configure the option in the configuration file. See the section below on how to configure *Next-action*.

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
reference: multiple
style: default
```

To make this the configuration that *Next-action* reads by default, redirect the output to `~/.next-action.cfg` like this: `next-action --write-config-file > ~/.next-action.cfg`.

If you want to use a configuration file that is not in the default location (`~/.next-action.cfg`), you'll need to explicitly specify its location:

```console
$ next-action --config-file docs/.next-action.cfg
(A) Call mom @phone
```

To skip reading the default configuration file, and also not read an alternative configuration file, use the `--config-file` option without arguments.

The configuration file format is [YAML](http://yaml.org). The options currently supported are which todo.txt files must be read, how many next actions should be shown, output styling, and context and/or project filters.

#### Configuring a default todo.txt

A default todo.txt file to use can be specified like this in the configuration file:

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

#### Limiting the tasks from which next actions are selected

##### By contexts and/or projects

You can limit the tasks from which the next action is selected by specifying contexts and/or projects to filter on, just like you would do on the command line:

```yaml
filters: -+FutureProject @work -@waiting
```

This would make *Next-action* by default select next actions from tasks with a `@work` context and without the `@waiting` context and not belonging to the `+FutureProject`.

An alternative syntax is:

```yaml
filters:
  - -+FutureProject
  - '@work'
  - -@waiting
```

Note that filters starting with `@` need to be in quotes. This is a [YAML restriction](http://yaml.org/spec/1.1/current.html#c-directive).

##### By priority

The minimum priority of next action to show can be specified as well:

```yaml
priority: Z
```

This could be useful if you, for example, keep a backlog of ideas without priority in your todo.txt file and prioritize only the tasks that are actionable.

Specifying a value on the command line overrides the priority in the configuration file, e.g. `next-action --priority C`. To override the priority set in the configuration but not set another minimum priority, use the priority option without argument: `next-action --priority`.

#### Configuring the output

Whether the next actions should have a reference to the todo.txt file from which they were read can be configured using the reference keyword:

```yaml
reference: always
```

Possible values are `always`, `never`, or `multiple`. The latter means that the filename is only added when you read tasks from multiple todo.txt files. The default value is `multiple`.

The output style can be configured using the style keyword:

```yaml
style: colorful
```

Run `next-action --help` to see the list of possible styles.

### Option details

#### Precedence

Options in the configuration file override the default options. Command-line options in turn override options in the configuration file.

If you have a configuration file with default options that you occasionally want to ignore, you can skip reading the configuration file entirely with the `--no-config-file` option.

#### Optional arguments followed by positional arguments

When you use an option that takes an optional argument, but have it followed by a positional argument, *Next-action* will interpret the positional argument as the argument to the option and complain, e.g.:

```console
$ next-action --due @home
Usage: next-action [-h] [--version] [-c [<config.cfg>] | -w] [-f <todo.txt> ...] [-r <ref>] [-s [<style>]] [-a
| -n <number>] [-d [<due date>] | -o] [-p [<priority>]] [--] [<context|project> ...]
next-action: error: argument -d/--due: invalid date: @home
```

There's two ways to help *Next-action* figure out what you mean. Either reverse the order of the arguments:

```console
$ next-action @home --due
(K) Pay July invoice @home due:2018-07-28
```

Or use `--` to separate the option from the positional argument(s):

```console
$ next-action --due -- @home
(K) Pay July invoice @home due:2018-07-28
```

## Recent changes

See the [change log](https://github.com/fniessink/next-action/blob/master/CHANGELOG.md).

## Developing *Next-action*

### Installing the development environment

To work on the software, clone the repository, create a virtual environment, install the dependencies with `pip install -r requirements-dev.txt -r requirements.txt`, and install *Next-action* in development mode using `python setup.py develop`.

### Running unit tests

To run the unit tests:

```console
$ python -m unittest
.............................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 221 tests in 1.637s

OK
```

Running `python setup.py test` should give the same results.

To create the unit test coverage report run the unit tests under coverage with:

```console
$ coverage run --branch -m unittest
.............................................................................................................................................................................................................................
----------------------------------------------------------------------
Ran 221 tests in 2.085s

OK
```

And then check the coverage. It should be 100%.

```console
$ coverage report --fail-under=100 --omit=".venv/*" --skip-covered
Name    Stmts   Miss Branch BrPart  Cover
-----------------------------------------
-----------------------------------------
TOTAL    1188      0    150      0   100%

25 files skipped due to complete coverage.
```

### Running quality checks

We use mypy, pylint, and  pycodestyle to check for quality issues. Mypy should give no warnings or errors:

```console
$ mypy --no-incremental --ignore-missing-import next_action
(no findings hence no output)
```

Pylint should score 10 out of 10:

```console
$ pylint next_action
--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
```

And pycodestyle should give no warnings or errors:

```console
$ pycodestyle next_action
(no findings hence no output)
```
