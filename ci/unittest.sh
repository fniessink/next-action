#!/bin/sh

coverage run --branch -m unittest --quiet
coverage xml -o build/unittest-coverage.xml
coverage html --directory build/unittest-coverage
coverage report --fail-under=100 --skip-covered