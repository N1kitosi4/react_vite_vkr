from datetime import timedelta

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from dotenv import load_dotenv
import os

from app.core.security import create_access_token

# Загружаем переменные окружения из .env
load_dotenv()

# Конфигурация SMTP
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=os.getenv("MAIL_PORT"),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS"),
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS"),
    USE_CREDENTIALS=os.getenv("USE_CREDENTIALS"),
    VALIDATE_CERTS=os.getenv("VALIDATE_CERTS")
)


async def send_registration_email(email: EmailStr, username: str, user_id: int):
    # Создаем токен для верификации
    token = create_access_token(data={"sub": email}, expires_delta=timedelta(hours=1))
    verify_link = f"http://localhost:8000/users/verify-email?token={token}"

    message = MessageSchema(
        subject="Подтверждение регистрации",
        recipients=[email],
        body=f"""
        <h2>Привет, {username}!</h2>
        <p>Для завершения регистрации, подтвердите вашу почту:</p>
        <p><a href="{verify_link}">Подтвердить email</a></p>
        <p>Если вы не регистрировались, проигнорируйте это письмо.</p>
        """,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
