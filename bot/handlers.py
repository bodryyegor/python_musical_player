from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F
from loguru import logger

from .states import MusicSearch
from .keyboards import get_main_keyboard, get_duration_filter_keyboard
from utils.parsers import MP3_parser
from utils.database import DBManager
import os

router = Router()
parser = MP3_parser()


def get_user_db(user_id):
    return DBManager(user_id)


@router.message(F.text == "/start")
async def start_handler(message: Message):
    try:
        logger.info(f"Пользователь {message.from_user.id}: /start")
        await message.answer("Привет!", reply_markup=get_main_keyboard())
    except Exception as e:
        logger.error(f"Ошибка в /start: {e}")


@router.message(F.text == "🎵 Поиск музыки")
async def search_music(message: Message, state: FSMContext):
    try:
        await message.answer("Введите название песни:")
        await state.set_state(MusicSearch.waiting_for_title)
    except Exception as e:
        logger.error(f"Ошибка при начале поиска: {e}")


@router.message(MusicSearch.waiting_for_title)
async def process_title(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        db_manager = get_user_db(user_id)

        title = message.text
        result = parser.get_html(title)
        title, artist, duration = result
        db_manager.insert(title, artist, duration)

        file_path = os.path.join("data/mp3", f"{title}.mp3")
        if os.path.exists(file_path):
            from aiogram.types import FSInputFile
            audio = FSInputFile(path=file_path)
            await message.answer_audio(audio=audio, caption=f"{title} — {artist}")
        else:
            await message.answer("Ошибка: файл не найден.")

        await state.clear()
    except Exception as e:
        logger.error(f"Ошибка при поиске: {e}")
        await message.answer("Произошла ошибка при поиске.")


@router.message(F.text == "📜 Показать всю музыку")
async def show_all_music(message: Message):
    try:
        user_id = message.from_user.id
        db_manager = get_user_db(user_id)

        rows = db_manager.select_all()
        if not rows:
            await message.answer("База данных пуста.")
            return

        for row in rows:
            _, title, artist, duration = row
            await message.answer(f"{title} — {artist}, {duration // 60}:{duration % 60:02d}")
    except Exception as e:
        logger.error(f"Ошибка при показе музыки: {e}")


@router.message(F.text == "🗑 Очистить базу")
async def clear_database(message: Message):
    try:
        user_id = message.from_user.id
        db_manager = get_user_db(user_id)
        db_manager.clear_db()
        await message.answer("Ваша база данных очищена.")
    except Exception as e:
        logger.error(f"Ошибка при очистке: {e}")


@router.message(F.text == "⏱ Фильтр по длительности")
async def filter_by_duration_start(message: Message):
    try:
        await message.answer("Выберите диапазон длительности:", reply_markup=get_duration_filter_keyboard())
    except Exception as e:
        logger.error(f"Ошибка при открытии фильтра: {e}")


@router.callback_query(F.data.startswith("filter_"))
async def filter_by_duration(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        db_manager = get_user_db(user_id)

        _, min_time, max_time = callback.data.split("_")
        results = db_manager.filter_by_duration(int(min_time), int(max_time))

        if not results:
            await callback.message.answer("Ничего не найдено в этом диапазоне.")
        else:
            for row in results:
                _, title, artist, duration = row
                await callback.message.answer(f"{title} — {artist}, {duration // 60}:{duration % 60:02d}")

        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка в фильтре: {e}")


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    try:
        await callback.message.edit_text("Главное меню:", reply_markup=get_main_keyboard())
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка при возврате в меню: {e}")
