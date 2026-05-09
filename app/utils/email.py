import smtplib
from email.mime.text import MIMEText

from app.config import settings


def send_email(
    to_email: str,
    subject: str,
    body: str
):

    try:
        msg = MIMEText(body)

        msg["Subject"] = subject
        msg["From"] = settings.SMTP_EMAIL
        msg["To"] = to_email

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            settings.SMTP_EMAIL,
            settings.SMTP_PASSWORD
        )

        server.sendmail(
            settings.SMTP_EMAIL,
            to_email,
            msg.as_string()
        )

        server.quit()

        print(f"Email sent to {to_email}")

    except Exception as e:
        print("EMAIL ERROR:", str(e))