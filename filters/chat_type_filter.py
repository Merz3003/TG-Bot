from aiogram.filters import Filter
from aiogram.types import Message

class IsGroupChat(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type in {"group", "supergroup"}

class IsPrivateChat(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.chat.type == "private"
