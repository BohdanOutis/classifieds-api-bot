import pytest

TEST_TG_ID = 999999
TEST_NAME = "test_user_1"

@pytest.fixture(autouse=True)
async def setup_test_user(client):
    payload = {"tg_id": TEST_TG_ID, "name": TEST_NAME}
    await client.post("/api/v1/users/", json=payload)
    yield

# --------------------------------------------
#                  POSITIVE
# --------------------------------------------

@pytest.mark.anyio
async def test_user_creation_success(client):
    response = await client.post("/api/v1/users/", json={"tg_id": TEST_TG_ID, "name": TEST_NAME})
    assert response.status_code == 201
    data = response.json()
    assert data["tg_id"] == TEST_TG_ID
    assert data["name"] == TEST_NAME

@pytest.mark.anyio
async def test_activate_vip_success(client):
    response = await client.patch(f"api/v1/users/{TEST_TG_ID}/activate-vip")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["is_vip"] == True

@pytest.mark.anyio
async def test_get_user_by_username_success(client):
    response = await client.get(f"/api/v1/users/by-username/{TEST_NAME}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == TEST_NAME

@pytest.mark.anyio
async def test_get_user_succes(client):
    response = await client.get(f"/api/v1/users/{TEST_TG_ID}")
    assert response.status_code == 200
    data = response.json()
    assert data["tg_id"] == TEST_TG_ID

@pytest.mark.anyio
async def test_update_user_success(client):
    payload = {
        "name": "test_user_2",
        "status": "admin",
        "is_vip": False
    }
    response = await client.patch(f"/api/v1/users/{TEST_TG_ID}", json = payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["status"] == payload["status"]
    assert data["is_vip"] == payload["is_vip"]

# --------------------------------------------
#                  Negative
# --------------------------------------------

@pytest.mark.anyio
async def test_get_user_not_found(client):
    """Перевірка, що для неіснуючого tg_id бекенд повертає 404."""
    fake_tg_id = 88888888
    response = await client.get(f"/api/v1/users/{fake_tg_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.anyio
async def test_activate_vip_user_not_found(client):
    """Перевірка активації VIP для неіснуючого користувача."""
    fake_tg_id = 88888888
    response = await client.patch(f"/api/v1/users/{fake_tg_id}/activate-vip")
    assert response.status_code == 404