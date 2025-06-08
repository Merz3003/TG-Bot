import time
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable

# user_id: timestamp последнего вызова
_last_called: Dict[int, float] = {}

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 2.0):
        self.rate_limit = rate_limit
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = data.get("event_from_user")
        if not user:
            return await handler(event, data)

        now = time.time()
        last_time = _last_called.get(user.id, 0)

        if now - last_time < self.rate_limit:
            return  # просто игнорируем
        _last_called[user.id] = now
        return await handler(event, data)
