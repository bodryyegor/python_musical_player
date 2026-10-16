from models.base import MP3
from models.exceptions import (
    EmptyPlaylistError,
    InvalidDataError,
    ObjectNotFoundError,
    ParsingError,
)
from models.patterns import (
    MP3Manager,
    PlaylistObserver,
    SortByArtist,
    SortByDuration,
    SortByTitle,
)
from utils.database import DBManager
from utils.parsers import Parser

parser = Parser()
manager = MP3Manager()
observer = PlaylistObserver()
manager.add_observer(observer)


def main():
    login = input()
    DB = DBManager(login + ".db")
    while True:
        print("\nМеню:")
        print("1. Добавить песню(уйдет ещё и в ДБ)")
        print("2. Добавить подкаст(ноу парсинг)")
        print("3. Просмотреть все файлы")
        print("4. Удалить файл")
        print("5. Изменить стратегию сортировки")
        print("6. Вывод ДБ")
        print("7. Фильтр по длителности в ДБ")
        print("0. Выход")
        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                title = input("Введите название песни: ")
                html = parser.get_html(title)
                if not html:
                    raise ParsingError()
                song = parser.unpack_html(html)
                if not song:
                    raise ObjectNotFoundError()
                manager.add_media("song", song[0], song[1], song[2])
                DB.insert(song[0], song[1], song[2])

            elif choice == "2":
                title = input("Введите название подкаста: ")
                host = input("Введите ведущего: ")
                topic = input("Введите тему: ")
                duration = int(input("Введите длину подкаста (в секундах): "))
                manager.add_media("podcast", title, host, topic, duration)

            elif choice == "3":
                playlist = manager.get_sorted_playlist()
                if not playlist:
                    raise EmptyPlaylistError()
                print("\nСписок всех файлов:")
                for item in playlist:
                    MP3.display_info(item)

            elif choice == "4":
                title_to_delete = input("Введите название файла для удаления: ")
                success = manager.remove_media_by_title(title_to_delete, MP3)
                DB.delete_by_title(title_to_delete)
                if success:
                    print(f"\nФайл '{title_to_delete}' успешно удален.")
                else:
                    print(f"\nФайл '{title_to_delete}' не найден.")

            elif choice == "5":
                sort_choice = input(
                    "Сортировать по:\n1 - названию\n2 - длительности\n3 - исполнителю\nВыберите: "
                )
                if sort_choice == "1":
                    manager.set_sort_strategy(SortByTitle())
                    DB.sort_db("title")
                    print("Теперь сортировка по названию.")
                elif sort_choice == "2":
                    manager.set_sort_strategy(SortByDuration())
                    DB.sort_db("duration")
                    print("Теперь сортировка по длительности.")
                elif sort_choice == "3":
                    manager.set_sort_strategy(SortByArtist())
                    DB.sort_db("artist")
                    print("Теперь сортировка по исполнителю.")
                else:
                    print("Неверный выбор.")
            elif choice == "6":
                DB.print_db()
            elif choice == "7":
                user_input = input(
                    "Введите min и max через пробел (можно пропустить): "
                ).split()
                if len(user_input) == 2:
                    min_val, max_val = map(int, user_input)
                    DB.filter_duration(min_val, max_val)
                elif len(user_input) == 1 and user_input[0].isdigit():
                    min_val = int(user_input[0])
                    DB.filter_duration(min=min_val)
                else:
                    DB.filter_duration()
            elif choice == "0":
                print("Выход")
                break
            else:
                print("Неверный выбор. Пожалуйста, выберите пункт из меню.")

        except InvalidDataError as e:
            print(f"Ошибка в данных: {e}")
        except ObjectNotFoundError:
            print("Ошибка: Файл с указанным названием не найден.")
        except EmptyPlaylistError:
            print("Ошибка: Ваш плейлист пуст. Добавьте файлы.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
    DB.close()


if __name__ == "__main__":
    main()
