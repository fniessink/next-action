#!/bin/sh

pydeps --noshow -T png -o docs/dependencies.png next_action
pyreverse --module-names=yes --show-associated=1 --show-ancestors=1 --output=png next_action > /dev/null
mv classes.png docs/
mv packages.png docs/
python setup.py --quiet develop
python docs/update_readme.py 
markdown README.md > build/README.html
