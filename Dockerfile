FROM python:3.6-alpine 

LABEL maintainer="Frank Niessink <frank@niessink.com>"
LABEL description="Development dependencies for Next-action."

RUN apk --no-cache add musl-dev gcc nodejs nodejs-npm graphviz docker

# hadolint ignore=DL3022
COPY --from=koalaman/shellcheck /bin/shellcheck /usr/local/bin/
# hadolint ignore=DL3022
COPY --from=hadolint/hadolint /bin/hadolint /usr/local/bin/
 
RUN npm install -g gherkin-lint@2.13.2 markdownlint-cli@0.13.0
RUN pip install pip==18.0
WORKDIR /next-action
COPY requirements*.txt /next-action/
RUN pip install -r requirements.txt -r requirements-dev.txt

