#!/bin/sh

pip install --quiet --quiet -e .
behave --format null tests/features
coverage report --rcfile=.coveragerc-behave --fail-under=100 --skip-covered
