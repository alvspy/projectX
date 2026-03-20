import smtplib
import random
import ssl
from email.message import EmailMessage
from config import smtp_port, smtp_server, sender_email, sender_password

def send_verification_email(user_email):
    ver_code = str(random.randint(100000, 999999))
    msg = EmailMessage()
    msg.set_content(f"Ваш код верификации: {ver_code}")
    msg['Subject'] = "Подтверждение адреса электронной почты"
    msg['From'] = sender_email
    msg['To'] = user_email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)
    return int(ver_code)
