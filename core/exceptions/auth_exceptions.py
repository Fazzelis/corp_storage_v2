from core.exceptions.base_exception import BaseApplicationException


class UserAlreadyRegistered(BaseApplicationException):
    def __init__(self):
        super().__init__("Пользователь с такой почтой уже существует")
