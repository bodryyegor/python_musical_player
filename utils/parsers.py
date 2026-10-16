from bs4 import BeautifulSoup as BS
from selenium import webdriver
import requests
import os


from models.exceptions import ObjectNotFoundError
from models.mixin import LogMixin

URL = "https://muzofond.fm/search/"
URL_2 = "https://rus.hitmotop.com/search?q="


class Parser(LogMixin):
    def get_html(self, title):
        self.log(f"Начало получения HTML для '{title}'")
        try:
            driver = webdriver.Chrome()
            driver.get(URL + title)
            html = driver.page_source
            driver.quit()
            self.log(f"Успешно получен HTML для '{title}'")
            return html
        except Exception as e:
            self.log(f"Ошибка при получении HTML: {str(e)}")
            raise e

    def time_to_sec(self, time_str):
        minutes, seconds = map(int, time_str.split(":"))
        return int(minutes) * 60 + int(seconds)

    def unpack_html(self, html):
        self.log("Начало парсинга HTML")
        try:
            borsh = BS(html, "html.parser")
            song = borsh.find("li", class_="item")
            if not song:
                raise ObjectNotFoundError("Элемент песни не найден")
            artist = song.find("span", class_="artist").get_text(strip=True)
            title = song.find("span", class_="track").get_text(strip=True)
            duration = self.time_to_sec(
                song.find("div", class_="duration enemy").get_text(strip=True)
            )
            self.log(f"Успешно распарсено: {title} - {artist} ({duration} сек)")
            return [title, artist, duration]
        except Exception as e:
            self.log(f"Ошибка парсинга HTML: {str(e)}")
            raise ObjectNotFoundError(f"Ошибка при парсинге: {str(e)}")
        
class MP3_parser(LogMixin):
    def time_to_sec(self, time_str):
        minutes, seconds = map(int, time_str.split(":"))
        return int(minutes) * 60 + int(seconds)
    def get_html(self, title):
        try:
            self.log(f"Начало получения HTML для '{title}'")
            response = requests.get(URL_2 + title)
            html = response.text
            self.log(f"Успешно получен HTML для '{title}'")
            borsh = BS(html, "html.parser")
            download_link = borsh.find("a", class_="track__download-btn").get("href")
            if not download_link:
                raise ObjectNotFoundError(f"Ошибка при парсинге: {str(e)}")
            title = borsh.find("div", class_="track__title").get_text(strip=True)
            artist = borsh.find("div", class_="track__desc").get_text(strip=True)
            duration = self.time_to_sec(borsh.find("div", class_="track__fulltime").get_text(strip=True))
            response = requests.get(download_link)
            path = os.path.join('./data/mp3', title + ".mp3")
            with open(path, 'wb') as f:
                f.write(response.content)
            print([title, artist, duration])
            return [title, artist, duration]
        except Exception as e:
            self.log(f"Ошибка при получении HTML: {str(e)}")
            raise e
