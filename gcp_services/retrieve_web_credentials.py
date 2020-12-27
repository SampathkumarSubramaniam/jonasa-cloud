from google.cloud import secretmanager

PROJECT_ID = "analog-sum-299523"


def access_secret_version(secret_id, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')


import json


def get_credentials():
    return json.loads(access_secret_version("jonasa-login"))
