import html
import httpx
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import Command, or_f
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from ..keyboards.profile_kb import profile_kb
from ..keyboards.main_kb import start_kb

router = Router(name="profile")

class MyAdsPagination(CallbackData, prefix="myads"):
    index: int

@router.message(or_f(F.text == "👤 Профіль", Command("profile")))
async def profile(message: Message, api_client: httpx.AsyncClient):
    response = await api_client.get(f"/users/{message.from_user.id}")

    if response.status_code == 200:
        user = response.json()
        is_vip = user.get("is_vip", False)
    
        user_name = html.escape(str(user.get('name', 'Не вказано')))
    
        vip_status = "✅ Активна" if is_vip else "❌ Відсутня"
        role_status = user.get('status', 'USER')

        text = (
        f"👤 <b>Ваш профіль</b>\n\n"
        f"<b>Ім'я:</b> {user_name}\n"
        f"<b>Статус:</b> {role_status}\n"
        f"<b>VIP-підписка:</b> {vip_status}"
    )
        await message.answer(
            text=text,
            reply_markup=profile_kb()
        )
    elif response.status_code == 404:
        await message.answer("⚠ Ви ще не зареєстровані! Напишіть /start, щоб пройти реєстрацію.")
    else:
        await message.answer("❌ Помилка сервера. Спробуйте пізніше.")


@router.message(F.text == "📦 Мої оголошення")
async def my_advertisements(message: Message, api_client: httpx.AsyncClient):
    await show_advertisement_page(
        message_or_query=message,
        api_client=api_client,
        tg_id=message.from_user.id,
        index=0
    )


@router.callback_query(MyAdsPagination.filter())
async def my_advertisement_switcher(
    callback: CallbackQuery, 
    callback_data: MyAdsPagination, 
    api_client: httpx.AsyncClient
):
    await show_advertisement_page(
        message_or_query=callback,
        api_client=api_client,
        tg_id=callback.from_user.id,
        index=callback_data.index
    )
    await callback.answer()


# Заглушка для інфо-кнопки по центру
@router.callback_query(F.data == "current_page_info")
async def current_page_info_handler(callback: CallbackQuery):
    await callback.answer("Це поточна сторінка", show_alert=False)


async def show_advertisement_page(
    message_or_query: Message | CallbackQuery, 
    api_client: httpx.AsyncClient,
    tg_id: int, 
    index: int
):
    response = await api_client.get("/ads/", params={"tg_id": tg_id})
    print(f"{response.json()} + {response.status_code}")
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
        text = "У вас ще немає створених оголошень."
        if isinstance(message_or_query, CallbackQuery):
            return await message_or_query.message.edit_text(text)
        return await message_or_query.answer(text)

    if index < 0:
        index = len(user_advertisements) - 1
    elif index >= len(user_advertisements):
        index = 0

    data = user_advertisements[index]

    status_emoji = {"pending": "⏳ Очікує", "approved": "✅ Опубліковано", "rejected": "❌ Відхилено"}
    current_status = status_emoji.get(data.get("status"), data.get("status"))

    caption_text = (
        f"📦 <b>Оголошення {index + 1} із {len(user_advertisements)}</b>\n\n"
        f"📌 <b>Назва:</b> {data.get('name')}\n"
        f"💰 <b>Ціна:</b> {data.get('price')} грн\n"
        f"📊 <b>Статус:</b> {current_status}\n"
        f"📝 <b>Опис:</b>\n{data.get('description')}"
    )

    kb_builder = InlineKeyboardBuilder()
    kb_builder.button(text="⬅ Назад", callback_data=MyAdsPagination(index=index - 1))
    kb_builder.button(text=f"🔢 {index + 1}/{len(user_advertisements)}", callback_data="current_page_info")
    kb_builder.button(text="Вперед ➡", callback_data=MyAdsPagination(index=index + 1))
    kb_builder.adjust(3)

    photo_response = await api_client.get("/ads_photos/", params={"advert_id": data["id"]})
    photos = photo_response.json() if photo_response.status_code == 200 else []
    main_photo = photos[0]["file_id"] if photos else None

    if isinstance(message_or_query, CallbackQuery):
        try:
            if main_photo:
                await message_or_query.message.edit_media(
                    media=InputMediaPhoto(media=main_photo, caption=caption_text),
                    reply_markup=kb_builder.as_markup()
                )
            else:
                await message_or_query.message.edit_text(
                    text=caption_text,
                    reply_markup=kb_builder.as_markup()
                )
        except Exception:
            await message_or_query.message.delete()
            if main_photo:
                await message_or_query.message.answer_photo(
                    photo=main_photo,
                    caption=caption_text,
                    reply_markup=kb_builder.as_markup()
                )
            else:
                await message_or_query.message.answer(
                    text=caption_text,
                    reply_markup=kb_builder.as_markup()
                )
    else:
        if main_photo:
            await message_or_query.answer_photo(
                photo=main_photo,
                caption=caption_text,
                reply_markup=kb_builder.as_markup()
            )
        else:
            await message_or_query.answer(
                text=caption_text,
                reply_markup=kb_builder.as_markup()
            )


@router.message(F.text == "⬅ Назад до головного меню")
async def back_to_main(message: Message):
    await message.answer(
        "Головне меню:",
        reply_markup=start_kb()
    )