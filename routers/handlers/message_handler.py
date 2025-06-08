from aiogram import Router
from aiogram.types import Message
from config.settings import settings
from services.crypto_api import get_rates
from services.fiat_api import get_fiat_rates
from utils.storage import load_user_currency
from utils.logger import setup_logger
import re

router = Router()
logger = setup_logger()

CRYPTO_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*(ETH|BTC|TON|SOL|XRP)", re.IGNORECASE)
FIAT_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*(USD|EUR|RUB|KZT|TRY)", re.IGNORECASE)

@router.message()
async def crypto_or_fiat_handler(message: Message):
    user_id = message.from_user.id
    user_currency = load_user_currency(user_id) or settings.DEFAULT_CURRENCY

    crypto_match = CRYPTO_PATTERN.search(message.text)
    fiat_match = FIAT_PATTERN.search(message.text)

    # Криптовалюта
    if crypto_match:
        amount, symbol = crypto_match.groups()
        amount = float(amount)
        symbol = symbol.upper()
        logger.info(f"[CRYPTO] {user_id}: {amount} {symbol}")

        base_currency = "RUB"
        crypto_rates = await get_rates(base_currency)

        # Обработка RUB→RUB без API-запроса
        if user_currency == base_currency:
            fx = 1.0
        else:
            fiat_rates = await get_fiat_rates(base=base_currency, symbols=[user_currency])
            fx = fiat_rates.get(user_currency)

        if symbol not in crypto_rates or fx is None:
            await message.reply("Ошибка: курс не найден.")
            return

        rub_value = crypto_rates[symbol]
        result = amount * rub_value * fx
        await message.reply(f"{amount} {symbol} = {result:,.2f} {user_currency}")
        return

    # Фиатная валюта
    if fiat_match:
        amount, from_currency = fiat_match.groups()
        amount = float(amount)
        from_currency = from_currency.upper()
        to_currency = user_currency.upper()
        logger.info(f"[FIAT] {user_id}: {amount} {from_currency} → {to_currency}")

        if from_currency == to_currency:
            await message.reply(f"{amount} {from_currency} = {amount:.2f} {to_currency}")
            return

        rates = await get_fiat_rates(base=from_currency, symbols=[to_currency])
        fx = rates.get(to_currency)

        if fx is None:
            await message.reply("Ошибка: невозможно пересчитать.")
            return

        result = amount * fx
        await message.reply(f"{amount} {from_currency} = {result:,.2f} {to_currency}")
        return

    # Сообщение не распознано — только в ЛС
    if message.chat.type == "private":
        await message.reply(
            "🤖 Я не понял сообщение.\n"
            "Пример: 3 ETH, 1000 USD, 200 TRY"
        )
