from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from ..keyboards.main_kb import start_kb
import httpx


router = Router(name="start")

@router.message(CommandStart())
async def cmd_start(message: Message, api_client: httpx.AsyncClient):
    payload = {
        "tg_id": message.from_user.id,
        "name": message.from_user.username
    }
    response = await api_client.post("/users/", json=payload)
    if response.status_code in (200,201):
        await message.answer(
            text=f"{message.from_user.full_name} ти задокшений і тд",
            reply_markup=start_kb()
        )
    else: 
        await message.answer("Сталася помилка при зверненні до сервера.")

@router.message(F.text, Command("help"))
async def cmd_help(message: Message):
    help_text = (
    "🤖 <b>Enterprise Classifieds Bot</b> — це зручний майданчик для розміщення та пошуку оголошень.\n\n"
    "<b>Ось що ви можете зробити тут:</b>\n"
    "📝 /create — Створити та опублікувати нове оголошення.\n"
    "🔍 /search — Знайти товари чи послуги за категоріями або ключовими словами.\n"
    "👤 /profile — Керувати своїми оголошеннями та переглянути баланс.\n"
    "💎 /vip — Дізнатися про переваги та придбати VIP-статус для ваших оголошень.\n\n"
    "Якщо у вас виникли технічні питання, звертайтеся до нашої підтримки: @support_username"
    )
    await message.answer(help_text)