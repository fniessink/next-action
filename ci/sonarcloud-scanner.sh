#!/bin/sh

# SonarQube needs Xunit format, see https://docs.sonarqube.org/display/PLUG/Python+Unit+Tests+Execution+Reports+Import
nosetests --nocapture --with-xunit --xunit-file=build/nosetests.xml tests/unittests
sonar-scanner -Dsonar.host.url=http://sonarcloud.io -Dsonar.organization=fniessink-github -Dsonar.login=$$SONAR_TOKEN
