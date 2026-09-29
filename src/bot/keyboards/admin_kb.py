from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def admin_kb() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    
    builder.button(text="🛡️ Модерація оголошень")
    builder.button(text="📰 Додати джерело новин")
    builder.button(text="👑 Надати VIP")
    builder.button(text="🔑 Надати статус адміна")
    builder.button(text="📊 Статистика Бота")
    builder.button(text="Вийти")
    
    builder.adjust(2, 2, 1, 1)
    
    return builder.as_markup(resize_keyboard=True)

def cancle_btn() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="❌ Скасувати")
    builder.adjust()
    return builder.as_markup(resize_keyboard=True)