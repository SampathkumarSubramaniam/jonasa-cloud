from gcp_services.retrieve_web_credentials import get_credentials
import smtplib

PROJECT_ID = "analog-sum-299523"

credentials = dict()
credentials = get_credentials("jonasa-mail")

mail_settings = {
    "MAIL_SERVER": credentials['MAIL_SERVER'],
    "MAIL_PORT": credentials['MAIL_PORT'],
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": credentials['MAIL_USERNAME'],
    "MAIL_PASSWORD": credentials['MAIL_PASSWORD']
}


def cf_send_mail(data, context):
    sender = credentials['MAIL_USERNAME']
    subject = "Login Attempt with wrong credentials"
    recipients = "sampathkumar.app@gmail.com"
    message = "Hello," + subject
    print("Sending mail")
    try:
        server = smtplib.SMTP_SSL(credentials['MAIL_SERVER'], credentials['MAIL_PORT'])
        server.login(credentials['MAIL_USERNAME'], credentials['MAIL_PASSWORD'])
        server.sendmail(sender, recipients, message)
        print("Successfully sent email")
    except Exception as err:
        print(f"Error: unable to send email:{err}")


cf_send_mail("a", "b")
