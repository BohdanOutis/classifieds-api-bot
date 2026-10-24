import pytest

@pytest.mark.anyio
async def test_health_check(client):
    """Тест перевірки загального стану сервера."""
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.anyio
async def test_get_bot_stats_empty(client):
    """Тест статистики, коли база даних порожня."""
    response = await client.get("/api/v1/stats/") # Заміни на свій префікс
    assert response.status_code == 200
    data = response.json()
    assert data["total_users"] == 0
    assert data["total_ads"] == 0
    assert data["total_revenue"] == 0