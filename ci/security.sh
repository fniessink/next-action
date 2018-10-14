#!/bin/sh

bandit -r next_action --format custom 2> /dev/null
bandit -r next_action --format html --output build/bandit.html 2> /dev/null  # Ignore boiler plate output
safety check -r requirements.txt -r requirements-dev.txt --bare
