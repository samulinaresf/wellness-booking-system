from smtplib import SMTP, SMTPException
from db.db import Session
from db.models import User
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

def send_message_by_email(
    user_email: str,
    subject: str,
    message: str
):    
    
    SMTP_EMAIL = os.getenv("SMTP_EMAIL")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
        
    msg = MIMEMultipart()
    msg["From"] = SMTP_EMAIL
    msg["To"] = user_email
    msg["Subject"] = f"{subject}"

    body = f"{message}"

    msg.attach(MIMEText(body, "plain"))

    # Enviar el correo usando el servidor SMTP
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
            servidor.starttls()
            servidor.login(SMTP_EMAIL, SMTP_PASSWORD)
            servidor.sendmail(SMTP_EMAIL, user_email, msg.as_string())
            print("Correo enviado con éxito")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

        