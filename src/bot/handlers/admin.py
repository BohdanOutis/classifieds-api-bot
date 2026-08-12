from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

import httpx

from ..filters.admin import IsAdmin
from ..keyboards.admin_kb import admin_kb
from ..services.wordpress import upload_media_to_wordpress, create_lisfinity_listing

router = Router()

router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())

class UsersPhotoPagination(CallbackData, prefix="users_photo"):
    index: int
    photo_index: int

class ModernizationCallback(CallbackData, prefix="modernization"):
    action: str
    advert_id: int

class ModerationStates(StatesGroup):
    waiting_for_reject_reason = State()

class VipStates(StatesGroup):
    waiting_for_username = State()

class AdminStates(StatesGroup):
    waiting_for_username = State()

@router.message(Command("admin"))
async def admin_panel(message: Message):
    await message.answer(
        text="Головне меню Адміна",
        reply_markup=admin_kb()
    )

# -------------------
# Надання статусу VIP
# -------------------

@router.message(F.text == "👑 Надати VIP")
async def give_vip(message: Message, state: FSMContext):
    await message.answer(
        text="Напишіть юзернейм користувача"
    )
    await state.set_state(VipStates.waiting_for_username)

@router.message(VipStates.waiting_for_username)
async def proccess_vip_status(message: Message, api_client: httpx.AsyncClient, state: FSMContext, bot: Bot):
    username = message.text.lstrip('@')

    user_response = await api_client.get(f"/users/by-username/{username}")

    if user_response.status_code == 404:
        await message.answer(
            f"❌ Користувача <b>@{username}</b> не знайдено в базі бота.\n"
            "Перевірте правильність написання та спробуйте ще раз."
        )
        return
    elif user_response.status_code != 200:
        await message.answer("Помилка сервера при пошуку користувача.")
        return

    user_data = user_response.json()
    tg_id = user_data["tg_id"]

    vip_response = await api_client.patch(f"/users/{tg_id}/activate-vip", params={"days": 30})

    if vip_response.status_code == 200:
        user_data = vip_response.json()
        expire_date = user_data['vip_expire_at'][:10]

        await message.answer(
            f"✅ <b>VIP-статус успішно надано!</b>\n\n"
            f"👤 Користувач: @{username}\n"
            f"🆔 Telegram ID: <code>{tg_id}</code>\n"
            f"📅 Дійсний до: <b>{expire_date}</b>"
        )

        if tg_id:
            try:
                await bot.send_message(
                    chat_id=tg_id,
                    text="🎉 Вітаємо! Адміністратор надав вам <b>VIP-статус</b> на 30 днів!"
                )
            except Exception:
                pass

    elif vip_response.status_code == 404:
        await message.answer(
            f"Користувача @{username} не знайдено в базі бота!\n"
            "Переконайтеся, що він запустив бота хоча б один раз."
        )
    else:
        await message.answer("Помилка сервера. Спробуйте пізніше.")

    await state.clear()

# ---------------------
# Надання статусу Admin
# ---------------------

@router.message(F.text == "🔑 Надати статус адміна")
async def give_admin(message: Message, state: FSMContext):
    await message.answer(
        text="Напишіть юзернейм користувача"
    )
    await state.set_state(AdminStates.waiting_for_username)

@router.message(AdminStates.waiting_for_username)
async def proccess_admin_status(message: Message, api_client: httpx.AsyncClient, state: FSMContext, bot: Bot):
    username = message.text.lstrip('@')

    user_response = await api_client.get(f"/users/by-username/{username}")
    
    if user_response.status_code == 404:
        await message.answer(
            f"❌ Користувача <b>@{username}</b> не знайдено в базі бота.\n"
            "Перевірте правильність написання та спробуйте ще раз."
        )
        return
    elif user_response.status_code != 200:
        await message.answer("Помилка сервера при пошуку користувача.")
        return
    
    user_data = user_response.json()
    tg_id = user_data["tg_id"]

    response = await api_client.patch(f"/users/{tg_id}", json={"status": "admin"})

    if response.status_code == 200:
        proccess_admin = response.json()
        await message.answer(
            text=f"Статус Admin успішно надано користувачу {username}"
        )

        if tg_id:
            try:
                await bot.send_message(
                    chat_id=tg_id, 
                    text="🎉 Вітаємо! Вам надано VIP-статус!"
                )
            except Exception:
                pass

    elif response.status_code == 404:
        await message.answer(
            text=f"Користувача {username} не знайдено в базі бота! \n"
            "Переконайтеся, що він запустив бота хоча б один раз."
        )
    else:
        await message.answer(
            text=f"Статус Admin успішно надано користувачу {username}"
        )

    await state.clear()

# ----------------------------
# Додавання новинного ресурсу
# ----------------------------



# ---------------------
# Верифікація оголошень
# ---------------------

@router.message(F.text == "🛡️ Модерація оголошень")
async def advert_verification(message: Message, api_client: httpx.AsyncClient, state: FSMContext):
    await state.clear() 
    await show_advertisement_page(
        message_or_query=message,
        api_client=api_client,
        index=0,
        photo_index=0
    )

@router.callback_query(UsersPhotoPagination.filter())
async def photo_switcher(callback: CallbackQuery, callback_data: UsersPhotoPagination, api_client: httpx.AsyncClient):
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
    # Отримуємо оголошення користувача
    ads_response = await api_client.get("/ads/", params={"status": "pending"})

    if ads_response.status_code == 200:
        user_advertisements = ads_response.json()
    elif ads_response.status_code == 404:
        user_advertisements = []
    else:
        text = "Помилка сервера. Спробуйте пізніше."
        if isinstance(message_or_query, CallbackQuery):
            await message_or_query.answer(text, show_alert=True)
        else:
            await message_or_query.answer(text=text)
        return

    if not user_advertisements:
        text = "✅ Усі оголошення перевірені! Черга порожня."
        if isinstance(message_or_query, CallbackQuery):
            await message_or_query.answer()
        return await message_or_query.answer(text=text)

    if index < 0:
        index = len(user_advertisements) - 1
    elif index >= len(user_advertisements):
        index = 0

    data = user_advertisements[index]

    photo_response = await api_client.get("/ads_photos/", params={"advert_id": data["id"]})

    photos = photo_response.json() if photo_response.status_code == 200 else []    

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
        builder.button(text="⬅ Фото", callback_data=UsersPhotoPagination(index=index, photo_index=photo_index - 1))
        builder.button(text="Фото ➡", callback_data=UsersPhotoPagination(index=index, photo_index=photo_index + 1))
    
    if len(user_advertisements) > 1:
        builder.button(text="⏮ Поп. Оголош.", callback_data=UsersPhotoPagination(index=index - 1, photo_index=0))
        builder.button(text="Наст. Оголош. ⏭", callback_data=UsersPhotoPagination(index=index + 1, photo_index=0))

    builder.button(text="Схвалити ✅", callback_data=ModernizationCallback(action="approve", advert_id=data['id']))
    builder.button(text="Відхилити ❌", callback_data=ModernizationCallback(action="reject", advert_id=data['id']))
    builder.adjust(2)

    status_emoji = {"pending": "⏳ Очікує", "published": "✅ Опубліковано", "rejected": "❌ Відхилено"}
    current_status = status_emoji.get(data['status'], data['status'])

    caption_text = (
        f"📦 <b>Оголошення {index + 1} із {len(user_advertisements)}</b> "
        f"(Фото {photo_index + 1} з {len(photos) if photos else 0})\n\n"
        f"📌 <b>Назва:</b> {data['name']}\n"
        f"💰 <b>Ціна:</b> {data['price']} грн\n"
        f"📊 <b>Статус:</b> {current_status}\n"
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


@router.callback_query(ModernizationCallback.filter(F.action == "approve"))
async def approve_advertisement(
    callback: CallbackQuery, 
    callback_data: ModernizationCallback,
    api_client: httpx.AsyncClient,
    bot: Bot
):
    await callback.answer("Обробка рішення...")
    advert_id = callback_data.advert_id

    advert_response = await api_client.get(f"/ads/{advert_id}", params={"advert_id": advert_id})
    advert = advert_response.json() if advert_response.status_code == 200 else None

    uploaded_media_ids = []

    photo_response = await api_client.get("/ads_photos/", params={"advert_id": advert_id})
    photos = photo_response.json() if photo_response.status_code == 200 else []

    for photo in photos:
        file_info = await bot.get_file(photo.get('file_id'))
        file_bytes = await bot.download_file(file_info.file_path)

        media_id = await upload_media_to_wordpress(
            file_bytes=file_bytes.read(),
            filename=f"advert_{advert_id}_{len(uploaded_media_ids)}.jpg"
        )
        if media_id:
            uploaded_media_ids.append(media_id)

    wp_post_id = await create_lisfinity_listing(
        title=advert['name'],
        content=advert['description'],
        price=advert['price'],
        media_ids=uploaded_media_ids
    )

    if wp_post_id:
        response = await api_client.patch(f"/ads/{advert_id}", json={"advert_id": advert_id, "status": "approved", "wp_post_id": wp_post_id})
        if response.status_code == 200:
            await callback.message.answer(
                f"✅ Оголошення #{advert_id} схвалено і відправлено на WP (ID: {wp_post_id})"
            )
        elif response.status_code == 404:
            return await callback.message.answer(
                "Оголошення не існує"
            )
        else:
            return await callback.message.answer(
                "Помилка сервера. Спробуйте пізніше"
            )
    else:
        await callback.message.answer(
            "⚠️ Оголошення схвалено в боті, але НЕ опубліковано на WP"
        )

    try:
        await bot.send_message(
            chat_id=advert['user_id'],
            text=f"🎉 Ваше оголошення <b>«{advert['name']}»</b> успішно схвалено та опубліковано!"
        )
    except Exception:
        pass

    if callback.message.photo:
        await callback.message.edit_caption(
            caption=(callback.message.caption or "") + "\n\n🟢 <b>Схвалено!</b>",
            reply_markup=None
        )
    else:
        await callback.message.edit_text(
            text=callback.message.text + "\n\n🟢 <b>Схвалено!</b>",
            reply_markup=None
        )
    await callback.answer()

@router.callback_query(ModernizationCallback.filter(F.action == "reject"))
async def reject_advertisement(
    callback: CallbackQuery, 
    callback_data: ModernizationCallback,
    state: FSMContext
):
    
    await state.update_data(advert_id=callback_data.advert_id, admin_msg_id=callback.message.message_id, admin_chat_id=callback.message.chat.id)
    await state.set_state(ModerationStates.waiting_for_reject_reason)

    await callback.message.answer(text="✍️ Будь ласка, напишіть причину відхилення оголошення:")
    await callback.answer()


@router.message(ModerationStates.waiting_for_reject_reason)
async def proccess_reject_reason(message: Message, state: FSMContext, api_client: httpx.AsyncClient, bot: Bot):
    reason_text = message.text
    state_data = await state.get_data()
    
    advert_id = state_data["advert_id"]
    admin_msg_id = state_data["admin_msg_id"]
    admin_chat_id = state_data["admin_chat_id"]

    await api_client.patch(f"/ads/{advert_id}", json={"status": "rejected"})
    advert_response = await api_client.get(f"/ads/{advert_id}")
    advert = advert_response.json() if advert_response.status_code == 200 else None

    try:
        await bot.send_message(
            chat_id=advert['user_id'],
            text=f"❌ Ваше оголошення «{advert['name']}» було відхилено модератором.\n\n💬 <b>Причина:</b> {reason_text}"
        )
    except Exception:
        pass
        
    try:
        await bot.edit_message_reply_markup(chat_id=admin_chat_id, message_id=admin_msg_id, reply_markup=None)
    except Exception:
        pass
    
    await message.answer("✅ Причину відправлено автору, статус оголошення оновлено.")
    await state.clear()
    await show_advertisement_page(
        message_or_query=message,
        api_client=api_client,
        index=0,
        photo_index=0
    )

# ----------------------------
#       Статистика бота
# ----------------------------

@router.message(F.text == "📊 Статистика Бота")
async def bot_statistic(message: Message, api_client: httpx.AsyncClient):
    response = await api_client.get("/stats/")

    if response.status_code == 200:
        data = response.json()
        text = (
            f"📊 <b>Статистика Телеграм Бота</b>\n\n"
            f"👤 К-сть користувачів: <b>{data['total_users']}</b>\n"
            f"📦 К-сть активних оголошень: <b>{data['total_ads']}</b>\n"
            f"💵 Зароблено загалом: <b>{data['total_revenue']}</b> грн\n"
        )
        await message.answer(
            text=text,
            reply_markup=admin_kb()
        )

# ----------------------------
#            Вихід
# ----------------------------

@router.message(F.text == "Вийти")
async def quite(message: Message):
    await message.answer(
        text="...",
        reply_markup=ReplyKeyboardRemove()
    )