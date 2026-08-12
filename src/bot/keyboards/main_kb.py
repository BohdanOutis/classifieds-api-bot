from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def start_kb() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text='➕ Створити оголошення'),  
            KeyboardButton(text='👤 Профіль')
        ],
        [KeyboardButton(text='👑 Придбати VIP'), KeyboardButton(text="📋 Оголошення")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Виберіть дію'
        )
    return keyboard