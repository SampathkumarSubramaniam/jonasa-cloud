import smtplib
from google.cloud import secretmanager
import json

PROJECT_ID = "analog-sum-299523"


def access_secret_version(secret_id, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')


def get_credentials(secret_name):
    return json.loads(access_secret_version(secret_name))


def cf_send_mail(data, context):
    credentials = dict()
    credentials = get_credentials("jonasa-mail")
    sender = credentials['MAIL_USERNAME']
    subject = "Login Attempt with wrong credentials"
    recipients = "sampathkumar.app@gmail.com"
    message = "Hello," + subject
    print("Sending mail")
    server = smtplib.SMTP_SSL(credentials['MAIL_SERVER'], credentials['MAIL_PORT'])
    server.login(credentials['MAIL_USERNAME'], credentials['MAIL_PASSWORD'])
    server.sendmail(sender, recipients, message)
    print("Successfully sent email")


cf_send_mail("a", "b")
