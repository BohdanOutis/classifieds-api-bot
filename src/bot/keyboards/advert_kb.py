from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

def advert_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ скасувати"), KeyboardButton(text="⬅ назад")]
        ],
        resize_keyboard=True
    )

def get_photos_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Зберегти оголошення")],
            [KeyboardButton(text="❌ скасувати"), KeyboardButton(text="⬅ назад")]
        ],
        resize_keyboard=True
    )

def category() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Cars"
    ))
    builder.add(InlineKeyboardButton(
        text="Headphones"
    ))
    builder.add(InlineKeyboardButton(
        text="Phones"
    ))
    builder.add(InlineKeyboardButton(
        text="Feet"
    ))
    builder.adjust(2)
    return builder.as_markup()