from core.exceptions.base_exception import BaseApplicationException


class UserNotFound(BaseApplicationException):
    def __init__(self):
        super().__init__("Пользователь не найден")


class UserMustChangePassword(BaseApplicationException):
    def __init__(self):
        super().__init__("Для доступа смените пароль")
