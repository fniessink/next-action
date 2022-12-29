#!/bin/sh

mypy next_action
pylint next_action tests docs
pycodestyle next_action tests
pydocstyle next_action tests
vulture next_action .vulture-whitelist.py
pyroma --min=10 .
shellcheck extra/.next-action-completion.bash ci/*.sh
gherkin-lint tests/features/*.feature
markdownlint README.md docs/*.md; markdownlint -c .markdownlint-changelog.json CHANGELOG.md
hadolint Dockerfile
docker-compose config --quiet
