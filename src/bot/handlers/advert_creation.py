from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, or_f

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from aiogram.utils.media_group import MediaGroupBuilder

import httpx 

from ..keyboards.advert_kb import advert_keyboard, get_photos_keyboard
from ..keyboards.main_kb import start_kb

router = Router(name="advert")

class Advert(StatesGroup):
    advert_name = State()
    advert_desc = State()
    advert_price = State()
    advert_photos = State()

@router.message(Command("cancel"))
@router.message(F.text.lower() == "❌ скасувати")
async def cmd_cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(
        text="Створення оголошення скасовано",
        reply_markup=start_kb()
    )

@router.message(Advert.advert_name, F.text.lower() == "⬅ назад")
async def go_back(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Створення оголошення скасовано",
        reply_markup=start_kb()
    )

@router.message(Advert.advert_desc, F.text.lower() == "⬅ назад")
async def go_back_to_name(message: Message, state: FSMContext):
    await message.answer(
        text="Добре, напишіть назву товару заново:",
        )
    await state.set_state(Advert.advert_name)

@router.message(Advert.advert_price, F.text.lower() == "⬅ назад")
async def go_back_to_desc(message: Message, state: FSMContext):
    await message.answer(
        text="Добре, напишіть опис товару заново:",
    )
    await state.set_state(Advert.advert_desc)

@router.message(Advert.advert_photos, F.text.lower() == "⬅ назад")
async def go_back_to_price(message: Message, state: FSMContext):
    await message.answer(
        text="Добре, напишіть ціну товару заново:",
    )
    await state.set_state(Advert.advert_price)

@router.message(or_f(F.text == "➕ Створити оголошення", Command("create")))
async def cmd_advert_creation(message: Message, state: FSMContext):
    await message.answer(
        text="Напишіть назву товару:",
        reply_markup=advert_keyboard()
    )
    await state.set_state(Advert.advert_name)

@router.message(Advert.advert_name, F.text.len() > 10)
async def name_writen(message: Message, state: FSMContext):
    await state.update_data(writen_name = message.text)
    await message.answer(
        text="Напишіть опис цього товару:",
        reply_markup=advert_keyboard()
    )
    await state.set_state(Advert.advert_desc)

@router.message(Advert.advert_name)
async def name_writen_incorrect(message: Message):
    await message.answer(
        text=f"Будь ласка введіть назву оголошення правильно(Довжина повинна бути не менше 10 символів)",
        reply_markup=advert_keyboard()
    )

@router.message(Advert.advert_desc)
async def desc_writen(message: Message, state: FSMContext):
    await state.update_data(writen_desc = message.text)
    await message.answer(
        text="Вкажіть ціну товару:",
        reply_markup=advert_keyboard()
    )
    await state.set_state(Advert.advert_price)

@router.message(Advert.advert_price, F.text.isdigit())
async def price_writen(message: Message, state: FSMContext):
    await state.update_data(writen_price = int(message.text))
    await state.update_data(photos = [])
    await message.answer(
        text="Надішліть одне або кілька фото для вашого оголошення. \n"
             "Коли закінчите, натисніть кнопку <b>Зберегти оголошення</b> нижче:",
        reply_markup=get_photos_keyboard()
    )
    await state.set_state(Advert.advert_photos)

@router.message(Advert.advert_photos, F.photo)
async def process_photos(message: Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id

    data = await state.get_data()
    photos = data.get("photos", [])

    if len(photos) >= 5:
        return await message.answer("Максимум можна завантажити 5 фото!")
    
    photos.append(photo_file_id)
    await state.update_data(photos=photos)

@router.message(Advert.advert_photos, F.text == "Зберегти оголошення")
async def advert_creation_end(message: Message, state: FSMContext, api_client: httpx.AsyncClient):
    data = await state.get_data()
    photos = data.get("photos", [])

    if not photos:
        return await message.answer("Будь ласка, завантажте хоча б одне фото для оголошення!")

    payload = {
        "tg_id": message.from_user.id,
        "name": data['writen_name'],
        "description": data['writen_desc'],
        "price": data['writen_price']
    }
    response = await api_client.post("/ads/", json=payload)
    
    if response.status_code in (200, 201):
        advert = response.json()
    elif response.status_code == 404:
        text = "У вас ще немає створених оголошень."
        return await message.answer(text)
    else:
        text = "Помилка сервера. Спробуйте пізніше."
        return await message.answer(text)
    
    payload = {
        "advert_id": advert["id"],
        "file_ids": photos
    }

    try:
        await api_client.post("/ads_photos/", json=payload)
    except httpx.ReadTimeout:
        await message.answer("⏱️ Сервер довго відповідає. Спробуйте ще раз трохи пізніше.")
        return
    except httpx.RequestError:
        await message.answer("❌ Не вдалося з'єднатися з сервером.")
        return

    caption_text = (
        f"<b>{data['writen_name']}</b> - {data['writen_price']} грн\n\n"
        f"<b>Опис:</b>\n{data['writen_desc']}"
    )

    media_builder = MediaGroupBuilder(caption=caption_text)

    for file_id in photos:
        media_builder.add_photo(media=file_id)

    await message.answer(
        text="Чудово! Ось створене вами оголошення:\n",
        reply_markup=start_kb()
    )

    await message.answer_media_group(
        media=media_builder.build()
    )
    await state.clear()

@router.message(Advert.advert_price)
async def advert_price_incorrect(message: Message):
    await message.answer(
        text="Будь ласка, вкажіть ціну коректно, використовуючи лише цифри.\n"
        "Наприклад: 1500",
        reply_markup=advert_keyboard()
    )