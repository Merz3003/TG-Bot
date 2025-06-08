from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config.settings import settings
from routers import commands, handlers, language
from routers.handlers import message_handler
from utils.logger import setup_logger
from middlewares.throttling import ThrottlingMiddleware
import asyncio


logger = setup_logger()

async def main():
    from aiogram.client.default import DefaultBotProperties

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher(storage=MemoryStorage())

    # Подключаем middleware антиспама
    dp.message.middleware(ThrottlingMiddleware(rate_limit=1))
    dp.callback_query.middleware(ThrottlingMiddleware(rate_limit=1.0))

    dp.include_routers(
        commands.router,
        language.router,
        message_handler.router
    )

    logger.info("Starting bot")
    await dp.start_polling(bot)

print('К боту можно перейти нажав по ссылке: t.me/Changer_for_chat_Bot')

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
