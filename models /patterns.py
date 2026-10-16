import datetime
import os
from abc import ABC, abstractmethod
from functools import wraps


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class MediaFactory:
    @staticmethod
    def create_media(media_type, *args):
        from models.inheritance import Podcast, Song

        if media_type == "song":
            return Song(*args)
        elif media_type == "podcast":
            return Podcast(*args)
        else:
            raise ValueError(f"Неизвестный тип медиа: {media_type}")


class PlaylistObserver:
    def update(self, event_type, data=None):
        print(f"[Уведомление] Тип события: {event_type}, данные: {data}")


class Subject:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, event_type, data=None):
        for observer in self._observers:
            observer.update(event_type, data)


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, items):
        pass


class SortByTitle(SortStrategy):
    def sort(self, items):
        return sorted(items, key=lambda x: x.get_title())


class SortByDuration(SortStrategy):
    def sort(self, items):
        return sorted(items, key=lambda x: x.get_duration())


class SortByArtist(SortStrategy):
    def sort(self, items):
        return sorted(items, key=lambda x: getattr(x, "get_artist", lambda: "")())


def file_logger_decorator(log_file="logs/app.log"):
    def decorator(func):
        @wraps(func)
        def wrapper(self, message):
            result = func(self, message)
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            class_name = self.__class__.__name__
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] {class_name}: {message}\n")
            return result

        return wrapper

    return decorator


class MP3Manager(Subject, metaclass=SingletonMeta):
    def __init__(self):
        Subject.__init__(self)
        self._playlist = []
        self.sort_strategy = SortByTitle()

    def add_media(self, media_type, *args):
        media = MediaFactory.create_media(media_type, *args)
        self._playlist.append(media)
        self.notify_observers("Добавлено", media.get_title())

    def get_playlist(self):
        return self._playlist

    def set_sort_strategy(self, strategy):
        self.sort_strategy = strategy

    def get_sorted_playlist(self):
        return self.sort_strategy.sort(self._playlist)

    def remove_media_by_title(self, title: str, cls) -> bool:
        title = title.strip().lower()
        removed_from_global = cls.remove_by_title(title)
        removed_from_playlist = any(
            item.get_title().strip().lower() == title for item in self._playlist
        )
        self._playlist = [
            item for item in self._playlist if item.get_title().strip().lower() != title
        ]

        if removed_from_global or removed_from_playlist:
            self.notify_observers("Файл удален", title)
            return True
        return False
