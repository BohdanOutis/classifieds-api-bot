from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.callback_data import CallbackData

import httpx

router = Router()

class PhotoPagination(CallbackData, prefix="photo_pagination"):
    index: int
    photo_index: int

@router.message(F.text == "📋 Оголошення")
async def adverts(message: Message, api_client: httpx.AsyncClient):
    await show_advertisement_page(
        message_or_query=message,
        api_client=api_client,
        index=0,
        photo_index=0
    )

@router.callback_query(PhotoPagination.filter())
async def photo_switcher(callback: CallbackQuery, callback_data: PhotoPagination, api_client: httpx.AsyncClient):
    await show_advertisement_page(
        message_or_query=callback,
        api_client=api_client,
        index=callback_data.index,
        photo_index=callback_data.photo_index
    )
    await callback.answer()


async def show_advertisement_page(
        message_or_query: Message | CallbackQuery,
        api_client: httpx.AsyncClient,
        index: int,
        photo_index: int,
):
    response = await api_client.get("/ads/", params={"status": "approved"})
    
    if response.status_code == 200:
        user_advertisements = response.json()
    elif response.status_code == 404:
        text = "У вас ще немає створених оголошень."
        if isinstance(message_or_query, CallbackQuery):
            return await message_or_query.message.edit_text(text)
        return await message_or_query.answer(text)
    else:
        text = "Помилка сервера. Спробуйте пізніше."
        if isinstance(message_or_query, CallbackQuery):
            return await message_or_query.answer(text, show_alert=True)
        return await message_or_query.answer(text)

    if not user_advertisements:
        text = "Немає оголошень"
        if isinstance(message_or_query, CallbackQuery):
            return await message_or_query.message.edit_text(text)
        return await message_or_query.answer(text=text)

    if index < 0:
        index = len(user_advertisements) - 1
    elif index >= len(user_advertisements):
        index = 0

    data = user_advertisements[index]

    photo_response = await api_client.get("/ads_photos/", params={"advert_id": data["id"]})
    photos = photo_response.json() if photo_response.status_code == 200 else []
    main_photo = photos[0]["file_id"] if photos else None

    if photos:
        if photo_index < 0:
            photo_index = len(photos) - 1
        elif photo_index >= len(photos):
            photo_index = 0
        photo = photos[photo_index]
    else:
        photo = None

    builder = InlineKeyboardBuilder()
    
    if photos and len(photos) > 1:
        builder.button(text="⬅ Фото", callback_data=PhotoPagination(index=index, photo_index=photo_index - 1))
        builder.button(text="Фото ➡", callback_data=PhotoPagination(index=index, photo_index=photo_index + 1))
    
    if len(user_advertisements) > 1:
        builder.button(text="⏮ Поп. Оголош.", callback_data=PhotoPagination(index=index - 1, photo_index=0))
        builder.button(text="Наст. Оголош. ⏭", callback_data=PhotoPagination(index=index + 1, photo_index=0))

    builder.button(text="Купити", callback_data=PhotoPagination(index=0, photo_index=0))
    builder.adjust(2)

    caption_text = (
        f"📦 <b>Оголошення {index + 1} із {len(user_advertisements)}</b> "
        f"(Фото {photo_index + 1} з {len(photos) if photos else 0})\n\n"
        f"📌 <b>Назва:</b> {data['name']}\n"
        f"💰 <b>Ціна:</b> {data['price']} грн\n"
        f"📝 <b>Опис:</b>\n{data['description']}"
    )

    if isinstance(message_or_query, CallbackQuery):
        try:
            if photo:
                await message_or_query.message.edit_media(
                    media=InputMediaPhoto(media=photo['file_id'], caption=caption_text, parse_mode="HTML"),
                    reply_markup=builder.as_markup()
                )
            else:
                await message_or_query.message.edit_text(
                    text=caption_text,
                    reply_markup=builder.as_markup(),
                    parse_mode="HTML"
                )
        except Exception:
            await message_or_query.answer()
    else:
        if photo:
            await message_or_query.answer_photo(
                photo=photo['file_id'],
                caption=caption_text,
                reply_markup=builder.as_markup(),
                parse_mode="HTML"
            )
        else:
            await message_or_query.answer(
                text=caption_text,
                reply_markup=builder.as_markup(),
                parse_mode="HTML"
            )