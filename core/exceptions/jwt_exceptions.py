from core.exceptions.base_exception import BaseApplicationException


class JwtTypeNotFoundException(BaseApplicationException):
    def __init__(self):
        super().__init__('Тип токена не зарегистрирован')

class ExpiredTokenException(BaseApplicationException):
    def __init__(self):
        super().__init__("Срок действия токена истек")

class WrongTokenTypeException(BaseApplicationException):
    def __init__(self):
        super().__init__("Неправильный тип токена")

class TokenDecodeException(BaseApplicationException):
    def __init__(self):
        super().__init__("Ошибка декодирования токена")
