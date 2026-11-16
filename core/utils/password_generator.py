import secrets
from configuration import settings


class PasswordGenerator:
    def __init__(self, chars_list: list | None = None, password_len: int | None = None):
        self._chars_list = chars_list if chars_list is not None else list(settings.generated_password_alphabet)
        self._password_len = password_len if password_len is not None else settings.generated_password_len

    def generate_password(self) -> str:
        return "".join(secrets.choice(self._chars_list) for _ in range(self._password_len))


default_password_generator = PasswordGenerator()
