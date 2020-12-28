from google.cloud import secretmanager
from google.cloud import pubsub_v1
import json

PROJECT_ID = "analog-sum-299523"
TOPIC_ID = "jonasa-web-wrong-credentials"


def publish_msg(msg):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
    msg = msg.encode("utf-8")
    future = publisher.publish(topic_path, msg, origin="jonasa-cloud", username="jonasa")
    print(future.result())


def access_secret_version(secret_id, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')


def get_credentials(secret_name):
    return json.loads(access_secret_version(secret_name))
