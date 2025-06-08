from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

SUPPORTED_CURRENCIES = [
    ("🇷🇺 RUB", "RUB"),
    ("🇺🇸 USD", "USD"),
    ("🇪🇺 EUR", "EUR"),
    ("🇰🇿 KZT", "KZT"),
    ("🇹🇷 TRY", "TRY")
]

def currency_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=label, callback_data=f"set_currency:{code}")]
        for label, code in SUPPORTED_CURRENCIES
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)



def get_language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")
        ]
    ])
