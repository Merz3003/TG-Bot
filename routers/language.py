from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from keyboards.inline import get_language_keyboard
from utils.storage import save_user_language

router = Router()

@router.message(Command("language"))
async def choose_language(message: types.Message):
    await message.answer(
        "🌐 Выберите язык / Select your language:",
        reply_markup=get_language_keyboard()
    )

@router.callback_query(lambda c: c.data.startswith("lang_"))
async def set_language(callback: CallbackQuery):
    lang_code = callback.data.split("_")[1]
    save_user_language(callback.from_user.id, lang_code)
    await callback.message.edit_text(
        "✅ Язык успешно изменён!" if lang_code == "ru" else "✅ Language changed successfully!"
    )
