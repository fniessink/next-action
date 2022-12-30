#!/bin/sh

pydeps --noshow -T png -o docs/dependencies.png next_action
pyreverse --module-names=yes --show-associated=1 --show-ancestors=1 --output=png next_action > /dev/null
mv classes.png docs/
mv packages.png docs/
pip install --quiet --quiet -e .
python docs/update_readme.py
marked -i README.md -o build/README.html
