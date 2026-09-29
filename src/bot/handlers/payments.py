from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, CallbackQuery
from aiogram.filters import Command, or_f
import httpx

from ...core.config import config
from .adverts import AdvertPayment

router = Router()

PAYMENT_PROVIDER_TOKEN = config.portmone.secret_key.get_secret_value()


# ==========================================
# 1. СТВОРЕННЯ ІНВОЙСІВ (INVOICES)
# ==========================================

@router.message(or_f(F.text == "👑 Придбати VIP", Command("vip")))
async def process_vip(message: Message):
    await message.answer_invoice(
        title="👑 VIP статус (30 днів)",
        description=(
            "Отримай доступ до пріоритетної публікації оголошень, "
            "виділення кольором та відсутності лімітів!"
        ),
        payload="vip_subscription_30_days",  # Фіксований payload
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency="UAH",
        prices=[
            LabeledPrice(label="VIP Статус на 1 місяць", amount=150000) # 1500.00 UAH
        ],
        start_parameter="vip-pay"
    )


@router.callback_query(AdvertPayment.filter())
async def process_advert_payment(callback: CallbackQuery, callback_data: AdvertPayment):
    prices = [LabeledPrice(label=callback_data.name, amount=callback_data.price * 100)]
    await callback.message.answer_invoice(
        title=f"Купівля: {callback_data.name}",
        description=f"Оплата товару {callback_data.name} на суму {callback_data.price} грн",
        payload=f"advert_pay_{callback_data.id}",  # Динамічний payload з ID
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency="UAH",
        prices=prices,
        start_parameter="advert_payment",
    )
    await callback.answer()


# ==========================================
# 2. PRE_CHECKOUT QUERIES (ПІДТВЕРДЖЕННЯ)
# ==========================================

# Окрема перевірка для VIP
@router.pre_checkout_query(F.invoice_payload == "vip_subscription_30_days")
async def process_vip_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


# Окрема перевірка для оголошень (можна додати перевірку в БД, чи оголошення ще є)
@router.pre_checkout_query(F.invoice_payload.startswith("advert_pay_"))
async def process_advert_pre_checkout(pre_checkout_query: PreCheckoutQuery, api_client: httpx.AsyncClient):
    payload = pre_checkout_query.invoice_payload
    advert_id = int(payload.split("advert_pay_")[1])

    # Опціонально: Перевіряємо в API, чи товар не проданий
    response = await api_client.get(f"/ads/{advert_id}")
    if response.status_code == 200 and response.json().get("status") == "approved":
        await pre_checkout_query.answer(ok=True)
    else:
        await pre_checkout_query.answer(ok=False, error_message="Товар вже проданий або недоступний!")


# ==========================================
# 3. SUCCESSFUL PAYMENTS (ОБРОБКА ОПЛАТИ)
# ==========================================

# Успішна оплата VIP
@router.message(F.successful_payment.invoice_payload == "vip_subscription_30_days")
async def process_vip_successful_payment(
    message: Message,
    api_client: httpx.AsyncClient
):
    payment_info = message.successful_payment
    amount_uah = payment_info.total_amount / 100
    tg_id = message.from_user.id

    response = await api_client.post(
        "/payments/telegram-success",
        json={
            "tg_id": message.from_user.id,
            "amount": payment_info.total_amount / 100,
            "currency": payment_info.currency,
            "type": "vip_subscription",
            "provider_charge_id": payment_info.provider_payment_charge_id,
            "telegram_charge_id": payment_info.telegram_payment_charge_id
        }
    )

    response = await api_client.patch(
        f"/users/{tg_id}/activate-vip", 
        params={"tg_id": tg_id, "days": 30}
    )

    if response.status_code == 200:
        data = response.json()
        expire_date = data['vip_expires_at'][:10]

        await message.answer(
            f"🎉 <b>VIP-статус успішно активовано!</b>\n"
            f"Дійсний до: <b>{expire_date}</b>\n"
            f"Сума оплати: <b>{amount_uah:.2f} {payment_info.currency}</b>\n"
            f"Номер чека: <code>{payment_info.provider_payment_charge_id}</code>"
        )
    else:
        await message.answer("Виникла помилка під час активації VIP. Зверніться до підтримки.")


# Успішна оплата Оголошення
@router.message(F.successful_payment.invoice_payload.startswith("advert_pay_"))
async def process_advert_successful_payment(
    message: Message,
    api_client: httpx.AsyncClient
):
    payment_info = message.successful_payment
    total_amount = payment_info.total_amount // 100
    payload = payment_info.invoice_payload

    advert_id = int(payload.split("advert_pay_")[1])
    response = await api_client.patch(f"/ads/{advert_id}", json={"status": "sold"})

    if response.status_code == 200:
        await message.answer(
            f"🎉 <b>Дякуємо за покупку!</b>\n\n"
            f"Оплата оголошення №{advert_id} на суму <b>{total_amount} UAH</b> пройшла успішно.\n"
            f"Статус оголошення змінено на «Продано».",
        )
    else:
        await message.answer(
            f"⚠️ Оплата пройшла успішно, але виникла помилка оновлення статусу оголошення №{advert_id}.\n"
            f"Служба підтримки вже сповіщена."
        )