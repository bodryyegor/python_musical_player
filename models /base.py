from typing import List, TypeVar

from .exceptions import EmptyPlaylistError, InvalidDataError, ObjectNotFoundError
from .mixin import LogMixin
from .patterns import MP3Manager
from .registry import ClassRegistryMeta

MP3Type = TypeVar("MP3Type", bound="MP3")


class MP3(LogMixin, metaclass=ClassRegistryMeta):
    __slots__ = ("_title", "_duration", "_type")
    _all_mp3_files = []

    def __init__(self, title, duration):
        self._title = ""
        self._duration = 0
        self.set_title(title)
        self.set_duration(duration)
        self._type = self.__class__.__name__
        MP3._all_mp3_files.append(self)
        MP3Manager().notify_observers("Файл создан", self.get_title())

    def get_title(self):
        return self._title

    def set_title(self, new_title):
        if isinstance(new_title, str) and new_title.strip():
            self._title = new_title
        else:
            raise InvalidDataError("Название должно быть непустой строкой.")

    def get_duration(self):
        return self._duration

    def set_duration(self, new_duration):
        if isinstance(new_duration, int) and new_duration > 0:
            self._duration = new_duration
        else:
            raise InvalidDataError(
                "Продолжительность должна быть положительным числом."
            )

    @classmethod
    def get_all_mp3_files(cls) -> List[MP3Type]:
        return cls._all_mp3_files

    @staticmethod
    def display_info(obj):
        print(f"{'-' * 50}")
        print(str(obj))
        print(f"{'-' * 50}\n")
        obj.log("Информация выведена")

    @classmethod
    def is_available(cls, title: str) -> bool:
        return any(mp3.get_title() == title for mp3 in cls._all_mp3_files)

    @classmethod
    def remove_by_title(cls, title: str) -> bool:
        title = title.strip().lower()
        initial_count = len(cls._all_mp3_files)
        cls._all_mp3_files = [
            item
            for item in cls._all_mp3_files
            if item.get_title().strip().lower() != title
        ]
        return len(cls._all_mp3_files) < initial_count

    def play(self):
        print(f"Воспроизведение {self._type}: {self.get_title()}")
        self.log("Началось воспроизведение")

    def pause(self):
        print(f"Пауза {self._type}: {self.get_title()}")
        self.log("Поставлена пауза")

    def __str__(self):
        return f"{self._type}: {self.get_title()}, Продолжительность: {self.get_duration()} сек."
