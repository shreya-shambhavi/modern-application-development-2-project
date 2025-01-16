from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = "localhost"
SMTP_PORT = 1025
SENDER_EMAIL = "admin@iescp.com"
SENDER_PASSWORD = ""

def send_email(to, subject, body):
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = to
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))
    client = SMTP(host = SMTP_HOST, port = SMTP_PORT)
    client.send_message(message)
    client.quit()