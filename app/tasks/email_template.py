from email.message import EmailMessage

from pydantic import EmailStr

from app.settings import settings


def create_user_confirmation_template(
    email_to: EmailStr,
):
    email = EmailMessage()

    email["Subject"] = "Добро пожаловать в сервис Cutly"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Добро пожаловать на сайт Cutly!</h1>
                    {email_to}
        """,
        subtype="html",
    )
    return email
