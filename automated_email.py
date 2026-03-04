import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

# SMTP configuration
smtp_host = "smtp.gmail.com"
smtp_port = 587
smtp_email = os.getenv("SMTP_EMAIL")
smtp_password = os.getenv("SMTP_PASSWORD")

def send_email(to_email, subject, body):
    try:
        # Create email message body
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = smtp_email
        msg['To'] = to_email
        
        # Connect to SMTP server and send
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()  # Secure connection
            server.login(smtp_email, smtp_password)
            server.sendmail(smtp_email, to_email, msg.as_string())
        
        return True, "Email sent successfully"
    except Exception as e:
        return False, str(e)
