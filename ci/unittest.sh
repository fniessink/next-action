#!/bin/sh

# Ignore the Deprecation warning thrown by nose, see https://github.com/nose-devs/nose/issues/559
python -W ignore:DeprecationWarning -m coverage run --branch -m unittest --quiet
coverage xml -o build/unittest-coverage.xml
coverage html --directory build/unittest-coverage
coverage report --fail-under=100 --skip-covered
