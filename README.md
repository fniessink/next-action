# Next-action

[![PyPI](https://img.shields.io/pypi/v/next-action.svg)](https://pypi.org/project/next-action/)
[![Updates](https://pyup.io/repos/github/fniessink/next-action/shield.svg)](https://pyup.io/repos/github/fniessink/next-action/)
[![Build Status](https://travis-ci.com/fniessink/next-action.svg?branch=master)](https://travis-ci.com/fniessink/next-action)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/746457c462cd4d9fa23f05424fa932b4)](https://www.codacy.com/app/frank_10/next-action?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=fniessink/next-action&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/746457c462cd4d9fa23f05424fa932b4)](https://www.codacy.com/app/frank_10/next-action?utm_source=github.com&utm_medium=referral&utm_content=fniessink/next-action&utm_campaign=Badge_Coverage)
[![SonarQube Badge](https://sonarcloud.io/api/project_badges/measure?project=fniessink%3Anext-action&metric=alert_status)](https://sonarcloud.io/dashboard?id=fniessink%3Anext-action)

Determine the next action to work on from a list of actions in a todo.txt file.

Don't know what *Todo.txt* is? See <https://github.com/todotxt/todo.txt> for the *Todo.txt* specification.

*Next-action* is not a tool for editing todo.txt files, see <http://todotxt.org> for available options.

## Table of contents

- [Demo](#demo)
- [Installation](#installation)
  - [*Next-action*](#next-action)
  - [Tab completion for *Next-action*](#tab-completion-for-next-action)
- [Usage](#usage)
  - [Limiting the tasks from which next actions are selected](#limiting-the-tasks-from-which-next-actions-are-selected)
  - [Showing more than one next action](#showing-more-than-one-next-action)
  - [Task dependencies](#task-dependencies)
  - [Styling the output](#styling-the-output)
  - [Configuring *Next-action*](#configuring-next-action)
  - [Option details](#option-details)
- [Recent changes](#recent-changes)
- [Developing *Next-action*](#developing-next-action)
  - [Installing the development environment and dependencies](#installing-the-development-environment-and-dependencies)
  - [Running unit tests](#running-unit-tests)
  - [Running feature tests](#running-feature-tests)
  - [Running quality checks](#running-quality-checks)
  - [Generating documentation](#generating-documentation)
  - [Source code structure and dependencies](#source-code-structure-and-dependencies)

## Demo

![gif](https://raw.githubusercontent.com/fniessink/next-action/master/docs/demo.gif)

## Installation

### *Next-action*

*Next-action* requires Python 3.6 or newer.

`pip install --upgrade next-action`

### Tab completion for *Next-action*

To install tab completion for *Next-action* in the Bash shell, follow these steps:

- Download [extra/.next-action-completion.bash](https://raw.githubusercontent.com/fniessink/next-action/master/extra/.next-action-completion.bash)
  and save it in your home folder.
- Next, add this line to your `~/.bash_profile` file:

  ```bash
  source ~/.next-action-completion.bash
  ```

- Then, open a new terminal.

Typing `next-action [TAB]` should give you the possible command line options. Hitting tab after an option that takes
arguments, shows the possible arguments.

## Usage

```console
$ next-action --help
Usage: next-action [-h] [-V] [-c [<config.cfg>] | -w] [-f <todo.txt> ...] [-b] [-g [<group>]] [-r <ref>] [-s
[<style>]] [-a | -n <number>] [-d [<due date>] | -o] [-p [<priority>]] [--] [<context|project> ...]

Show the next action in your todo.txt. The next action is selected from the tasks in the todo.txt file based
on task properties such as priority, due date, and creation date. Limit the tasks from which the next action
is selected by specifying contexts the tasks must have and/or projects the tasks must belong to.

Optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit

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
  -b, --blocked         show the tasks blocked by the next action, if any (default: False)
  -g [<group>], --groupby [<group>]
                        group the next actions; available groups: context, duedate, priority, project,
                        source (default: None)
  -r {always,never,multiple}, --reference {always,never,multiple}
                        reference next actions with the name of their todo.txt file (default: when reading
                        multiple todo.txt files)
  -s [<style>], --style [<style>]
                        colorize the output; available styles: abap, algol, algol_nu, arduino, autumn,
                        borland, bw, colorful, default, emacs, friendly, fruity, igor, lovelace, manni,
                        monokai, murphy, native, paraiso-dark, paraiso-light, pastie, perldoc, rainbow_dash,
                        rrt, sas, solarized-dark, solarized-light, stata, stata-dark, stata-light, tango,
                        trac, vim, vs, xcode (default: None)

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

Assuming your todo.txt file is in your home folder, running *Next-action* without arguments will show the next action
you should do. For example, given this
[todo.txt](https://raw.githubusercontent.com/fniessink/next-action/master/docs/todo.txt), calling mom would be the next
action:

```console
$ next-action
(A) Call mom @phone
```

The next action is determined using priority. Due date is considered after priority, with tasks due earlier getting
precedence over tasks due later. Creation date is considered after due date, with older tasks getting precedence over
newer tasks. Finally, tasks that belong to more projects get precedence over tasks that belong to fewer projects.

Several types of tasks can not be a next action:

- completed tasks (~~`x This is a completed task`~~),
- tasks with a creation date in the future (`9999-01-01 Start preparing for five-digit years`),
- tasks with a future threshold date (`Start preparing for emigration to Mars t:3000-01-01`),
- blocked tasks (see [task dependencies](#task-dependencies) below), and
- hidden tasks (`This is a hidden task h:1`).

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

When you supply multiple contexts and/or projects, the next action belongs to all of the contexts and at least one of
the projects:

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
Nothing to do! 😴
```

If there's nothing to do because you use contexts or projects that aren't present in the todo.txt file, *Next-action*
will warn you:

```console
$ next-action +PaintGarage @freetime
Nothing to do! (warning: unknown context: freetime; unknown project: PaintGarage)
```

#### By due date

To limit the the tasks from which the next action is selected to actions with a due date, use the `--due` option:

```console
$ next-action @home --due
(K) Pay October invoice @home due:2019-10-28
```

Add a due date to select a next action from tasks due on or before that date:

```console
$ next-action @home --due "2019-10-01"
(L) Pay September invoice @home due:2019-09-28
```

To make sure you have no overdue actions, or work on overdue actions first, limit the tasks from which the next action
is selected to overdue actions:

```console
$ next-action --overdue
Buy flowers due:2018-02-14
```

#### By priority

To make sure you work on important tasks rather than urgent tasks, you can make sure the tasks from which the
next action is selected have at least a minimum priority:

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

Note again that completed tasks, tasks with a future creation or threshold date, and blocked tasks are never the next
action.

### Task dependencies

*Next-action* takes task dependencies into account when determining the next actions. For example, that cooking a meal
depends on buying groceries and that doing the dishes comes after cooking the meal can be specified as follows:

```console
$ grep +DinnerParty docs/todo.txt
Buy groceries @store +DinnerParty before:meal
Cook meal @home +DinnerParty id:meal due:2018-07-01
Take out the garbage @home +DinnerParty due:2018-07-02
Do the dishes @home +DinnerParty after:meal
```

This means that buying groceries blocks cooking the meal; cooking, and thus doing the dishes as well, can't be done
until buying the groceries has been completed:

```console
$ next-action --all +DinnerParty
Buy groceries @store +DinnerParty before:meal
Take out the garbage @home +DinnerParty due:2018-07-02
```

Note how buying the groceries comes before taking out the garbage even though buying the groceries has no due date and
taking out the garbage does. As buying groceries has to be done before cooking the meal and cooking the meal does have
a due date, buying groceries takes on the same due date as cooking the meal. Priority is taken into account in a
similar way.

To show which tasks are blocked by the next action, use the `--blocked` option:

```console
$ next-action --blocked --all +DinnerParty
Buy groceries @store +DinnerParty before:meal
blocks:
- Cook meal @home +DinnerParty id:meal due:2018-07-01
  blocks:
  - Do the dishes @home +DinnerParty after:meal
Take out the garbage @home +DinnerParty due:2018-07-02
```

If you always want to see the tasks that are blocked by the next action, you can configure this in the configuration
file. See the section below on how to configure *Next-action*.

Additional notes:

- The ids can be any string without whitespace.
- Instead of `before` you can also use `p` (for "parent") because some other tools that work with *Todo.txt* files
  use that.
- A task can block multiple other tasks by repeating the before key,
  e.g. `Buy groceries before:cooking and before:sending_invites`.
- A task can be blocked by multiple other tasks by repeating the after key,
  e.g. `Eat meal after:cooking and after:setting_the_table`.
- If a task blocks one or more tasks, the blocking task takes on the priority and due date of the tasks it is blocking:
  - the blocking task is considered to have a priority that is the maximum of its own priority and the priorities of
    the tasks it is blocking, and
  - the blocking task is considered to have a due date that is the minimum of its own due date and the due dates of
    the tasks it is blocking.

### Styling the output

By default, *Next-action* references the todo.txt file from which actions were read if you read tasks from multiple
todo.txt files. The `--reference` option controls this:

```console
$ next-action --reference always
(A) Call mom @phone [docs/todo.txt]
```

Use `--reference never` to turn off this behavior. To permanently change this, configure the option in the
configuration file. See the section below on how to configure *Next-action*.

The next actions can be colorized using the `--style` argument. Run `next-action --help` to see the list of possible
styles.

When you've decided on a style you prefer, it makes sense to configure the style in the configuration file. See the
section below on how to configure *Next-action*.

Not passing an argument to `--style` cancels the style that is configured in the configuration file, if any.

When showing multiple next actions, these can be grouped by passing the `--groupby` option:

```console
$ next-action --number 5 --groupby context
phone:
- (A) Call mom @phone
store:
- (B) Buy paint to +PaintHouse @store @weekend
- (G) Buy wood for new +DogHouse @store
weekend:
- (B) Buy paint to +PaintHouse @store @weekend
work:
- (C) Finish proposal for important client @work
home:
- (K) Pay October invoice @home due:2019-10-28
```

*Next-action* sorts the groups according to the most important next action in the group. Actions may be repeated
if they belong to multiple groups, as is the case with the `Buy paint` task above.

If you always want to group next actions, you can configure this in the configuration file. See the section
below on how to configure *Next-action*.

### Configuring *Next-action*

In addition to specifying options on the command-line, you can also configure options in a configuration file. The
configuration file format is [YAML](http://yaml.org). The options currently supported are which todo.txt files must be
read, how many next actions should be shown, output styling, and context and/or project filters.

#### Writing the configuration file

To get started, you can tell *Next-action* to generate a configuration file with the default options:

```console
$ next-action --write-config-file
# Configuration file for Next-action. Edit the settings below as you like.
file: ~/todo.txt
number: 1
reference: multiple
style: default
```

To make this the configuration that *Next-action* reads by default, redirect the output to `~/.next-action.cfg` like
this: `next-action --write-config-file > ~/.next-action.cfg`.

Any additional options specified on the command line are used to generate the configuration file:

```console
$ next-action --write-config-file --blocked --groupby context --number 3 --file ~/tasks.txt --style fruity --priority Z -@waiting
# Configuration file for Next-action. Edit the settings below as you like.
blocked: true
file: ~/tasks.txt
filters:
- -@waiting
groupby: context
number: 3
priority: Z
reference: multiple
style: fruity
```

#### Reading the configuration file

By default, *Next-action* tries to read a file called
[.next-action.cfg](https://raw.githubusercontent.com/fniessink/next-action/master/docs/.next-action.cfg) in your home
folder.

If you want to use a configuration file that is not in the default location (`~/.next-action.cfg`), you'll need to
explicitly specify its location:

```console
$ next-action --config-file docs/.next-action.cfg
(A) Call mom @phone
```

To skip reading the default configuration file, and also not read an alternative configuration file, use the
`--config-file` option without arguments.

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

#### Configuring the tasks from which next actions are selected

##### Limiting by contexts and/or projects

You can limit the tasks from which the next action is selected by specifying contexts and/or projects to filter on,
just like you would do on the command line:

```yaml
filters: -+FutureProject @work -@waiting
```

This would make *Next-action* by default select next actions from tasks with a `@work` context and without the
`@waiting` context and not belonging to the `+FutureProject`.

An alternative syntax is:

```yaml
filters:
  - -+FutureProject
  - '@work'
  - -@waiting
```

Note that filters starting with `@` need to be in quotes. This is a
[YAML restriction](http://yaml.org/spec/1.1/current.html#c-directive).

##### Limiting by priority

The minimum priority of next actions to show can be specified as well:

```yaml
priority: Z
```

This could be useful if you, for example, keep a backlog of ideas without priority in your todo.txt file and
prioritize only the tasks that are actionable.

Specifying a value on the command line overrides the priority in the configuration file, e.g.
`next-action --priority C`. To override the priority set in the configuration but not set another minimum priority,
use the priority option without argument: `next-action --priority`.

#### Configuring the output

Whether the next actions should have a reference to the todo.txt file from which they were read can be configured
using the reference keyword:

```yaml
reference: always
```

Possible values are `always`, `never`, or `multiple`. The latter means that the filename is only added when you read
tasks from multiple todo.txt files. The default value is `multiple`.

The output style can be configured using the style keyword:

```yaml
style: colorful
```

Run `next-action --help` to see the list of possible styles.

To always see the tasks blocked by the next action, put this in your configuration file:

```yaml
blocked: true
```

Next actions can be configured to be grouped as follows:

```yaml:
groupby: priority
```

Possible grouping options are by `context`, `duedate`, `priority`, `project`, and `source`. Specifying a value on
the command line overrides the grouping in the configuration file, e.g. `next-action --groupby project`.
To cancel the grouping set in the configuration file all together, use the groupby option without argument:
`next-action --groupby`.

### Option details

#### Precedence

Options in the configuration file override the default options. Command-line options in turn override options in the
configuration file.

If you have a configuration file with default options that you occasionally want to ignore, you can skip reading the
configuration file entirely with the `--no-config-file` option.

#### Optional arguments followed by positional arguments

When you use an option that takes an optional argument, but have it followed by a positional argument, *Next-action*
will interpret the positional argument as the argument to the option and complain, e.g.:

```console
$ next-action --due @home
Usage: next-action [-h] [-V] [-c [<config.cfg>] | -w] [-f <todo.txt> ...] [-b] [-g [<group>]] [-r <ref>] [-s
[<style>]] [-a | -n <number>] [-d [<due date>] | -o] [-p [<priority>]] [--] [<context|project> ...]
next-action: error: argument -d/--due: invalid date: @home
```

There's two ways to help *Next-action* figure out what you mean. Either reverse the order of the arguments:

```console
$ next-action @home --due
(K) Pay October invoice @home due:2019-10-28
```

Or use `--` to separate the option from the positional argument(s):

```console
$ next-action --due -- @home
(K) Pay October invoice @home due:2019-10-28
```

## Recent changes

See the [change log](https://github.com/fniessink/next-action/blob/master/CHANGELOG.md).

## Developing *Next-action*

### Installing the development environment and dependencies

We use Docker as development environment. To build the Docker image with all the development dependencies make sure
you have Git and Docker installed. Then, follow these steps:

- Clone the repository: `git clone https://github.com/fniessink/next-action.git`.
- Enter the folder: `cd next-action`.
- Build the Docker image: `docker build . -t next-action-dev`.

The `docker-compose.yml` contains services for each of the development tools. These are described below.

### Running unit tests

To run the unit tests and check their code coverage:

```console
$ docker-compose --no-ansi up unittest
Starting next-action_unittest_1 ...
Starting next-action_unittest_1 ... done
Attaching to next-action_unittest_1
unittest_1                | ----------------------------------------------------------------------
unittest_1                | Ran 258 tests in 3.305s
unittest_1                |
unittest_1                | OK
unittest_1                | Name    Stmts   Miss Branch BrPart  Cover
unittest_1                | -----------------------------------------
unittest_1                | -----------------------------------------
unittest_1                | TOTAL    1668      0    244      0   100%
unittest_1                |
unittest_1                | 29 files skipped due to complete coverage.
next-action_unittest_1 exited with code 0
```

The HTML coverage report is written to `build/unittest-coverage/`.

### Running feature tests

To run the feature tests and measure their code coverage:

```console
$ docker-compose --no-ansi up behave
Starting next-action_behave_1 ...
Starting next-action_behave_1 ... done
Attaching to next-action_behave_1
behave_1                  | 16 features passed, 0 failed, 0 skipped
behave_1                  | 116 scenarios passed, 0 failed, 0 skipped
behave_1                  | 383 steps passed, 0 failed, 0 skipped, 0 undefined
behave_1                  | Took 1m45.811s
behave_1                  | Name    Stmts   Miss Branch BrPart  Cover
behave_1                  | -----------------------------------------
behave_1                  | -----------------------------------------
behave_1                  | TOTAL     500      0    226      0   100%
behave_1                  |
behave_1                  | 12 files skipped due to complete coverage.
next-action_behave_1 exited with code 0
```

The HTML coverage report is written to `build/feature-coverage/`.

### Running quality checks

The tools Mypy, Pylint, Pycodestyle, Pydocstyle, Bandit, Pyroma, and Vulture are used to check for quality issues in
the Python code. Shellcheck is used evaluate the Bash code. Gherkin feature files are chcked with Gherkin-lint.
The Markdown files are evaluated with Markdownlint. The Dockerfile is checked with Hadolint. The docker-compose.yml is
checked with Docker-compose.

To run the quality checks:

```console
$ docker-compose --no-ansi up quality
Starting next-action_quality_1 ...
Starting next-action_quality_1 ... done
Attaching to next-action_quality_1
quality_1                 | Generated HTML report (via XSLT): /Users/fniessink/workspace/next-action/build/mypy/index.html
quality_1                 |
quality_1                 | --------------------------------------------------------------------
quality_1                 | Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
quality_1                 |
quality_1                 | ------------------------------
quality_1                 | Checking .
quality_1                 | Found next-action
quality_1                 | ------------------------------
quality_1                 | Final rating: 10/10
quality_1                 | Your cheese is so fresh most people think it's a cream: Mascarpone
quality_1                 | ------------------------------
next-action_quality_1 exited with code 0
```

### Generating documentation

This `README.md` file is generated with `docker-compose up docs`.

The dependency graph below is created with Pydeps and the package and class diagrams below are created with
Pyreverse (part of Pylint).

### Source code structure and dependencies

The dependency graph shows the relationships between the packages and modules in the code base and the third-party
packages used. When the user imvokes *Next-action* from the command-line, the `next_action()` method in the
`next_action` package is run. The `next_action()` method uses the `next_action.arguments` package to parse the
command-line arguments and the configuration file. The *Todo.txt* file is read into a domain model using the
`next_action.todotxt` package. The `next_action.pick_action` module contains the logic to select the next action.
Finally, the output is formatted using the `next_action.output` package.

![png](https://raw.githubusercontent.com/fniessink/next-action/master/docs/dependencies.png)

The package diagram created by Pyreverse looks quite similar.

![png](https://raw.githubusercontent.com/fniessink/next-action/master/docs/packages.png)

The class diagram created by Pyreverse shows the classes used. The biggest one is the `NextActionArgumentParser` class,
responsible for parsing the command-line arguments. The other two relevant classes are the `Task` class for holding
information about an individual task and the `Tasks` class that contains a collection of tasks.

![png](https://raw.githubusercontent.com/fniessink/next-action/master/docs/classes.png)
