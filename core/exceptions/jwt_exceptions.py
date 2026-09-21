from core.exceptions.base_exception import BaseApplicationException

class JwtTypeNotFoundException(BaseApplicationException):
    def __init__(self):
        super().__init__('Тип токена не зарегистрирован')
