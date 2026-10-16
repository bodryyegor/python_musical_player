from .patterns import file_logger_decorator


class LogMixin:
    @file_logger_decorator()
    def log(self, message):
        print(f"{self.__class__.__name__}: {message}")
