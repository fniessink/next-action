#!/bin/sh

mypy next_action
pylint next_action tests docs
pycodestyle .
pydocstyle .
vulture next_action .vulture-whitelist.py
# Set min pyroma to 9 because Pyroma does not yet accept Markdown, see https://github.com/regebro/pyroma/issues/42
pyroma --min=9 .
shellcheck extra/.next-action-completion.bash ci/*.sh
gherkin-lint tests/features/*.feature
markdownlint README.md docs/*.md; markdownlint -c .markdownlint-changelog.json CHANGELOG.md
hadolint Dockerfile
docker-compose config --quiet
