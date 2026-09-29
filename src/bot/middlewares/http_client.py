import httpx 
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from ...core.config import config

class HttpClientMiddleware(BaseMiddleware):
    def __init__(self, api_base_url: str):
        super().__init__()
        
        headers = {
            "X-API-Key": config.api.server_secret_key.get_secret_value(),
            "Content-Type": "application/json",
        }

        self.client = httpx.AsyncClient(
            base_url=api_base_url,
            headers=headers,
            timeout=10.0,
            follow_redirects=True
        )

    async def __call__(
        self, 
        handler, 
        event, 
        data
    ):
       data["api_client"] = self.client
       return await handler(event, data)