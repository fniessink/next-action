"""Get a SonarQube token for sonar-scanner."""

import sys

import requests

API_URL = f"{sys.argv[1].rstrip('/')}/api/user_tokens/"
API_ARGS = dict(data=dict(name="admin"), auth=("admin", "admin"))
requests.post(API_URL + "revoke", **API_ARGS)  # Revoke any previous tokens
print(requests.post(API_URL + "generate", **API_ARGS).json()["token"])
