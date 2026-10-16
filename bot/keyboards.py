from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎵 Поиск музыки")],
            [KeyboardButton(text="📜 Показать всю музыку"), KeyboardButton(text="🗑 Очистить базу")],
            [KeyboardButton(text="⏱ Фильтр по длительности")]
        ],
        resize_keyboard=True
    )

def get_duration_filter_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="0-2 мин", callback_data="filter_0_120")],
            [InlineKeyboardButton(text="2-5 мин", callback_data="filter_120_300")],
            [InlineKeyboardButton(text="5+ мин", callback_data="filter_300_600")],
            [InlineKeyboardButton(text="⬅ Назад", callback_data="back_to_menu")]
        ]
    )
