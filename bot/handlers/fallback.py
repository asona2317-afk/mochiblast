"""
Handler fallback untuk menangkap pesan/callback yang tidak cocok dengan
handler manapun, supaya user tetap mendapat respons yang jelas.
"""

from aiogram import Router
from aiogram.types import CallbackQuery, Message

from bot.keyboards.user import main_menu_kb
from bot.utils import texts
from bot.utils.logger import get_logger

router = Router(name="fallback_router")
logger = get_logger(__name__)


@router.message()
async def fallback_message(message: Message) -> None:
    await message.answer(texts.UNKNOWN_COMMAND_TEXT, reply_markup=main_menu_kb())


@router.callback_query()
async def fallback_callback(callback: CallbackQuery) -> None:
    await callback.answer("Menu tidak tersedia atau sudah kedaluwarsa.", show_alert=True)
