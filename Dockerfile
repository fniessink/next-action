FROM koalaman/shellcheck-alpine:v0.9.0 AS shellcheck
FROM hadolint/hadolint:v2.12.0-alpine AS hadolint
FROM python:3.12-alpine

LABEL maintainer="Frank Niessink <frank@niessink.com>"
LABEL description="Development dependencies for Next-action."

# Hadolint wants pinned versions but that breaks the build of the Docker image on Travis
# hadolint ignore=DL3018
RUN apk --no-cache add musl-dev gcc make nodejs npm graphviz docker docker-compose ttf-freefont libffi-dev openjdk11 unzip sed libxml2-dev libxslt-dev openssl-dev
# libffi is needed for twine, ubuntu-font-family for graphviz, openjdk11 for sonar-scanner, libxml2 for lxml

ADD https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.4.0.2170-linux.zip ./package.zip
RUN unzip package.zip && mv ./sonar-scanner* /sonar-scanner && ln -s /sonar-scanner/bin/sonar-scanner /usr/local/bin/sonar-scanner && rm package.zip
# Ensure Sonar uses the provided Java for musl instead of the included glibc one
RUN sed -i 's/use_embedded_jre=true/use_embedded_jre=false/g' /sonar-scanner/bin/sonar-scanner

COPY --from=shellcheck /bin/shellcheck /usr/local/bin/
COPY --from=hadolint /bin/hadolint /usr/local/bin/

RUN npm install -g gherkin-lint@4.2.2 markdownlint-cli@0.32.2 marked@4.2.5
WORKDIR /next-action
COPY requirements*.txt /next-action/
RUN pip install --no-cache-dir pip==22.3.1 && pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt
