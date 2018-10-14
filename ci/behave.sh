#!/bin/sh

python setup.py --quiet develop
behave --format null tests/features
coverage report --rcfile=.coveragerc-behave --fail-under=100 --skip-covered
