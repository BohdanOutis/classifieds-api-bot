import pytest
from src.models.payments import PaymentType, PaymentStatus

TEST_TG_ID = 999999
TEST_NAME = "shinei33"

@pytest.fixture(autouse=True)
async def setup_test_user(client):
    payload = {"tg_id": TEST_TG_ID, "name": TEST_NAME}
    await client.post("/api/v1/users/", json=payload)
    yield

# --------------------------------------------
#                  POSITIVE
# --------------------------------------------

@pytest.mark.anyio
async def test_add_payment_success(client):
    payload = {
        "tg_id": TEST_TG_ID,
        "telegram_charge_id": "4444333322221111",
        "amount": 1000,
        "currency": "UAH",
        "service_type": PaymentType.VIP_SUBSCRIPTION.value,
        "status": PaymentStatus.SUCCESS.value,
        "ad_id": 1,
        "provider": "portmone",
        "provider_charge_id": "4444333322221111",
    }
    response = await client.post("/api/v1/payments/", json=payload)
    assert response.status_code == 201

# --------------------------------------------
#                  Negative
# --------------------------------------------

@pytest.mark.anyio
async def test_add_payment_fake_user(client):
    payload = {
        "tg_id": 888888,
        "telegram_charge_id": "1",
        "amount": 1000,
        "currency": "UAH",
        "service_type": PaymentType.VIP_SUBSCRIPTION.value,
        "status": PaymentStatus.SUCCESS.value,
        "ad_id": 1,
        "provider": "portmone",
        "provider_charge_id": "1",
    }
    response = await client.post("/api/v1/payments/", json=payload)
    assert response.status_code == 404

@pytest.mark.anyio
async def test_add_payment_duplicate_telegram_charge_id(client):
    """Спершу створюємо платіж, а потім намагаємося створити ще один із тим самим telegram_charge_id"""
    payload = {
        "tg_id": TEST_TG_ID,
        "telegram_charge_id": "DUPLICATE_TG_123",  # Використовуємо унікальне для цього тесту значення
        "amount": 500,
        "currency": "UAH",
        "service_type": PaymentType.VIP_SUBSCRIPTION.value,
        "status": PaymentStatus.SUCCESS.value,
        "provider": "portmone",
        "provider_charge_id": "prov_id_001",
    }
    
    # 1. Перший раз створюємо успішно (201)
    response_first = await client.post("/api/v1/payments/", json=payload)
    assert response_first.status_code == 201

    # 2. Другий раз відправляємо з ТАКИМ ЖЕ telegram_charge_id, але іншим provider_charge_id
    payload_duplicate = payload.copy()
    payload_duplicate["provider_charge_id"] = "prov_id_002"  # Змінюємо інше унікальне поле, щоб перевірити саме telegram_charge_id
    
    response_second = await client.post("/api/v1/payments/", json=payload_duplicate)
    assert response_second.status_code == 409


@pytest.mark.anyio
async def test_add_payment_duplicate_provider_charge_id(client):
    """Те ж саме для provider_charge_id"""
    payload = {
        "tg_id": TEST_TG_ID,
        "telegram_charge_id": "tg_id_002",
        "amount": 500,
        "currency": "UAH",
        "service_type": PaymentType.VIP_SUBSCRIPTION.value,
        "status": PaymentStatus.SUCCESS.value,
        "provider": "portmone",
        "provider_charge_id": "DUPLICATE_PROV_123",  # Унікальне для цього тесту
    }
    
    # 1. Перший раз успішно
    response_first = await client.post("/api/v1/payments/", json=payload)
    assert response_first.status_code == 201

    # 2. Другий раз із ТАКИМ ЖЕ provider_charge_id, але іншим telegram_charge_id
    payload_duplicate = payload.copy()
    payload_duplicate["telegram_charge_id"] = "tg_id_003"
    
    response_second = await client.post("/api/v1/payments/", json=payload_duplicate)
    assert response_second.status_code == 409