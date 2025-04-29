# middlewares/antiflood.py

from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any
import asyncio

class AntifloodMiddleware(BaseMiddleware):
    def __init__(self, limit: float = 1.0):
        self.limit = limit
        self._last_message_time: Dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Any],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        now = asyncio.get_running_loop().time()

        last_time = self._last_message_time.get(user_id, 0)
        if now - last_time < self.limit:
            return  # Игнорировать сообщение если слишком быстро

        self._last_message_time[user_id] = now
        return await handler(event, data)
