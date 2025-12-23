from app.core_celery import celery_app
from app.services.email_service import send_ticket_email
from app.core.config import settings
import os

@celery_app.task(bind=True, max_retries=3)
def send_ticket_task(self, to_email: str, subject: str, html_content: str, attachments: list = None):
    try:
        send_ticket_email(to_email, subject, html_content, attachments)
        return {"status": "sent"}
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
