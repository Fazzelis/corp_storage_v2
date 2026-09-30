from core.exceptions.base_exception import BaseApplicationException


class UserNotFound(BaseApplicationException):
    def __init__(self):
        super().__init__("Пользователь не найден")
