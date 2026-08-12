from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter
import httpx

class IsAdmin(Filter):
    async def __call__(self, event: Message | CallbackQuery, api_client: httpx.AsyncClient):
        tg_id = event.from_user.id
        response = await api_client.get(f"/users/{tg_id}", params={"tg_id": tg_id})
        user = response.json() if response.status_code == 200 else None
        if user and user['status'] == "admin":
            return True
        return False

