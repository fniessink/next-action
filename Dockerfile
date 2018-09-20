FROM python:3.6-alpine as base

MAINTAINER Frank Niessink <frank@niessink.com>

RUN apk --no-cache add musl-dev

# Build shellcheck
FROM base AS shellcheck

RUN apk --no-cache add cabal ghc 
RUN cabal update
RUN cabal install ShellCheck

# Install development dependencies
FROM base AS python

COPY --from=shellcheck /root/.cabal/bin/shellcheck /usr/local/bin/
 
RUN apk --no-cache add gcc nodejs nodejs-npm graphviz docker
RUN npm install -g gherkin-lint markdownlint-cli
RUN pip install --upgrade pip
WORKDIR /work
COPY requirements*.txt /work/
RUN pip install -r requirements.txt -r requirements-dev.txt


