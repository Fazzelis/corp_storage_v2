import smtplib
from email.header import Header
from email.mime.text import MIMEText

from configuration import settings

class MailSender:
    async def send_verify_code(self, to_email: str, code: str):
        server = smtplib.SMTP(settings.smtp_server, int(settings.smtp_port))
        server.starttls()
        server.ehlo()

        server.login(settings.email_login, settings.email_password)

        msg = MIMEText(
            f"Вас пригласили в корпоративное хранилище файлов! Данные для входа в систему: почта: {to_email}, пароль: {code}",
            "plain",
            "utf-8"
        )
        msg["Subject"] = Header("Приглашение в корпоративное хранилище", "utf-8")
        msg["From"] = settings.email_login
        msg["To"] = to_email

        server.sendmail(settings.email_login, to_email, msg.as_string())

        server.quit()

    async def send_recovery_code(self, to_email: str, recovery_code: str):
        server = smtplib.SMTP(settings.smtp_server, int(settings.smtp_port))
        server.starttls()
        server.ehlo()

        server.login(settings.email_login, settings.email_password)

        msg = MIMEText(
            f"Ваш код для восстановления пароля: {recovery_code}. Если не вы его запросили, игнорируйте данное сообщение.",
            "plain",
            "utf-8"
        )
        msg["Subject"] = Header("Восстановление пароля от корпоративного хранилища", "utf-8")
        msg["From"] = settings.email_login
        msg["To"] = to_email

        server.sendmail(settings.email_login, to_email, msg.as_string())

        server.quit()
