from core.exceptions.base_exception import BaseApplicationException


class EmptyAvatarException(BaseApplicationException):
    def __init__(self):
        super().__init__("Файл пустой!")


class UnsupportedAvatarTypeException(BaseApplicationException):
    def __init__(self):
        super().__init__("Поддерживается только PNG и JPG")

class TooBigResolutionAvatarException(BaseApplicationException):
    def __init__(self, max_resolution: int):
        super().__init__(f"Разрешение больше чем {max_resolution}x{max_resolution}")


class TooSmallResolutionAvatarException(BaseApplicationException):
    def __init__(self):
        super().__init__("Разрешение меньше 0!")


class NotImageAvatarException(BaseApplicationException):
    def __init__(self):
        super().__init__("Файл не является изображением")


class TooBigFileSizeAvatarException(BaseApplicationException):
    def __init__(self):
        super().__init__("Слишком большой размер файл")


class FailToWriteAvatarException(BaseApplicationException):
    def __init__(self):
        super().__init__("Ошибка записи файла")


class ImageNotFoundAvatarException(BaseApplicationException):
    def __init__(self):
        super().__init__("Файл не найден")
