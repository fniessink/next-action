#!/bin/sh

mypy next_action
pylint next_action tests docs
pycodestyle .
pydocstyle .
vulture next_action .vulture-whitelist.py
pyroma --min=10 . 2> /dev/null  # Ignore the error messages on stderr about the README file because pyroma doesn't accept Markdown.
shellcheck extra/.next-action-completion.bash ci/*.sh
gherkin-lint tests/features/*.feature
markdownlint README*.md; markdownlint -c .markdownlint-changelog.json CHANGELOG.md
hadolint Dockerfile
docker-compose config --quiet

