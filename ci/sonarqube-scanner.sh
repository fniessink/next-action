#!/bin/sh

# SonarQube needs Xunit format, see https://docs.sonarqube.org/display/PLUG/Python+Unit+Tests+Execution+Reports+Import
nosetests --nocapture --with-xunit --xunit-file=build/nosetests.xml tests/unittests
sonar-scanner -Dsonar.host.url="$SONARQUBE_URL" -Dsonar.login="$(python ci/sonarqube_token.py "$SONARQUBE_URL")"
