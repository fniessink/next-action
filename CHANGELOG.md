# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [1.8.0] - 2018-09-06

### Added

- Tab completion for the *Next-action* command line interface in Bash. Closes #228.

### Fixed

- Allow for projects and contexts at the start of a line. Fixes #242.

## [1.7.2] - 2018-08-26

### Fixed

- Add option `-V` as short alternative for `--version`. Fixes #225.

## [1.7.1] - 2018-08-26

### Changed

- Several performance improvements.

## [1.7.0] - 2018-08-23

### Added

- Allow for time travel using the `--time-travel` option. Closes #206.

### Changed

- Several performance improvements.

## [1.6.1] - 2018-08-10

### Fixed

- Allow for putting the `--blocked` option in the configuration file. Fixes #204.

## [1.6.0] - 2018-08-07

### Added

- Show tasks blocked by the next action using the `--blocked` option. Closes #166.

### Fixed

- Give proper error message when the `--number` argument is smaller than one. Fixes #164.

## [1.5.3] - 2018-07-14

### Fixed

- Allow for using `--config` when generating a configuration file with `--write-config-file` so it is possible to ignore the existing configuration file when generating a new one. Fixes #161.

## [1.5.2] - 2018-07-07

### Fixed

- Add support for Python 3.7.

## [1.5.1] - 2018-07-01

### Fixed

- When generating a configuration file with `--write-config-file` also include context and project filters passed on the command-line. Fixes #141.
- When generating a configuration file with `--write-config-file` also include the minimum priority if passed on the command-line. Fixes #142.
- Accept other arguments after excluded contexts and projects. Fixes #143.

## [1.5.0] - 2018-06-30

### Added

- When generating a configuration file with `--write-config-file` add any other options on the command-line to the generated configuration file. Closes #78.

## [1.4.0] - 2018-06-25

### Added

- Tasks are considered to have a priority that's the maximum of their own priority and the priorities of the task(s) they block, recursively. Closes #114.
- Tasks are considered to have a due date that's the minimum of their own due date and the due dates of the task(s) they block, recursively. Closes #115.

## [1.3.0] - 2018-06-19

### Added

- Next to `p:parent_task` it's also possible to use `before:parent_task` to specifiy task dependencies.
- In addition to `before:other_task`, it's also possible to use `after:other_task` to specify task dependencies.

## [1.2.0] - 2018-06-16

### Added

- Warn user if there are no next actions because they are using contexts or projects not present in the todo.txt file.

## [1.1.0] - 2018-06-11

### Added

- Take task dependencies into account. Closes #101.

## [1.0.0] - 2018-06-09

### Added

- Default context and/or project filters can be configured in the configuration file. Closes #109.

## [0.17.0] - 2018-06-07

### Added

- Support threshold dates (`t:<date>`) in todo.txt files.

## [0.16.3] - 2018-06-05

### Fixed

- Capitalise the help information. Fixes #105.

## [0.16.2] - 2018-06-05

### Fixed

- Mention how to deal with options with optional arguments followed by positional arguments in the help information and README. Closes #100.
- Short options immediately followed by a value weren't parsed correctly. Fixes #84.

## [0.16.1] - 2018-06-04

### Fixed

- Include reference parameter into standard configuration file. Fixes #98.

## [0.16.0] - 2018-06-03

### Added

- Optionally reference the todo.txt filename from which the next actions were read. Closes #38.

### Changed

- Reorganized the help information.

## [0.15.0] - 2018-06-02

### Added

- The due date argument to `--due` is now optional. Closes #92.

## [0.14.1] - 2018-06-01

### Fixed

- Fix packaging.

## [0.14.0] - 2018-06-01

### Added

- Option to limit the next action to tasks that have a given due date. Closes #53.

## [0.13.0] - 2018-05-30

### Added

- Using the `--style` option without arguments ignores the style specified in the configuration file, if any. Closes #83.

### Changed

- The `--no-config-file` option was removed. To not read any configuration file, use the `--config-file` option without specifying a configuration filename. Closes #82.

## [0.12.0] - 2018-05-28

### Added

- Option to limit the next action to tasks with a minimum priority. Closes #80.

### Fixed

- Properly wrap the usage line of the help information. Fixes #81.

## [0.11.0] - 2018-05-27

### Changed

- Better error messages when the configuration file is invalid.

## [0.10.1] - 2018-05-27

### Fixed

- Setup.py and requirements.txt were inconsistent.

## [0.10.0] - 2018-05-27

### Added

- Coloring of output using Pygments. Closes #11.

## [0.9.0] - 2018-05-25

### Added

- Option to limit the next action to tasks that are over due. Closes #75.

## [0.8.0] - 2018-05-24

### Added

- Option to not read a configuration file. Closes #71.
- Option to write a default configuration file. Closes #68.

## [0.7.0] - 2018-05-23

### Added

- The number of next actions to show can be configured in the configuration file. Closes #65.

### Changed

- Use a third-party package to validate the configuration file YAML instead of custom code. Closes #66.

## [0.6.0] - 2018-05-21

### Added

- Next-action can read a configuration file in which the todo.txt file(s) to read can be specified. Closes #40.

## [0.5.2] - 2018-05-19

### Fixed

- Make the demo animated gif visible on the Python Package Index. Fixes #61.

## [0.5.1] - 2018-05-19

### Added

- Add the README file to the package description on the [Python Package Index](https://pypi.org/project/next-action/). Closes #59.

## [0.5.0] - 2018-05-19

### Added

- Other properties being equal, task with more projects get precedence over tasks with fewer projects when selecting the next action. Closes #57.

## [0.4.0] - 2018-05-19

### Changed

- If no file is specified, *Next-action* tries to read the todo.txt in the user's home folder. Closes #4.

## [0.3.0] - 2018-05-19

### Added

- The `--file` argument accepts `-` to read input from standard input. Closes #42.

### Fixed

- Give consistent error message when files can't be opened. Fixes #54.

## [0.2.1] - 2018-05-16

### Changed

- Simpler help message. Fixes #45.

## [0.2.0] - 2018-05-14

### Added

- Allow for excluding contexts from which the next action is selected: `next-action -@office`. Closes #20.
- Allow for excluding projects from which the next action is selected: `next-action -+DogHouse`. Closes #32.

## [0.1.0] - 2018-05-13

### Added

- Take due date into account when determining the next action. Tasks due earlier take precedence. Closes #33.

## [0.0.9] - 2018-05-13

### Added

- Next-action can now read multiple todo.txt files to select the next action from. For example: `next-action --file todo.txt --file big-project-todo.txt`. Closes #35.

### Changed

- Ignore tasks that have a start date in the future. Closes #34.
- Take creation date into account when determining the next action. Tasks created earlier take precedence. Closes #26.

## [0.0.8] - 2018-05-13

### Added

- Specify the number of next actions to show: `next-action --number 3`. Closes #7.
- Show all next actions: `next-action --all`. Closes #29.

## [0.0.7] - 2018-05-12

### Added

- Allow for limiting the next action to one from multiple projects: `next-action +DogHouse +PaintHouse`. Closes #27.
- Allow for limiting the next action to multiple contexts: `next-action @work @staffmeeting`. Closes #23.

## [0.0.6] - 2018-05-11

### Added

- Allow for limiting the next action to a specific project. Closes #6.

## [0.0.5] - 2018-05-11

### Changed

- Renamed Next-action's binary from `next_action` to `next-action` for consistency with the application and project name.

## [0.0.4] - 2018-05-10

### Added

- Allow for limiting the next action to a specific context. Closes #5.
- Version number command line argument (`--version`) to display Next-action's version number.

### Fixed

- Runing tests with "python setup.py test" would result in test failures. Fixes #15.
- Move development dependencies to requirements-dev.txt so they don't get installed when a user installs Next-action. Fixes #14.
- Make Travis generate a wheel distribution in addition to the source distribution. Fixes #14.

## [0.0.3] - 2018-05-10

### Fixed

- Show default filename in the help message. Fixes #3.
- Show friendly error message when file cannot be found. Fixes #2.

## [0.0.2] - 2018-05-09

### Changed

- Release to the Python Package Index from Travis.

## [0.0.1] - 2018-05-06

### Added

- `next_action` script that reads a todo.txt file and prints the next action the user should work on, based on the priorities of the tasks.
