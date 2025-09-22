import smtplib
import ssl
from pydantic import EmailStr
from app.settings import settings
from app.tasks.email_template import create_user_confirmation_template
from app.tasks.tasks import celery



@celery.task(max_retries=3)
def send_booking_confirmation_email(email_to: EmailStr):
    try:
        msg_content = create_user_confirmation_template(email_to)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT, context=context) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.send_message(msg_content)
    except (smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError) as exc:
        raise send_booking_confirmation_email.retry(exc=exc, countdown=60)