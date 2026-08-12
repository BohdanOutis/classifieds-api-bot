from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def nothing(message: Message) -> None:
    await message.answer("okay")