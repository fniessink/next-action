FROM koalaman/shellcheck:v0.5.0 AS shellcheck
FROM hadolint/hadolint:v1.13.0 AS hadolint
FROM python:3.6-alpine

LABEL maintainer="Frank Niessink <frank@niessink.com>"
LABEL description="Development dependencies for Next-action."

# Hadolint wants pinned versions but that breaks the build of the Docker image on Travis
# hadolint ignore=DL3018
RUN apk --no-cache add musl-dev gcc nodejs nodejs-npm graphviz docker git libffi-dev
# Git is needed by codacy-coverage, libffi by twine

COPY --from=shellcheck /bin/shellcheck /usr/local/bin/
COPY --from=hadolint /bin/hadolint /usr/local/bin/

RUN npm install -g gherkin-lint@2.13.2 markdownlint-cli@0.13.0
RUN pip install pip==18.0
WORKDIR /next-action
COPY requirements*.txt /next-action/
RUN pip install -r requirements.txt -r requirements-dev.txt
