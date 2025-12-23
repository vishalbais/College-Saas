import smtplib
from email.message import EmailMessage
from app.core.config import settings
from typing import Optional
import os
from email.mime.image import MIMEImage

def send_ticket_email(to_email: str, subject: str, html_content: str, attachments: Optional[list] = None):
    """
    Basic SMTP email send. In prod replace with robust mail service (SendGrid, SES)
    attachments: list of file paths to attach
    """
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_USER
    msg["To"] = to_email
    msg.set_content("This is a ticket email. Please open in an HTML-capable client.")
    msg.add_alternative(html_content, subtype="html")

    if attachments:
        for path in attachments:
            if not os.path.exists(path):
                continue
            with open(path, "rb") as f:
                img_data = f.read()
            img = MIMEImage(img_data)
            img.add_header('Content-ID', f"<{os.path.basename(path)}>" )
            img.add_header("Content-Disposition", "inline", filename=os.path.basename(path))
            msg.get_payload().append(img)

    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        smtp.send_message(msg)
