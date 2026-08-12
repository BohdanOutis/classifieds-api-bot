from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def profile_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.add(KeyboardButton(
        text="📦 Мої оголошення"
    ))
    builder.add(KeyboardButton(
        text="⬅ Назад до головного меню"
    ))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)