class EmptyPlaylistError(Exception):
    def __init__(self, message="Список воспроизведения пуст."):
        super().__init__(message)


class InvalidDataError(Exception):
    def __init__(self, message="Некорректные данные"):
        super().__init__(message)


class ObjectNotFoundError(Exception):
    def __init__(self, message="Объект не найден"):
        super().__init__(message)


class ParsingError(Exception):
    def __init__(self, message="Проблема с парсингом, попробуйте позже"):
        super().__init__(message)
