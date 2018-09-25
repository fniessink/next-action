FROM python:3.6-alpine 

LABEL maintainer="Frank Niessink <frank@niessink.com>"
LABEL description="Development dependencies for Next-action."

RUN apk --no-cache add musl-dev=1.1.18-r3 gcc=6.4.0-r5 nodejs=8.9.3-r1 nodejs-npm=8.9.3-r1 graphviz=2.40.1-r0 docker=17.12.1-r0

# hadolint ignore=DL3022
COPY --from=koalaman/shellcheck /bin/shellcheck /usr/local/bin/
# hadolint ignore=DL3022
COPY --from=hadolint/hadolint /bin/hadolint /usr/local/bin/
 
RUN npm install -g gherkin-lint@2.13.2 markdownlint-cli@0.13.0
RUN pip install pip==18.0
WORKDIR /next-action
COPY requirements*.txt /next-action/
RUN pip install -r requirements.txt -r requirements-dev.txt

