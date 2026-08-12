from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from aiogram.filters import Command, or_f
from ...core.config import config

import httpx

router = Router()

PAYMENT_PROVIDER_TOKEN = config.portmone.secret_key.get_secret_value()

@router.message(or_f(F.text == "👑 Придбати VIP", Command("vip")))
async def process_vip(message: Message):
    await message.answer_invoice(
        title="👑 VIP статус (30 днів)",
        description=(
            "Отримай доступ до пріоритетної публікації оголошень, "
            "виділення кольором та відсутності лімітів!"
        ),
        payload="vip_subscription_30_days",
        provider_token="1661751239:TEST:SH7R-NDje-QoRD-1T3c",
        currency="UAH",
        prices=[
            LabeledPrice(label="VIP Статус на 1 місяць", amount=150000)
        ],
        start_parameter="vip-pay"
    )


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def process_successful_payment(
    message: Message,
    api_client: httpx.AsyncClient
):
    payment_info = message.successful_payment
    amount_uah = payment_info.total_amount / 100

    tg_id = message.from_user.id
    response = await api_client.patch(f"/users/{tg_id}/activate-vip", params={"tg_id": tg_id, "days": 30})

    if response.status_code == 200:
        data = response.json()
        expire_date = data['vip_expires_at'][:10]

        await message.answer(
            f"🎉 <b>VIP-статус успішно активовано!</b>\n"
            f"Дійсний до: <b>{expire_date}</b>"
        )
    else:
        await message.answer("Виникла помилка під час активації VIP. Зверніться до підтримки.")

    await message.answer(
        f"🎉 <b>Дякуємо за покупку!</b>\n\n"
        f"Вам успішно активовано <b>VIP Статус</b> на 30 днів.\n"
        f"Сума оплати: <b>{amount_uah:.2f} {payment_info.currency}</b>\n"
        f"Номер чека: <code>{payment_info.provider_payment_charge_id}</code>"
    )