from .base import MP3
from .exceptions import InvalidDataError


class Song(MP3):
    __slots__ = ("_artist", "_album")

    def __init__(self, title, artist, duration):
        super().__init__(title, duration)
        self._artist = ""
        #        self._album = ""
        self.set_artist(artist)
        self.log("Создан объект")

    def get_artist(self):
        return self._artist

    def set_artist(self, new_artist):
        if isinstance(new_artist, str) and new_artist.strip():
            self._artist = new_artist
        else:
            raise InvalidDataError("Исполнитель должен быть непустой строкой.")

    #    def get_album(self):
    #        return self._album

    #    def set_album(self, new_album):
    #        if isinstance(new_album, str) and new_album.strip():
    #            self._album = new_album
    #        else:
    #            raise InvalidDataError("Альбом должен быть непустой строкой.")

    def __str__(self):
        return f"{super().__str__()}, Исполнитель: {self.get_artist()}"


class Podcast(MP3):
    __slots__ = ("_host", "_topic")

    def __init__(self, title, host, topic, duration):
        super().__init__(title, duration)
        self._host = ""
        self._topic = ""
        self.set_host(host)
        self.set_topic(topic)

    def get_host(self):
        return self._host

    def set_host(self, new_host):
        if isinstance(new_host, str) and new_host.strip():
            self._host = new_host
        else:
            raise InvalidDataError("Ведущий должен быть непустой строкой.")

    def get_topic(self):
        return self._topic

    def set_topic(self, new_topic):
        if isinstance(new_topic, str) and new_topic.strip():
            self._topic = new_topic
        else:
            raise InvalidDataError("Тема должна быть непустой строкой.")

    def __str__(self):
        return (
            f"{super().__str__()}, Ведущий: {self.get_host()}, Тема: {self.get_topic()}"
        )
