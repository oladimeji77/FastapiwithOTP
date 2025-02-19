import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

def send_email(recipient_email, body):
    sender_email = "oladimeji.oladepo@gmail.com"
    password = "xdnv ctvy cdxn exsh"
    sender_name = "OLADIMEJI"
    subject = "Welcome to my Bank"
    

    message = MIMEText(body, 'html')
    message['Subject'] = subject
    message['From'] = formataddr((sender_name, sender_email))
    message['To'] = recipient_email


    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient_email, message.as_string())
# app pass from google: bank - xdnv ctvy cdxn exsh
# Example usage:
sender_name = "OLADIMEJI"
sender_email = "oladimeji.oladepo@gmail.com"
recipient_email = "oladepo.oladimeji@gmail.com"
subject = "Test Email"
body = """
<html>
<head>
<title>HTML Email</title>
</head>
<body>
<p>This is an HTML email with <b>bold</b> text and <i>italic</i> text.</p>
</body>
</html>
"""

# send_email(recipient_email, body)