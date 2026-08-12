from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
import httpx 

class HttpClientMiddleware(BaseMiddleware):
    def __init__(self, api_base_url: str):
        super().__init__()
        self.client = httpx.AsyncClient(base_url=api_base_url, timeout=10.0, follow_redirects=True)

    async def __call__(
        self, 
        handler, 
        event, 
        data
    ):
       data["api_client"] = self.client
       return await handler(event, data)