# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

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
