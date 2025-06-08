from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from config.settings import settings
from keyboards.inline import currency_keyboard, get_language_keyboard
from services.crypto_api import get_rates
from services.fiat_api import get_fiat_rates
from utils.storage import save_user_currency, load_user_currency, save_user_language
from utils.logger import setup_logger
from filters import IsPrivateChat
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.translator import translate

logger = setup_logger()
router = Router()


@router.message(Command("start"))
async def start(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="English", callback_data="lang_en")
    builder.button(text="Русский", callback_data="lang_ru")
    builder.adjust(2)

    await message.answer(
        text="Please select your language / Пожалуйста, выберите язык:",
        reply_markup=builder.as_markup()
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    text = await translate(message.from_user.id, "help")
    await message.answer(text)


@router.message(Command("language"))
async def choose_language(message: Message):
    text = await translate(message.from_user.id, "choose_language")
    await message.answer(text, reply_markup=get_language_keyboard())


@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: CallbackQuery):
    lang_code = callback.data.split("_")[1]
    save_user_language(callback.from_user.id, lang_code)

    welcome_text = await translate(callback.from_user.id, "start")
    await callback.message.edit_text(welcome_text)


@router.message(Command("my_currency"), IsPrivateChat())
async def cmd_my_currency(message: Message):
    user_currency = load_user_currency(message.from_user.id) or settings.DEFAULT_CURRENCY
    text = await translate(message.from_user.id, "my_currency", currency=user_currency)
    await message.answer(text)


@router.message(Command("set_currency"))
async def cmd_set_currency(message: Message):
    text = await translate(message.from_user.id, "set_currency")
    await message.answer(text, reply_markup=currency_keyboard())


@router.callback_query(F.data.startswith("set_currency:"))
async def currency_chosen(callback: CallbackQuery):
    currency = callback.data.split(":")[1]
    save_user_currency(callback.from_user.id, currency)

    text = await translate(callback.from_user.id, "currency_set", currency=currency)
    await callback.message.answer(text)
    await callback.answer()


@router.message(Command("rates"))
async def cmd_rates(message: Message):
    user_currency = load_user_currency(message.from_user.id) or settings.DEFAULT_CURRENCY
    base_currency = "RUB"

    crypto_rates = await get_rates(base_currency)
    fiat_rates = await get_fiat_rates(base=base_currency, symbols=[user_currency])

    if not crypto_rates or not fiat_rates or user_currency not in fiat_rates:
        text = await translate(message.from_user.id, "error_rates")
        await message.answer(text)
        return

    fx = fiat_rates[user_currency]
    text = await translate(message.from_user.id, "rates_header", currency=user_currency.upper()) + "\n"

    for symbol, rub_value in crypto_rates.items():
        try:
            conv = rub_value * fx
            text += f"{symbol}: {conv:,.2f} {user_currency.upper()}\n"
        except Exception:
            text += f"{symbol}: error\n"

    await message.answer(text)


@router.message(Command("convert"))
async def cmd_convert(message: Message):
    parts = message.text.strip().split()
    if len(parts) != 3:
        text = await translate(message.from_user.id, "convert_usage")
        await message.reply(text)
        return

    _, amount_str, symbol = parts
    try:
        amount = float(amount_str.replace(",", "."))
        symbol = symbol.upper()
        if symbol not in {"ETH", "BTC", "TON", "SOL", "XRP"}:
            raise ValueError("Unknown crypto")
    except Exception:
        text = await translate(message.from_user.id, "convert_error_format")
        await message.reply(text)
        return

    user_currency = load_user_currency(message.from_user.id) or settings.DEFAULT_CURRENCY
    base_currency = "RUB"

    crypto_rates = await get_rates(base_currency)
    fiat_rates = await get_fiat_rates(base=base_currency, symbols=[user_currency])

    if symbol not in crypto_rates or user_currency not in fiat_rates:
        text = await translate(message.from_user.id, "error_rates")
        await message.reply(text)
        return

    try:
        rub_value = float(crypto_rates[symbol])
        fx = fiat_rates[user_currency]
        result = amount * rub_value * fx

        text = await translate(
            message.from_user.id,
            "convert_result",
            amount=amount,
            symbol=symbol,
            result=f"{result:,.2f}",
            currency=user_currency
        )
        await message.reply(text)
    except Exception:
        text = await translate(message.from_user.id, "convert_calc_error")
        await message.reply(text)
