# Music Player

A console application for managing a playlist of songs and podcasts. The player lets you add, view, and remove MP3 media files through a simple interactive CLI.

## Overview

**Music Player** is a command-line tool built in Python that manages a shared collection of media items — both songs and podcasts. The main goal of the project is to give the user a straightforward way to add, remove, and inspect MP3 media files, with clear error handling and a single unified playlist.

## Features

- Add songs and podcasts to the playlist.
- View all items in the playlist with detailed information.
- Remove items from the playlist by title.
- Graceful error handling:
  - empty playlist,
  - invalid input,
  - missing item / object.
- All created objects are stored in a single shared collection.

## Requirements

- **Python 3.9+**
- **Poetry 1.8.0**
- Python standard library only (no external runtime dependencies)

## Project structure

```text
.
├── config.py
├── main.py
├── models
│   ├── base.py
│   ├── inheritance.py
│   └── __init__.py
├── poetry.lock
├── pyproject.toml
└── README.md
```

### Structure overview

| Path | Purpose |
|------|---------|
| `main.py` | Entry point. Contains the application logic and the interactive CLI. |
| `models/base.py` | Base class for all MP3 file types, plus custom exceptions. |
| `models/inheritance.py` | Subclasses of the base MP3 class (e.g., song, podcast). |
| `models/__init__.py` | Marks `models` as a Python package. |
| `config.py` | Project-wide configuration values. |
| `pyproject.toml` | Poetry configuration: dependencies, metadata, scripts. |
| `poetry.lock` | Locked dependency versions for reproducible installs. |

## Installation

### 1. Install Poetry

If Poetry is not installed yet:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Or follow the official guide: <https://python-poetry.org/docs/#installation>

### 2. Install project dependencies

```bash
poetry install
```

## Running

```bash
poetry run python main.py
```

## Usage

On start, the application displays the following menu:

```text
Меню:
1. Добавить песню
2. Добавить подкаст
3. Просмотреть все файлы
4. Удалить файл
5. Выход
Выберите действие:
```

- **1 — Add a song.** Prompts for the song’s details and appends it to the playlist.
- **2 — Add a podcast.** Prompts for the podcast’s details and appends it to the playlist.
- **3 — View all files.** Prints every item in the playlist with its details.
- **4 — Delete a file.** Asks for a title and removes the matching item.
- **5 — Exit.** Closes the application.

## Error handling

The application handles the following situations without crashing:

| Situation | Behaviour |
|-----------|-----------|
| Empty playlist | Prints a friendly message instead of an empty list. |
| Invalid input | Asks the user to re-enter the value. |
| Missing item | Reports that no matching object was found and returns to the menu. |

## Design notes

- All media items inherit from a common base class defined in `models/base.py`.
- Custom exceptions live next to the base class and are raised from the model layer.
- The CLI in `main.py` catches those exceptions and turns them into readable messages.
- The playlist itself is a single shared collection — every created object is stored there.

## License

MIT License. See `LICENSE` if included.
