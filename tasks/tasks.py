import smtplib
from email.message import EmailMessage
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.config import settings
from app.tasks.celery import celery


def get_mail_text(booking: dict, email_to: EmailStr) -> EmailMessage:
    email = EmailMessage()
    
    email['Subject'] = 'Подверждение бронирования'
    email['From'] = settings.SMTP_USER
    email['To'] = email_to
    
    email.set_content(
        f"""
            <h1>Подверждение бронирования</h1>
            <p>Вы бронировали номер от {booking['date_from']} по {booking['date_to']}</p>
        """, subtype='html'
    )
    return email


@celery.task
def process_pic(path: str) -> None:
    im_path = Path(path)
    im = Image.open(im_path)
    im_resized_450_720 = im.resize((720, 450))
    im_resized_270_135 = im.resize((270, 130))
    im_resized_450_720.save(f"app/media/highest/{im_path.name}")
    im_resized_270_135.save(f"app/media/lowers/{im_path.name}")
    

@celery.task
def send_message(booking: dict, email_to: EmailStr):
    
    msg_content = get_mail_text(booking, email_to)
    
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)