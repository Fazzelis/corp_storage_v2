from core.exceptions.base_exception import BaseApplicationException


class UserAlreadyRegistered(BaseApplicationException):
    def __init__(self):
        super().__init__("Пользователь с такой почтой уже существует")


class InvalidLoginOrPassword(BaseApplicationException):
    def __init__(self):
        super().__init__("Неправильная почта или пароль")


class RefreshTokenNotFound(BaseApplicationException):
    def __init__(self):
        super().__init__("Refresh токен не найден")


class InvalidRecoveryCode(BaseApplicationException):
    def __init__(self):
        super().__init__("Неправильный код")


class InvalidTicket(BaseApplicationException):
    def __init__(self):
        super().__init__("Неправильный тикет восстановления пароля")


class TooManyAttempts(BaseApplicationException):
    def __init__(self):
        super().__init__("Слишком много попыток, попробуйте позже.")
